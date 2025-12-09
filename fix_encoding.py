#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix corrupted UTF-8 characters in Python files."""

import os

# Mapping of corrupted -> correct characters
fix_map = {
    'Ã£': 'ã',
    'Ã¢': 'â', 
    'Ã®': 'î',
    'unÃ£': 'unã',
    'doauÃ£': 'doauã',
    'dauÃ£': 'dauã',
    'noauÃ£': 'noauã',
    'nauÃ£': 'nauã',
    'sutÃ£': 'sutã',
    'protÃ£': 'protã',
    'ultimÃ£': 'ultimã',
    'njiliunÃ£': 'njiliunã',
    'miliunÃ£': 'miliunã',
    'giumÃ£tati': 'giumãtati',
    'sfÃ£rtu': 'sfãrtu',
}

folder = 'spacy_rup'
fixed = 0

for filename in os.listdir(folder):
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
            print(f'Fixed: {filename}')
            fixed += 1
        else:
            print(f'OK: {filename}')

print(f'\nTotal fixed: {fixed} files')
