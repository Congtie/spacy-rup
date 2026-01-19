import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import random
import os
import re
from tqdm import tqdm
from sklearn.model_selection import train_test_split

# --- CONFIGURĂRI ---
FILE_SRC = "basma_cunia.txt"
FILE_TRG = "basma_diaro.txt"
MODEL_PATH = "translator_final.pth"

# Model Bidirecțional Puternic
ENC_EMB_DIM = 64
DEC_EMB_DIM = 64
HID_DIM = 128
ENC_DROPOUT = 0.5
DEC_DROPOUT = 0.5
BATCH_SIZE = 64
N_EPOCHS = 50          # Mai multe epoci pentru tranziția lină
LEARNING_RATE = 0.0005

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# =========================================================================
# 1. DATE + AUGMENTARE (Același cod bun de data trecută)
# =========================================================================
def generate_synthetic_data(diaro_lines):
    synthetic_pairs = []
    replacements = [
        ("ș", "sh"), ("Ș", "Sh"), ("ț", "ts"), ("Ț", "Ts"),
        ("ľ", "lj"), ("Ľ", "Lj"), ("ń", "nj"), ("Ń", "Nj"),
        ("d̦", "dz"), ("D̦", "Dz"), ("ă", "ã"),  ("Ă", "Ã"),
        ("â", "ã"),  ("Â", "Ã"), ("î", "ã"),  ("Î", "Ã")
    ]
    for line in diaro_lines:
        words = line.strip().split()
        for w_diaro in words:
            w_clean = re.sub(r'[^\w]', '', w_diaro)
            if not w_clean: continue
            w_cunia = w_clean
            for d_char, c_char in replacements:
                w_cunia = w_cunia.replace(d_char, c_char)
            synthetic_pairs.append((w_cunia.lower(), w_clean.lower()))
    return list(set(synthetic_pairs))

def load_data():
    pairs = []
    if os.path.exists(FILE_SRC) and os.path.exists(FILE_TRG):
        with open(FILE_SRC, "r", encoding="utf-8") as f: src = f.readlines()
        with open(FILE_TRG, "r", encoding="utf-8") as f: trg = f.readlines()
        for s, t in zip(src, trg):
            s_words = s.strip().lower().split()
            t_words = t.strip().lower().split()
            if len(s_words) == len(t_words):
                for ws, wt in zip(s_words, t_words):
                    pairs.append((ws, wt))
    
    if os.path.exists(FILE_TRG):
        with open(FILE_TRG, "r", encoding="utf-8") as f: diaro_lines = f.readlines()
        pairs.extend(generate_synthetic_data(diaro_lines))
    
    unique_pairs = list(set(pairs))
    filtered_pairs = [p for p in unique_pairs if p[0] != p[1] or len(p[0]) > 3]
    return filtered_pairs

class Vocabulary:
    def __init__(self):
        self.char2idx = {"<PAD>": 0, "<SOS>": 1, "<EOS>": 2, "<UNK>": 3}
        self.idx2char = {0: "<PAD>", 1: "<SOS>", 2: "<EOS>", 3: "<UNK>"}
        self.n_chars = 4
    def add_text(self, text):
        for char in text:
            if char not in self.char2idx:
                self.char2idx[char] = self.n_chars
                self.idx2char[self.n_chars] = char
                self.n_chars += 1
    def encode(self, text):
        return [self.char2idx.get(c, 3) for c in text]

class WordDataset(Dataset):
    def __init__(self, pairs, vocab):
        self.pairs = pairs
        self.vocab = vocab
    def __len__(self): return len(self.pairs)
    def __getitem__(self, idx):
        s, t = self.pairs[idx]
        src = [1] + self.vocab.encode(s[:25]) + [2]
        trg = [1] + self.vocab.encode(t[:25]) + [2]
        return torch.tensor(src), torch.tensor(trg)

def collate_fn(batch):
    src, trg = zip(*batch)
    src_pad = nn.utils.rnn.pad_sequence(src, padding_value=0, batch_first=True)
    trg_pad = nn.utils.rnn.pad_sequence(trg, padding_value=0, batch_first=True)
    return src_pad, trg_pad

