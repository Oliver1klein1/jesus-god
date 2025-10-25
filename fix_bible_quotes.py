#!/usr/bin/env python3
"""
Script to fix missing bible-quote classes in all EPUB chapter files.
"""

import os
import re

def fix_bible_quotes_in_chapters():
    """Find and fix div elements that should have bible-quote class but don't."""
    
    # Get all chapter files
    text_dir = 'epub/OEBPS/Text'
    chapter_files = [f for f in os.listdir(text_dir) if f.startswith('chapter') and f.endswith('.xhtml')]
    
    fixed_count = 0
    
    for chapter_file in sorted(chapter_files):
        file_path = os.path.join(text_dir, chapter_file)
        print(f"\nProcessing {chapter_file}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to find div elements that contain Bible verses but don't have bible-quote class
        # This looks for div elements that contain quoted text (inside quotes or with verse references)
        
        # Pattern 1: <div> followed by quoted text and references like (John 17:3)
        pattern1 = r'<div>\s*([^<]*"[^"]*"[^<]*\([^)]*\)[^<]*)</div>'
        
        # Pattern 2: <div> followed by text with quotes and no existing class
        pattern2 = r'<div>([^<]*"[^"]*"[^<]*)</div>'
        
        # Pattern 3: <div> with quoted text ending with verse references in parentheses
        pattern3 = r'<div>\s*([^<]*\([A-Za-z]+ [0-9]+:[0-9]+[^)]*\)[^<]*)</div>'
        
        # More comprehensive pattern to catch various Bible verse formats
        # Look for divs containing quoted text, verse references, or historical quotes
        patterns = [
            # Div with quoted text and verse reference
            r'<div>\s*([^<]*"[^"]*".*?\([^)]*[A-Z][a-z]+ [0-9]+:[0-9]+[^)]*\)[^<]*)</div>',
            # Div with verse reference in parentheses  
            r'<div>\s*([^<]*\([A-Z][a-z]+ [0-9]+:[0-9]+[^)]*\)[^<]*)</div>',
            # Div with quoted text (more general)
            r'<div>\s*([^<]*"[A-Z][^"]*"[^<]*)</div>',
            # Div with historical quotes or citations (e.g., Tertullian, Irenaeus)
            r'<div>\s*([^<]*— [A-Z][^<]*\)[^<]*)</div>',
        ]
        
        for pattern in patterns:
            def replace_bible_quote(match):
                div_content = match.group(1).strip()
                
                # Skip if already has bible-quote class
                if 'class="bible-quote"' in match.group(0):
                    return match.group(0)
                
                # Skip if it's an image or other non-text content
                if 'src=' in div_content or '<img' in div_content:
                    return match.group(0)
                
                # Skip if it's clearly not a verse (e.g., navigation, chapter numbers)
                if any(skip_word in div_content.lower() for skip_word in ['chapter', 'table of contents', 'copyright']):
                    return match.group(0)
                
                # Apply bible-quote class
                return f'<div class="bible-quote">\n{div_content}\n</div>'
            
            # Apply the replacement
            new_content = re.sub(pattern, replace_bible_quote, content, flags=re.MULTILINE | re.DOTALL)
            if new_content != content:
                content = new_content
                print(f"  Fixed pattern in {chapter_file}")
                fixed_count += 1
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated {chapter_file}")
    
    print(f"\nTotal files with changes: {fixed_count}")
    return fixed_count

if __name__ == "__main__":
    fix_bible_quotes_in_chapters()






