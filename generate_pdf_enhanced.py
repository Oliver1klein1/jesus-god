#!/usr/bin/env python3
"""
Enhanced PDF Generation Script for Book Publishing
Creates high-quality PDFs from HTML files with proper print styling
"""

import os
import subprocess
import webbrowser
import tempfile
from pathlib import Path

def create_print_css():
    """Create comprehensive print CSS for PDF generation"""
    print_css = """
/* Enhanced Print CSS for Book Publishing */
@media print {
    /* Page setup - 16x9 inch landscape */
    @page {
        size: 16in 9in;
        margin: 1in;
    }
    
    /* Base styles */
    body {
        font-family: Georgia, 'Times New Roman', Times, serif;
        font-size: 12pt;
        line-height: 1.6;
        color: #000;
        background: #fff;
        margin: 0;
        padding: 0;
    }
    
    /* Hide all navigation elements */
    .navigation,
    .nav-link,
    nav,
    .navbar,
    .menu,
    .breadcrumb,
    .pagination,
    [class*="nav"],
    [class*="menu"],
    [class*="breadcrumb"] {
        display: none !important;
    }
    
    /* Preserve bible-quote styling */
    .bible-quote {
        font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
        font-style: italic;
        color: #2c5282;
        background: #f0f4f8;
        border-left: 4px solid #4299e1;
        padding: 1.2rem 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0 0.5rem 0.5rem 0;
        page-break-inside: avoid;
        box-shadow: none;
    }
    
    /* Preserve highlight and callout styling */
    .highlight,
    .callout,
    .emphasis {
        page-break-inside: avoid;
        margin: 1rem 0;
        background: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #007bff;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
        page-break-inside: avoid;
        color: #2d3748;
        font-weight: bold;
    }
    
    h1 {
        font-size: 18pt;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    h2 {
        font-size: 16pt;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    h3 {
        font-size: 14pt;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    p, li {
        page-break-inside: avoid;
        orphans: 3;
        widows: 3;
        margin-bottom: 0.5rem;
        text-align: justify;
    }
    
    /* Images */
    img {
        max-width: 100% !important;
        height: auto !important;
        page-break-inside: avoid;
        display: block;
        margin: 1rem auto;
    }
    
    /* Page breaks */
    .page-break {
        page-break-before: always;
    }
    
    .no-break {
        page-break-inside: avoid;
    }
    
    .chapter {
        page-break-before: always;
    }
    
    /* Tables */
    table {
        page-break-inside: avoid;
        border-collapse: collapse;
        width: 100%;
        margin: 1rem 0;
    }
    
    th, td {
        border: 1px solid #000;
        padding: 0.5rem;
        text-align: left;
    }
    
    th {
        background-color: #f8f9fa;
        font-weight: bold;
    }
    
    /* Lists */
    ul, ol {
        page-break-inside: avoid;
        margin: 1rem 0;
    }
    
    li {
        margin-bottom: 0.25rem;
    }
    
    /* Links */
    a {
        color: #000;
        text-decoration: none;
    }
    
    a[href]:after {
        content: " (" attr(href) ")";
        font-size: 10pt;
        color: #666;
    }
    
    /* Hide elements that shouldn't print */
    .no-print,
    .screen-only,
    .print-hidden {
        display: none !important;
    }
    
    /* Preserve inline styles */
    [style] {
        /* Inline styles are preserved by default */
    }
    
    /* Container adjustments */
    .container {
        max-width: none;
        margin: 0;
        padding: 0;
        background: transparent;
        box-shadow: none;
    }
    
    /* Drop caps */
    .drop-cap {
        float: left;
        font-size: 3em;
        line-height: 0.8;
        margin: 0.1em 0.1em 0 0;
        font-weight: bold;
    }
    
    /* Blockquotes */
    blockquote {
        margin: 1rem 0;
        padding: 1rem;
        border-left: 4px solid #ccc;
        background: #f9f9f9;
        page-break-inside: avoid;
    }
    
    /* Code blocks */
    pre, code {
        font-family: 'Courier New', monospace;
        background: #f4f4f4;
        padding: 0.5rem;
        border-radius: 3px;
        page-break-inside: avoid;
    }
    
    /* Ensure proper spacing */
    .spacing {
        margin: 1rem 0;
    }
    
    /* Footer and header */
    @page {
        @bottom-center {
            content: counter(page);
            font-size: 10pt;
        }
    }
}
"""
    return print_css

def inject_print_css(html_file_path):
    """Inject print CSS into HTML file"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if print CSS already exists
    if '@media print' in content:
        print(f"Print CSS already exists in {html_file_path}")
        return content
    
    # Find the closing </head> tag and inject print CSS before it
    head_end = content.find('</head>')
    if head_end == -1:
        print(f"Warning: No </head> tag found in {html_file_path}")
        return content
    
    print_css = create_print_css()
    css_injection = f"""
    <style>
    {print_css}
    </style>
    """
    
    new_content = content[:head_end] + css_injection + content[head_end:]
    return new_content

def generate_pdf_with_puppeteer(html_file, output_file):
    """Generate PDF using Puppeteer (Node.js)"""
    puppeteer_script = f"""
