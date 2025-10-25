#!/usr/bin/env python3
"""
EPUB Creation Template Script
Copy this script to new book projects for final EPUB creation
"""

import zipfile
import os
import shutil

def create_epub():
    # Remove existing EPUB if it exists
    if os.path.exists("Your_Book_Name_Final.epub"):  # CUSTOMIZE THIS
        os.remove("Your_Book_Name_Final.epub")
    
    # Create EPUB file
    with zipfile.ZipFile("Your_Book_Name_Final.epub", 'w', zipfile.ZIP_DEFLATED) as epub:  # CUSTOMIZE THIS
        
        # Add mimetype first, uncompressed (EPUB requirement)
        epub.write("epub/mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF directory
        for root, dirs, files in os.walk("epub/META-INF"):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, "epub")
                epub.write(file_path, arc_path)
        
        # Add OEBPS directory
        for root, dirs, files in os.walk("epub/OEBPS"):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, "epub")
                epub.write(file_path, arc_path)
    
    print("EPUB created successfully: Your_Book_Name_Final.epub")  # CUSTOMIZE THIS
    
    # Verify the structure
    print("\nVerifying EPUB structure...")
    with zipfile.ZipFile("Your_Book_Name_Final.epub", 'r') as epub:  # CUSTOMIZE THIS
        file_list = epub.namelist()
        
        # Check that mimetype is first
        if file_list[0] == "mimetype":
            print("✓ mimetype file is first (EPUB requirement met)")
        else:
            print("✗ mimetype file is not first")
        
        # Check for required files
        required_files = [
            "mimetype",
            "META-INF/container.xml",
            "OEBPS/content.opf",
            "OEBPS/nav.xhtml",
            "OEBPS/toc.ncx",
            "OEBPS/Styles/style.css",
            "OEBPS/Images/framing-jesus-cover.jpg"  # CUSTOMIZE THIS
        ]
        
        for req_file in required_files:
            if req_file in file_list:
                print(f"✓ {req_file}")
            else:
                print(f"✗ {req_file} - MISSING")
        
        print(f"\nTotal files in EPUB: {len(file_list)}")
        
        # Show first 10 files to verify order
        print("\nFirst 10 files in EPUB:")
        for i, file in enumerate(file_list[:10]):
            print(f"{i+1}. {file}")

if __name__ == "__main__":
    create_epub()
