#!/usr/bin/env python3
"""
Enhanced fix for corrupted ellipses in XHTML files
"""
import os
import re
from pathlib import Path

def fix_corrupted_ellipses_enhanced(file_path):
    """Fix corrupted ellipses in a single file with enhanced patterns"""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count original ellipses
    original_count = content.count('...')
    
    # Enhanced regex patterns for more complex cases
    patterns = [
        # Fix ellipses in class names
        (r'class="([^"]*?)\.\.\.([^"]*?)"', r'class="\1-\2"'),
        (r'class="([^"]*?)\.\.\.([^"]*?)\.\.\.([^"]*?)"', r'class="\1-\2-\3"'),
        
        # Fix ellipses in CSS properties
        (r'([a-zA-Z-]+)\.\.\.([a-zA-Z-]+):', r'\1-\2:'),
        (r'([a-zA-Z-]+)\.\.\.([a-zA-Z-]+)\.\.\.([a-zA-Z-]+):', r'\1-\2-\3:'),
        
        # Fix ellipses in CSS values
        (r'([a-zA-Z-]+)\.\.\.([a-zA-Z-]+)\s*;', r'\1-\2;'),
        (r'([a-zA-Z-]+)\.\.\.([a-zA-Z-]+)\s*\)', r'\1-\2)'),
        (r'([a-zA-Z-]+)\.\.\.([a-zA-Z-]+)\s*"', r'\1-\2"'),
        
        # Fix ellipses in text content (common patterns)
        (r'([A-Za-z]+)\.\.\.([A-Za-z]+)', r'\1-\2'),
        
        # Fix ellipses in dates and numbers
        (r'c\.\.\.(\d+)', r'c. \1'),
        (r'(\d+)\.\.\.(\d+)', r'\1-\2'),
        (r'AD\.\.\.(\d+)', r'AD \1'),
        
        # Fix ellipses in CSS gradients and values
        (r'(\d+)\.\.\.(\d+)px', r'\1-\2px'),
        (r'(\d+)\.\.\.(\d+)rem', r'\1-\2rem'),
        (r'(\d+)\.\.\.(\d+)em', r'\1-\2em'),
        (r'(\d+)\.\.\.(\d+)deg', r'\1-\2deg'),
        
        # Fix ellipses in color values
        (r'#([a-fA-F0-9]+)\.\.\.([a-fA-F0-9]+)', r'#\1-\2'),
        
        # Fix ellipses in URLs and paths
        (r'src="([^"]*?)\.\.\.([^"]*?)"', r'src="\1-\2"'),
        (r'href="([^"]*?)\.\.\.([^"]*?)"', r'href="\1-\2"'),
    ]
    
    # Apply regex patterns
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Additional specific replacements for common corrupted patterns
    specific_replacements = [
        # CSS classes that might have been missed
        ('scripture...card', 'scripture-card'),
        ('chapter...card', 'chapter-card'),
        ('mb...4', 'mb-4'),
        ('mb...8', 'mb-8'),
        ('px...4', 'px-4'),
        ('px...8', 'px-8'),
        ('mx...auto', 'mx-auto'),
        ('drop...cap', 'drop-cap'),
        ('list...disc', 'list-disc'),
        ('list...decimal', 'list-decimal'),
        ('pl...8', 'pl-8'),
        ('mt...12', 'mt-12'),
        ('py...8', 'py-8'),
        ('text...center', 'text-center'),
        ('text...gray-600', 'text-gray-600'),
        ('border...t', 'border-t'),
        ('border...gray-200', 'border-gray-200'),
        
        # CSS properties
        ('margin...top', 'margin-top'),
        ('margin...bottom', 'margin-bottom'),
        ('margin...left', 'margin-left'),
        ('margin...right', 'margin-right'),
        ('padding...top', 'padding-top'),
        ('padding...bottom', 'padding-bottom'),
        ('padding...left', 'padding-left'),
        ('padding...right', 'padding-right'),
        ('border...left', 'border-left'),
        ('border...right', 'border-right'),
        ('border...top', 'border-top'),
        ('border...bottom', 'border-bottom'),
        ('border...radius', 'border-radius'),
        ('linear...gradient', 'linear-gradient'),
        ('box...shadow', 'box-shadow'),
        ('text...align', 'text-align'),
        ('font...size', 'font-size'),
        ('font...weight', 'font-weight'),
        ('line...height', 'line-height'),
        ('background...color', 'background-color'),
        
        # Text content
        ('Father...Creator', 'Father-Creator'),
        ('Father...only...as...Creator', 'Father-only-as-Creator'),
        ('Greco...Roman', 'Greco-Roman'),
        ('time...lapse', 'time-lapse'),
        ('crystal...clear', 'crystal-clear'),
        ('shadow...filled', 'shadow-filled'),
        ('climate...controlled', 'climate-controlled'),
        ('non...negotiable', 'non-negotiable'),
        ('Pseudo...Clementine', 'Pseudo-Clementine'),
        ('third...century', 'third-century'),
        ('mid...third...century', 'mid-third-century'),
        ('real...time', 'real-time'),
        ('forensic...detail', 'forensic-detail'),
        ('textual...criticism', 'textual-criticism'),
        ('theological...realignment', 'theological-realignment'),
        ('manuscript...variants', 'manuscript-variants'),
        ('biblical...manuscripts', 'biblical-manuscripts'),
        ('early...Christianity', 'early-Christianity'),
        ('Council...of...Nicaea', 'Council-of-Nicaea'),
        ('Trinity...origins', 'Trinity-origins'),
        ('Jesus...vs...Paul', 'Jesus-vs-Paul'),
        ('Bible...changes', 'Bible-changes'),
        ('historical...Jesus', 'historical-Jesus'),
        
        # Dates and numbers
        ('c...100', 'c. 100'),
        ('c...150', 'c. 150'),
        ('c...155', 'c. 155'),
        ('c...170', 'c. 170'),
        ('c...180', 'c. 180'),
        ('c...202', 'c. 202'),
        ('c...215', 'c. 215'),
        ('c...220', 'c. 220'),
        ('AD...144', 'AD 144'),
        ('AD...150', 'AD 150'),
        
        # CSS values
        ('#f0f4f8...0%', '#f0f4f8 0%'),
        ('#e6f0f7...100%', '#e6f0f7 100%'),
        ('0...5rem', '0.5rem'),
        ('1...5rem', '1.5rem'),
        ('2...5rem', '2.5rem'),
        ('4px...solid', '4px solid'),
        ('1px...solid', '1px solid'),
        ('2px...solid', '2px solid'),
        ('5px...solid', '5px solid'),
    ]
    
    # Apply specific replacements
    for old, new in specific_replacements:
        content = content.replace(old, new)
    
    # Count remaining ellipses
    remaining_count = content.count('...')
    fixed_count = original_count - remaining_count
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Fixed {fixed_count} ellipses, {remaining_count} remaining")
    return fixed_count, remaining_count

def main():
    """Fix all XHTML files with enhanced patterns"""
    epub_text_dir = Path('epub/OEBPS/Text')
    
    if not epub_text_dir.exists():
        print("EPUB Text directory not found!")
        return
    
    total_fixed = 0
    total_remaining = 0
    
    # Get all XHTML files
    xhtml_files = list(epub_text_dir.glob('*.xhtml'))
    
    print(f"Found {len(xhtml_files)} XHTML files to fix")
    
    for file_path in xhtml_files:
        fixed, remaining = fix_corrupted_ellipses_enhanced(file_path)
        total_fixed += fixed
        total_remaining += remaining
    
    print(f"\nSummary:")
    print(f"Total ellipses fixed: {total_fixed}")
    print(f"Total ellipses remaining: {total_remaining}")
    
    if total_remaining > 0:
        print(f"\nWarning: {total_remaining} ellipses still remain. Manual review may be needed.")
        print("Files with remaining ellipses:")
        for file_path in xhtml_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            count = content.count('...')
            if count > 0:
                print(f"  {file_path.name}: {count} ellipses")
    else:
        print("\nAll ellipses have been fixed!")

if __name__ == "__main__":
    main()