const puppeteer = require('puppeteer');
const path = require('path');

async function generatePDF() {{
    const browser = await puppeteer.launch({{ headless: true }});
    const page = await browser.newPage();
    
    const htmlPath = path.resolve('{html_file}');
    await page.goto(`file://${{htmlPath}}`, {{ waitUntil: 'networkidle0' }});
    
    await page.pdf({{
        path: '{output_file}',
        format: 'A4',
        printBackground: true,
        margin: {{
            top: '1in',
            right: '1in',
            bottom: '1in',
            left: '1in'
        }},
        displayHeaderFooter: true,
        headerTemplate: '<div></div>',
        footerTemplate: '<div style="font-size: 10px; text-align: center; width: 100%;"><span class="pageNumber"></span></div>'
    }});
    
    await browser.close();
    console.log('PDF generated successfully');
}}

generatePDF().catch(console.error);
"""
    
    # Write temporary script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(puppeteer_script)
        script_path = f.name
    
    try:
        # Run Puppeteer script
        result = subprocess.run(['node', script_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"PDF generated successfully: {output_file}")
            return True
        else:
            print(f"Error generating PDF: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Node.js not found. Please install Node.js and Puppeteer.")
        return False
    finally:
        os.unlink(script_path)

def generate_pdf_with_wkhtmltopdf(html_file, output_file):
    """Generate PDF using wkhtmltopdf"""
    try:
        cmd = [
            'wkhtmltopdf',
            '--page-size', 'A4',
            '--margin-top', '1in',
            '--margin-right', '1in',
            '--margin-bottom', '1in',
            '--margin-left', '1in',
            '--print-media-type',
            '--enable-local-file-access',
            '--load-error-handling', 'ignore',
            html_file,
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"PDF generated successfully: {output_file}")
            return True
        else:
            print(f"Error generating PDF: {result.stderr}")
            return False
    except FileNotFoundError:
        print("wkhtmltopdf not found. Please install wkhtmltopdf.")
        return False

def generate_pdf_with_browser(html_file, output_file):
    """Generate PDF using browser print functionality"""
    print(f"Opening {html_file} in browser for manual PDF generation...")
    print("Please use Ctrl+P to print and save as PDF.")
    print(f"Save as: {output_file}")
    
    # Open HTML file in default browser
    webbrowser.open(f'file://{os.path.abspath(html_file)}')
    
    input("Press Enter after you've saved the PDF...")
    return os.path.exists(output_file)

def main():
    """Main PDF generation function"""
    print("🖨️ Enhanced PDF Generation for Book Publishing")
    print("=" * 50)
    
    # Get HTML file from user
    html_file = input("Enter HTML file path (or press Enter for index.html): ").strip()
    if not html_file:
        html_file = "index.html"
    
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found")
        return
    
    # Get output file name
    base_name = os.path.splitext(html_file)[0]
    output_file = f"{base_name}_print.pdf"
    
    print(f"Input file: {html_file}")
    print(f"Output file: {output_file}")
    
    # Inject print CSS
    print("\n📝 Injecting print CSS...")
    html_content = inject_print_css(html_file)
    
    # Create temporary HTML file with print CSS
    temp_html = f"{base_name}_print_temp.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Temporary HTML file created: {temp_html}")
    
    # Choose PDF generation method
    print("\n🔧 Choose PDF generation method:")
    print("1. Puppeteer (Node.js) - Recommended")
    print("2. wkhtmltopdf - Alternative")
    print("3. Browser print - Manual")
    
    choice = input("Enter choice (1-3): ").strip()
    
    success = False
    
    if choice == "1":
        print("\n🚀 Generating PDF with Puppeteer...")
        success = generate_pdf_with_puppeteer(temp_html, output_file)
    elif choice == "2":
        print("\n🚀 Generating PDF with wkhtmltopdf...")
        success = generate_pdf_with_wkhtmltopdf(temp_html, output_file)
    elif choice == "3":
        print("\n🚀 Opening browser for manual PDF generation...")
        success = generate_pdf_with_browser(temp_html, output_file)
    else:
        print("Invalid choice. Using browser method...")
        success = generate_pdf_with_browser(temp_html, output_file)
    
    # Clean up temporary file
    if os.path.exists(temp_html):
        os.remove(temp_html)
        print(f"Cleaned up temporary file: {temp_html}")
    
    if success:
        print(f"\n✅ PDF generated successfully: {output_file}")
        print("\n📋 Quality Checklist:")
        print("□ All styling preserved")
        print("□ Navigation elements hidden")
        print("□ Page breaks appropriate")
        print("□ Images display correctly")
        print("□ Text is readable")
        print("□ Bible quotes styled properly")
    else:
        print("\n❌ PDF generation failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
