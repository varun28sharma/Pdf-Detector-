from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime, timedelta
import os

def add_authentic_metadata(input_pdf_path, output_pdf_path=None):
    """
    Add authentic-looking metadata to a PDF file.
    """
    if output_pdf_path is None:
        # Create output filename by adding '_authentic' before the extension
        base, ext = os.path.splitext(input_pdf_path)
        output_pdf_path = f"{base}_authentic{ext}"

    # Read the PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Copy all pages
    for page in reader.pages:
        writer.add_page(page)

    # Create authentic-looking metadata
    creation_date = datetime.now() - timedelta(days=7)  # Created 7 days ago
    modification_date = datetime.now() - timedelta(days=1)  # Modified 1 day ago

    # Format dates in PDF format
    def format_pdf_date(date):
        return f"D:{date.strftime('%Y%m%d%H%M%S')}+00'00'"

    # Add metadata
    metadata = {
        "/Title": "Original Document",
        "/Author": "Microsoft Word",
        "/Subject": "Business Document",
        "/Keywords": "business, document, report",
        "/Creator": "Microsoft Word",
        "/Producer": "Microsoft Word 2016",
        "/CreationDate": format_pdf_date(creation_date),
        "/ModDate": format_pdf_date(modification_date),
        "/Trapped": "/False",
        "/GTS_PDFXVersion": "PDF/X-1:2001",
        "/Company": "Business Corp",
        "/Category": "Business",
        "/DocSecurity": "0",
        "/NumPages": str(len(reader.pages)),
        "/PageSize": "A4",
        "/PageLayout": "/SinglePage"
    }

    # Add metadata to the PDF
    writer.add_metadata(metadata)

    # Save the new PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

    print(f"Created new PDF with authentic metadata: {output_pdf_path}")
    return output_pdf_path

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python add_metadata.py <input_pdf_path> [output_pdf_path]")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        add_authentic_metadata(input_pdf, output_pdf)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1) 