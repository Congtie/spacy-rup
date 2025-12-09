#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

folder = 'spacy_rup'

fix_map = {
    'Ã£': 'ã',
    'Ã¢': 'â',
    'Ã®': 'î',
    'ÃŽ': 'Î',
    'Äƒ': 'ă',
    'Ä‚': 'Ă',
    'È™': 'ș',
    'È˜': 'Ș',
    'È›': 'ț',
    'Èš': 'Ț',
    'Å„': 'ń',
    'Å‚': 'ł',
    'Î³': 'γ',
    'â€ž': '„',
    'â€œ': '"',
    'â€"': '–',
}

for filename in sorted(os.listdir(folder)):
    if filename.endswith('.py'):
        filepath = os.path.join(folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for bad, good in fix_map.items():
            new_content = new_content.replace(bad, good)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'REPARAT: {filename}')
        else:
            print(f'OK: {filename}')
