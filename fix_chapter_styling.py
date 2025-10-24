#!/usr/bin/env python3
"""
Fix chapter styling in XHTML files by adding proper container structure
"""

import os
import re

def fix_chapter_styling():
    # List of chapter files to fix
    chapter_files = [
        "epub/OEBPS/Text/chapter1.xhtml",
        "epub/OEBPS/Text/chapter2.xhtml", 
        "epub/OEBPS/Text/chapter3.xhtml",
        "epub/OEBPS/Text/chapter4.xhtml",
        "epub/OEBPS/Text/chapter5.xhtml",
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
        
        # Fix the structure
        # 1. Replace <div> with proper container structure
        content = re.sub(
            r'<body>\s*<div>',
            r'<body>\n    <div class="container mx-auto px-4">\n        <div class="chapter-card">',
            content
        )
        
        # 2. Close the containers properly before </body>
        content = re.sub(
            r'</div>\s*</body>',
            r'        </div>\n    </div>\n</body>',
            content
        )
        
        # 3. Add drop-cap class to first paragraph after h1
        content = re.sub(
            r'(<h1>.*?</h1>\s*)(<p[^>]*>)',
            r'\1<p class="drop-cap">',
            content,
            flags=re.DOTALL
        )
        
        # Write the fixed content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Fixed {file_path}")

if __name__ == "__main__":
    fix_chapter_styling()
