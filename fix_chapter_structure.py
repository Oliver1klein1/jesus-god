#!/usr/bin/env python3
"""
Fix chapter styling in XHTML files by cleaning up the structure properly
"""

import os
import re

def fix_chapter_structure():
    # List of chapter files to fix
    chapter_files = [
        "epub/OEBPS/Text/chapter6.xhtml",
        "epub/OEBPS/Text/chapter7.xhtml", 
        "epub/OEBPS/Text/chapter8.xhtml",
        "epub/OEBPS/Text/chapter9.xhtml",
        "epub/OEBPS/Text/chapter10.xhtml"
    ]
    
    for file_path in chapter_files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        print(f"Fixing {file_path}...")
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the structure by removing extra divs and ensuring proper nesting
        # 1. Remove extra div tags that are interfering
        content = re.sub(r'<div class="chapter-card">\s*<div>\s*<h1>', r'<div class="chapter-card">\n<h1>', content)
        content = re.sub(r'</h1>\s*<div>\s*<p>', r'</h1>\n<p>', content)
        
        # 2. Ensure proper closing structure
        content = re.sub(r'</div>\s*</div>\s*</body>', r'        </div>\n    </div>\n</body>', content)
        
        # Write the fixed content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Fixed {file_path}")

if __name__ == "__main__":
    fix_chapter_structure()
