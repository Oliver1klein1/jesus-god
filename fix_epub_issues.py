#!/usr/bin/env python3
"""
Fix EPUB validation issues found by epubcheck
"""

import os
import re
import zipfile
from bs4 import BeautifulSoup

def fix_html_files():
    """Fix HTML/XHTML files to use proper EPUB3 format"""
    
    # List of XHTML files to fix
    xhtml_files = []
    text_dir = "epub/OEBPS/Text"
    
    for file in os.listdir(text_dir):
        if file.endswith('.xhtml'):
            xhtml_files.append(os.path.join(text_dir, file))
    
    for file_path in xhtml_files:
        print(f"Fixing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Fix DOCTYPE to HTML5 for EPUB3
        html_tag = soup.find('html')
        if html_tag:
            # Remove XHTML namespace if present and use HTML5 DOCTYPE
            new_content = content
            new_content = re.sub(
                r'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1\.1//EN" "http://www\.w3\.org/TR/xhtml11/DTD/xhtml11\.dtd">',
                '<!DOCTYPE html>',
                new_content
            )
            
            # Remove xmlns from html tag for HTML5
            new_content = re.sub(r'<html xmlns="http://www\.w3\.org/1999/xhtml">', '<html>', new_content)
            
            # Fix external links to use .xhtml instead of .html
            new_content = re.sub(r'\.html"', '.xhtml"', new_content)
            new_content = re.sub(r'\.html#', '.xhtml#', new_content)
            
            # Fix br tags in lists - replace with proper list structure
            new_content = re.sub(r'<br\s*/?>\s*</li>', '</li>', new_content)
            
            # Write the fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

def fix_content_opf():
    """Fix content.opf metadata issues"""
    
    opf_path = "epub/OEBPS/content.opf"
    
    with open(opf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix metadata issues
    # Remove invalid title-type property that doesn't refine properly
    content = re.sub(r'<meta property="title-type">main</meta>\n', '', content)
    
    # Fix duplicate cover-image reference
    content = re.sub(
        r'<item id="cover-image" href="Images/framing-jesus-cover\.jpg" media-type="image/jpeg" properties="cover-image"/>',
        '<item id="cover-image" href="Images/framing-jesus-cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
        content
    )
    
    # Remove the duplicate entry that's causing the error
    lines = content.split('\n')
    fixed_lines = []
    cover_image_added = False
    
    for line in lines:
        if 'framing-jesus-cover.jpg' in line and 'cover-image' in line:
            if not cover_image_added:
                fixed_lines.append(line)
                cover_image_added = True
            # Skip duplicate entries
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Fix invalid XML names (remove colons and spaces)
    content = re.sub(r'id="([^"]*b4[^"]*)"', r'id="b4-mum-daughter-jpg"', content)
    content = re.sub(r'href="Images/b4 mum-daughter\.jpg"', r'href="Images/b4-mum-daughter.jpg"', content)
    
    with open(opf_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_image_filename():
    """Fix the problematic image filename with spaces"""
    
    old_path = "epub/OEBPS/Images/b4 mum-daughter.jpg"
    new_path = "epub/OEBPS/Images/b4-mum-daughter.jpg"
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")

def fix_nav_xhtml():
    """Fix navigation XHTML file"""
    
    nav_path = "epub/OEBPS/nav.xhtml"
    
    with open(nav_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix DOCTYPE and namespace
    content = re.sub(
        r'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1\.1//EN" "http://www\.w3\.org/TR/xhtml11/DTD/xhtml11\.dtd">',
        '<!DOCTYPE html>',
        content
    )
    
    content = re.sub(r'<html xmlns="http://www\.w3\.org/1999/xhtml" xmlns:epub="http://www\.idpf\.org/2007/ops">', 
                    '<html xmlns:epub="http://www.idpf.org/2007/ops">', content)
    
    with open(nav_path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_fixed_epub():
    """Create a new EPUB with proper mimetype handling"""
    
    epub_filename = "Framing_Jesus_Fixed.epub"
    
    # Remove existing EPUB if it exists
    if os.path.exists(epub_filename):
        os.remove(epub_filename)
    
    print(f"Creating fixed {epub_filename}...")
    
    with zipfile.ZipFile(epub_filename, 'w', zipfile.ZIP_DEFLATED) as epub:
        # First, add mimetype file uncompressed (critical for EPUB)
        mimetype_path = 'epub/mimetype'
        if os.path.exists(mimetype_path):
            # Add mimetype first and uncompressed
            epub.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
        
        # Add all other files with compression
        for root, dirs, files in os.walk('epub'):
            for file in files:
                if file == 'mimetype':
                    continue  # Already added above
                
                file_path = os.path.join(root, file)
                # Calculate relative path within epub
                rel_path = os.path.relpath(file_path, 'epub')
                epub.write(file_path, rel_path, compress_type=zipfile.ZIP_DEFLATED)
    
    print(f"Fixed EPUB created: {epub_filename}")

def main():
    print("Fixing EPUB validation issues...")
    
    # Fix the issues in order
    fix_image_filename()
    print("Fixed image filename")
    
    fix_html_files()
    print("Fixed HTML/XHTML files")
    
    fix_content_opf()
    print("Fixed content.opf metadata")
    
    fix_nav_xhtml()
    print("Fixed navigation file")
    
    create_fixed_epub()
    print("Created fixed EPUB file")

if __name__ == "__main__":
    main()