# =========================================================================
# 2. MODEL BIDIRECTIONAL (GRU)
# =========================================================================
class Encoder(nn.Module):
    def __init__(self, input_dim, emb_dim, hid_dim, dropout):
        super().__init__()
        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.rnn = nn.GRU(emb_dim, hid_dim, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(dropout)
    def forward(self, src):
        embedded = self.dropout(self.embedding(src))
        outputs, hidden = self.rnn(embedded)
        return outputs, hidden

class Decoder(nn.Module):
    def __init__(self, output_dim, emb_dim, hid_dim, dropout):
        super().__init__()
        self.output_dim = output_dim
        self.embedding = nn.Embedding(output_dim, emb_dim)
        self.rnn = nn.GRU(hid_dim * 2 + emb_dim, hid_dim * 2, batch_first=True)
        self.fc_out = nn.Linear(hid_dim * 4 + emb_dim, output_dim)
        self.attn = nn.Linear(hid_dim * 4, hid_dim * 2)
        self.v = nn.Linear(hid_dim * 2, 1, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input, hidden, encoder_outputs):
        input = input.unsqueeze(1)
        embedded = self.dropout(self.embedding(input))
        src_len = encoder_outputs.shape[1]
        hidden_rep = hidden[-1].unsqueeze(1).repeat(1, src_len, 1)
        energy = torch.tanh(self.attn(torch.cat((hidden_rep, encoder_outputs), dim=2)))
        attention = torch.softmax(self.v(energy).squeeze(2), dim=1).unsqueeze(1)
        weighted = torch.bmm(attention, encoder_outputs)
        rnn_input = torch.cat((embedded, weighted), dim=2)
        output, hidden = self.rnn(rnn_input, hidden)
        prediction = self.fc_out(torch.cat((output, weighted, embedded), dim=2))
        return prediction.squeeze(1), hidden

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, device):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.device = device
    def forward(self, src, trg, teacher_forcing_ratio=0.5):
        batch_size = src.shape[0]
        trg_len = trg.shape[1]
        outputs = torch.zeros(batch_size, trg_len, self.decoder.output_dim).to(self.device)
        encoder_outputs, hidden = self.encoder(src)
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1).unsqueeze(0)
        input = trg[:, 0]
        for t in range(1, trg_len):
            output, hidden = self.decoder(input, hidden, encoder_outputs)
            outputs[:, t] = output
            teacher_force = random.random() < teacher_forcing_ratio
            input = trg[:, t] if teacher_force else output.argmax(1)
        return outputs

# =========================================================================
# 3. TRAINING LOOP (DYNAMIC TEACHER FORCING)
# =========================================================================
def train():
    pairs = load_data()
    vocab = Vocabulary()
    for s, t in pairs: vocab.add_text(s); vocab.add_text(t)
    
    train_pairs, test_pairs = train_test_split(pairs, test_size=0.1, random_state=42)
    train_loader = DataLoader(WordDataset(train_pairs, vocab), batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
    test_loader = DataLoader(WordDataset(test_pairs, vocab), batch_size=BATCH_SIZE, collate_fn=collate_fn)
    
    enc = Encoder(vocab.n_chars, ENC_EMB_DIM, HID_DIM, ENC_DROPOUT)
    dec = Decoder(vocab.n_chars, DEC_EMB_DIM, HID_DIM, DEC_DROPOUT)
    model = Seq2Seq(enc, dec, device).to(device)
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    
    print("\nStart antrenament FINAL (Dynamic TF)...")
    best_loss = float('inf')

    for epoch in range(N_EPOCHS):
        model.train()
        
        # --- DYNAMIC TEACHER FORCING ---
        # Scade liniar de la 1.0 la 0.0 pe parcursul epocilor
        # Asta forțează modelul să devină independent
        tf_ratio = max(0.0, 1.0 - (epoch / (N_EPOCHS * 0.8))) 
        
        epoch_loss = 0
        loop = tqdm(train_loader, desc=f"Ep {epoch+1} [TF: {tf_ratio:.2f}]", leave=False)
        
        for src, trg in loop:
            src, trg = src.to(device), trg.to(device)
            optimizer.zero_grad()
            output = model(src, trg, tf_ratio) # Folosim ratio dinamic
            loss = criterion(output[:, 1:].reshape(-1, output.shape[-1]), trg[:, 1:].reshape(-1))
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            loop.set_postfix(loss=loss.item())

        # Validare
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for src, trg in test_loader:
                src, trg = src.to(device), trg.to(device)
                out = model(src, trg, 0) # 0 TF la validare
                val_loss += criterion(out[:, 1:].reshape(-1, out.shape[-1]), trg[:, 1:].reshape(-1)).item()
        
        avg_val = val_loss / len(test_loader)
        print(f"Ep {epoch+1} | Val Loss: {avg_val:.4f}")
        
        if avg_val < best_loss:
            best_loss = avg_val
            torch.save({
                'model': model.state_dict(),
                'vocab': vocab,
                'cfg': {'enc': ENC_EMB_DIM, 'dec': DEC_EMB_DIM, 'hid': HID_DIM, 'bidirectional': True}
            }, MODEL_PATH)

    print("Gata!")

if __name__ == "__main__":
    train()