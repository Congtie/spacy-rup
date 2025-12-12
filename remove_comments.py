import os
import re

files = [
    'spacy_rup/__init__.py',
    'spacy_rup/tokenizer_exceptions.py',
    'spacy_rup/stop_words.py',
    'spacy_rup/punctuation.py',
    'spacy_rup/orthography.py',
    'spacy_rup/lex_attrs.py',
    'spacy_rup/lemma_component.py',
    'spacy_rup/lemmatizer.py',
    'spacy_rup/examples.py',
]

def remove_comments(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    in_docstring = False
    docstring_char = None
    
    for line in lines:
        stripped = line.lstrip()
        
        if '"""' in line or "'''" in line:
            if '"""' in line:
                char = '"""'
            else:
                char = "'''"
            
            count = line.count(char)
            if not in_docstring:
                in_docstring = True
                docstring_char = char
                new_lines.append(line)
                if count >= 2:
                    in_docstring = False
            else:
                new_lines.append(line)
                if char == docstring_char:
                    in_docstring = False
            continue
        
        if in_docstring:
            new_lines.append(line)
            continue
        
        if '#' in line:
            in_string = False
            quote_char = None
            result = []
            i = 0
            escaped = False
            
            while i < len(line):
                char = line[i]
                
                if escaped:
                    result.append(char)
                    escaped = False
                    i += 1
                    continue
                
                if char == '\\':
                    escaped = True
                    result.append(char)
                    i += 1
                    continue
                
                if char in ['"', "'"]:
                    if not in_string:
                        in_string = True
                        quote_char = char
                    elif char == quote_char:
                        in_string = False
                        quote_char = None
                    result.append(char)
                elif char == '#' and not in_string:
                    code_part = ''.join(result).rstrip()
                    if code_part:
                        new_lines.append(code_part)
                    break
                else:
                    result.append(char)
                i += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f'✓ Processed: {filepath}')

for filepath in files:
    remove_comments(filepath)

print('\nDone! All comments removed from source files.')
