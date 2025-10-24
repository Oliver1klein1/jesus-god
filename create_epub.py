#!/usr/bin/env python3
"""
Create EPUB file with proper structure for Amazon KDP
"""

import zipfile
import os

def create_epub():
    epub_filename = "Framing_Jesus.epub"
    
    # Remove existing EPUB if it exists
    if os.path.exists(epub_filename):
        os.remove(epub_filename)
    
    print(f"Creating {epub_filename}...")
    
    with zipfile.ZipFile(epub_filename, 'w', zipfile.ZIP_STORED) as epub:
        # First, add mimetype file (must be first and uncompressed)
        epub.write('epub/mimetype', 'mimetype')
        
        # Add all other files with compression
        for root, dirs, files in os.walk('epub'):
            for file in files:
                if file == 'mimetype':
                    continue  # Already added above
                
                file_path = os.path.join(root, file)
                # Calculate relative path within epub
                rel_path = os.path.relpath(file_path, 'epub')
                epub.write(file_path, rel_path)
    
    print(f"EPUB created successfully: {epub_filename}")
    print(f"File size: {os.path.getsize(epub_filename) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    create_epub()



