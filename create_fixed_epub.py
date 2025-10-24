#!/usr/bin/env python3
"""
Create properly formatted EPUB with correct mimetype handling
"""

import zipfile
import os

def create_epub_correct():
    epub_filename = "Framing_Jesus.epub"
    
    # Remove existing EPUB if it exists
    if os.path.exists(epub_filename):
        os.remove(epub_filename)
    
    print(f"Creating {epub_filename} with proper structure...")
    
    # Read mimetype content
    with open('epub/mimetype', 'r') as f:
        mimetype_content = f.read()
    
    with zipfile.ZipFile(epub_filename, 'w', zipfile.ZIP_DEFLATED) as epub:
        # CRITICAL: Add mimetype file first, uncompressed
        info = zipfile.ZipInfo(filename='mimetype')
        info.compress_type = zipfile.ZIP_STORED
        info.external_attr = 0o644 << 16  # Set file permissions
        epub.writestr(info, mimetype_content)
        
        # Add all other files
        for root, dirs, files in os.walk('epub'):
            for file in files:
                if file == 'mimetype':
                    continue  # Already added above
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, 'epub')
                
                # Ensure proper compression for all other files
                epub.write(file_path, rel_path, compress_type=zipfile.ZIP_DEFLATED)
    
    # Verify the mimetype was added first and uncompressed
    with zipfile.ZipFile(epub_filename, 'r') as epub:
        file_list = epub.namelist()
        if file_list[0] == 'mimetype':
            file_info = epub.getinfo('mimetype')
            if file_info.compress_type == zipfile.ZIP_STORED:
                print("✓ Mimetype file is first and uncompressed")
            else:
                print("✗ Mimetype file is compressed")
        else:
            print("✗ Mimetype file is not first")
    
    print(f"EPUB created: {epub_filename}")
    print(f"File size: {os.path.getsize(epub_filename) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    create_epub_correct()



