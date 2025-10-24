#!/usr/bin/env python3
"""
Fix corrupted ellipses in XHTML files
"""
import os
import re
from pathlib import Path

def fix_corrupted_ellipses(file_path):
    """Fix corrupted ellipses in a single file"""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count original ellipses
    original_count = content.count('...')
    
    # Fix common corrupted patterns
    replacements = [
        # CSS classes
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
        ('color', 'color'),  # This one might be corrupted too
        
        # Text content patterns
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
        
        # Common word patterns
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
        ('CE', 'CE'),
        ('BCE', 'BCE'),
        
        # Fix any remaining ellipses in CSS values
        ('#f0f4f8...0%', '#f0f4f8 0%'),
        ('#e6f0f7...100%', '#e6f0f7 100%'),
        ('135deg', '135deg'),
        ('0...5rem', '0.5rem'),
        ('1...5rem', '1.5rem'),
        ('2...5rem', '2.5rem'),
        ('4px...solid', '4px solid'),
        ('1px...solid', '1px solid'),
        ('2px...solid', '2px solid'),
        ('5px...solid', '5px solid'),
    ]
    
    # Apply replacements
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Fix any remaining ellipses in class names (generic pattern)
    content = re.sub(r'class="([^"]*?)\.\.\.([^"]*?)"', r'class="\1-\2"', content)
    
    # Fix any remaining ellipses in CSS properties
    content = re.sub(r'([a-zA-Z-]+)\.\.\.([a-zA-Z-]+):', r'\1-\2:', content)
    
    # Count remaining ellipses
    remaining_count = content.count('...')
    fixed_count = original_count - remaining_count
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Fixed {fixed_count} ellipses, {remaining_count} remaining")
    return fixed_count, remaining_count

def main():
    """Fix all XHTML files"""
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
        fixed, remaining = fix_corrupted_ellipses(file_path)
        total_fixed += fixed
        total_remaining += remaining
    
    print(f"\nSummary:")
    print(f"Total ellipses fixed: {total_fixed}")
    print(f"Total ellipses remaining: {total_remaining}")
    
    if total_remaining > 0:
        print(f"\nWarning: {total_remaining} ellipses still remain. Manual review may be needed.")
    else:
        print("\nAll ellipses have been fixed!")

if __name__ == "__main__":
    main()
