#!/usr/bin/env python3
"""
Copy missing images to EPUB Images folder
"""
import os
import shutil
from pathlib import Path

def copy_missing_images():
    """Copy all missing images to EPUB Images folder"""
    epub_images_dir = Path('epub/OEBPS/Images')
    main_dir = Path('.')
    
    # Get list of all JPG files in main directory
    main_images = set(f.name for f in main_dir.glob('*.jpg'))
    
    # Get list of all JPG files in EPUB Images directory
    epub_images = set(f.name for f in epub_images_dir.glob('*.jpg'))
    
    # Find missing images
    missing_images = main_images - epub_images
    
    print(f"Found {len(missing_images)} missing images:")
    for img in sorted(missing_images):
        print(f"  {img}")
    
    # Copy missing images
    copied_count = 0
    for img in missing_images:
        src = main_dir / img
        dst = epub_images_dir / img
        try:
            shutil.copy2(src, dst)
            print(f"Copied: {img}")
            copied_count += 1
        except Exception as e:
            print(f"Failed to copy {img}: {e}")
    
    print(f"\nCopied {copied_count} images to EPUB Images folder")

if __name__ == "__main__":
    copy_missing_images()
