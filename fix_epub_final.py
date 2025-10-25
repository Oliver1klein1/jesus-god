#!/usr/bin/env python3
"""
Final fix for remaining EPUB validation issues
"""

import os
import re

def fix_xhtml_files():
    """Fix XHTML files to use proper EPUB3 XHTML format"""
    
    # List of XHTML files to fix
    text_dir = "epub/OEBPS/Text"
    nav_file = "epub/OEBPS/nav.xhtml"
    
    files_to_fix = []
    
    # Add all XHTML files in Text directory
    if os.path.exists(text_dir):
        for file in os.listdir(text_dir):
            if file.endswith('.xhtml'):
                files_to_fix.append(os.path.join(text_dir, file))
    
    # Add nav.xhtml
    if os.path.exists(nav_file):
        files_to_fix.append(nav_file)
    
    for file_path in files_to_fix:
        print(f"Fixing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix DOCTYPE back to proper XHTML for EPUB
        content = re.sub(
            r'<!DOCTYPE html>',
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
            content
        )
        
        # Fix HTML tag with proper XHTML namespace
        if 'xmlns=' not in content and '<html>' in content:
            content = re.sub(r'<html>', '<html xmlns="http://www.w3.org/1999/xhtml">', content)
        
        # Fix the fatal error in part3.xhtml with ampersand
        content = content.replace('& BEGOTTEN SONS', '&amp; BEGOTTEN SONS')
        content = content.replace('VIRGINS &', 'VIRGINS &amp;')
        
        # Fix any other unescaped ampersands in text content
        # But be careful not to break existing entities
        content = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', content)
        
        # Fix duplicate body tags
        content = re.sub(r'<body>\s*<body>', '<body>', content)
        
        # Fix any remaining .html references to .xhtml
        content = re.sub(r'\.html"', '.xhtml"', content)
        content = re.sub(r'\.html#', '.xhtml#', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def fix_content_opf_duplicate():
    """Fix the duplicate manifest entry for cover image"""
    
    opf_path = "epub/OEBPS/content.opf"
    
    with open(opf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and remove duplicate cover-image entries
    lines = content.split('\n')
    fixed_lines = []
    cover_image_count = 0
    
    for line in lines:
        if 'framing-jesus-cover.jpg' in line and 'cover-image' in line:
            cover_image_count += 1
            if cover_image_count == 1:
                fixed_lines.append(line)  # Keep first occurrence
            # Skip subsequent duplicates
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    with open(opf_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_mimetype_file():
    """Ensure mimetype file contains only the required string"""
    
    mimetype_path = "epub/mimetype"
    
    with open(mimetype_path, 'w') as f:
        f.write('application/epub+zip')
    
    print("Fixed mimetype file content")

def main():
    print("Applying final EPUB fixes...")
    
    fix_xhtml_files()
    print("Fixed XHTML files with proper EPUB format")
    
    fix_content_opf_duplicate()
    print("Fixed duplicate manifest entries")
    
    fix_mimetype_file()
    print("Fixed mimetype file content")

if __name__ == "__main__":
    main()






