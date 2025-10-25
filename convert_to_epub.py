#!/usr/bin/env python3
"""
EPUB Conversion Script for Framing Jesus
Converts HTML files to EPUB-compatible XHTML format
"""

import os
import re
from bs4 import BeautifulSoup
import shutil

def convert_html_to_xhtml(html_file_path, output_dir):
    """Convert a single HTML file to EPUB-compatible XHTML"""
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract the title
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else "Chapter"
    
    # Extract the body content
    body = soup.find('body')
    if not body:
        return None
    
    # Clean up the content for EPUB
    # Remove navigation elements and external styles
    for nav in body.find_all(['div'], class_=['navigation']):
        nav.decompose()
    
    # Update image src paths
    for img in body.find_all('img'):
        src = img.get('src', '')
        if src.startswith('.') or not src.startswith('../'):
            # Update to proper EPUB image path
            img['src'] = f"../Images/{os.path.basename(src)}"
    
    # Create XHTML structure
    xhtml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
</head>
<body>
{str(body)}
</body>
</html>'''
    
    # Clean up the XHTML
    xhtml_content = re.sub(r' class="[^"]*"', '', xhtml_content)  # Remove classes that might not be in CSS
    xhtml_content = re.sub(r' style="[^"]*"', '', xhtml_content)  # Remove inline styles
    xhtml_content = xhtml_content.replace('&nbsp;', '&#160;')  # Fix entities
    
    # Get the filename for output
    filename = os.path.basename(html_file_path).replace('.html', '.xhtml')
    output_path = os.path.join(output_dir, filename)
    
    # Write the XHTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xhtml_content)
    
    return filename

def main():
    # Define paths
    epub_dir = "epub"
    oebps_dir = os.path.join(epub_dir, "OEBPS")
    text_dir = os.path.join(oebps_dir, "Text")
    images_dir = os.path.join(oebps_dir, "Images")
    
    # Files to process (in order)
    files_to_process = [
        "introduction.html",
        "part1.html", "chapter1.html", "chapter2.html", "chapter3.html",
        "part2.html", "chapter4.html", "chapter5.html",
        "part3.html", "chapter6.html", "chapter7.html", "chapter8.html",
        "part4.html", "chapter9.html", "chapter10.html",
        "conclusion.html",
        "appendix1.html", "appendix2.html"
    ]
    
    # Convert HTML files to XHTML
    for html_file in files_to_process:
        if os.path.exists(html_file):
            print(f"Converting {html_file}...")
            convert_html_to_xhtml(html_file, text_dir)
        else:
            print(f"Warning: {html_file} not found")
    
    # Copy images to EPUB Images directory
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            print(f"Copying image {file}...")
            shutil.copy2(file, images_dir)
    
    print("Conversion complete!")

if __name__ == "__main__":
    main()






