#!/usr/bin/env python3
"""
Update the content.opf file to include all image files
"""

import os
import re

def update_content_opf():
    # Read the current content.opf
    with open('epub/OEBPS/content.opf', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get list of images
    images_dir = 'epub/OEBPS/Images'
    image_files = []
    
    for file in os.listdir(images_dir):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg')):
            image_files.append(file)
    
    # Create image manifest items
    image_manifest_items = []
    for img in sorted(image_files):
        # Determine media type
        ext = img.lower().split('.')[-1]
        if ext in ['jpg', 'jpeg']:
            media_type = 'image/jpeg'
        elif ext == 'png':
            media_type = 'image/png'
        elif ext == 'gif':
            media_type = 'image/gif'
        elif ext == 'svg':
            media_type = 'image/svg+xml'
        else:
            continue
        
        # Create item ID from filename
        item_id = img.replace('.', '-').replace('-', '_').lower()
        
        image_manifest_items.append(
            f'        <item id="{item_id}" href="Images/{img}" media-type="{media_type}"/>'
        )
    
    # Find the position to insert image items (before the closing manifest tag)
    manifest_end = content.find('    </manifest>')
    if manifest_end != -1:
        # Insert image items before closing manifest tag
        insert_pos = manifest_end
        
        # Prepare the new image items text
        image_items_text = '\n        <!-- Images -->\n' + '\n'.join(image_manifest_items) + '\n        \n'
        
        # Insert the image items
        new_content = content[:insert_pos] + image_items_text + content[insert_pos:]
        
        # Write the updated content.opf
        with open('epub/OEBPS/content.opf', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added {len(image_files)} image files to manifest")
    else:
        print("Could not find manifest closing tag")

if __name__ == "__main__":
    update_content_opf()



