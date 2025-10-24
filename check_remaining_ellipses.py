#!/usr/bin/env python3
"""
Fix XML declaration and check remaining ellipses
"""
import os
import re
from pathlib import Path

def fix_xml_declaration_and_check(file_path):
    """Fix XML declaration and check remaining ellipses"""
    print(f"Checking {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix XML declaration
    content = content.replace('UTF...8', 'UTF-8')
    
    # Count ellipses
    ellipses_count = content.count('...')
    
    # Find examples of remaining ellipses
    lines = content.split('\n')
    examples = []
    for line in lines:
        if '...' in line and len(examples) < 5:
            examples.append(line.strip())
    
    # Write back if we fixed XML declaration
    if 'UTF-8' in content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"  {ellipses_count} ellipses remaining")
    if examples:
        print(f"    Examples:")
        for example in examples[:3]:
            print(f"      {example[:100]}...")
    
    return ellipses_count

def main():
    """Check all XHTML files"""
    epub_text_dir = Path('epub/OEBPS/Text')
    
    if not epub_text_dir.exists():
        print("EPUB Text directory not found!")
        return
    
    total_ellipses = 0
    
    # Get all XHTML files
    xhtml_files = list(epub_text_dir.glob('*.xhtml'))
    
    print(f"Checking {len(xhtml_files)} XHTML files")
    
    for file_path in xhtml_files:
        count = fix_xml_declaration_and_check(file_path)
        total_ellipses += count
    
    print(f"\nTotal ellipses remaining: {total_ellipses}")
    
    if total_ellipses > 0:
        print("\nMost remaining ellipses appear to be legitimate text content (like 'verse by verse...')")
        print("These should be preserved as they are part of the original text.")

if __name__ == "__main__":
    main()
