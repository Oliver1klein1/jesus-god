#!/usr/bin/env python3
"""
Create EPUB file for Framing Jesus
"""
import zipfile
import os
from pathlib import Path

def create_epub():
    """Create the EPUB file"""
    epub_path = "framing-jesus.epub"
    
    # Remove existing EPUB if it exists
    if os.path.exists(epub_path):
        os.remove(epub_path)
    
    # Create EPUB file
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as epub:
        # Add mimetype first (must be uncompressed)
        epub.write('epub/mimetype', 'mimetype', compress_type=zipfile.ZIP_STORED)
        
        # Add all other files
        epub_dir = Path('epub')
        for file_path in epub_dir.rglob('*'):
            if file_path.is_file() and file_path.name != 'mimetype':
                arcname = str(file_path.relative_to(epub_dir))
                epub.write(file_path, arcname)
    
    print(f"EPUB created: {epub_path}")
    return epub_path

if __name__ == "__main__":
    create_epub()
