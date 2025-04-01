from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

def create_test_pdf(is_original=True):
    # Create a PDF with some content
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, 750, "This is a test PDF file")
    can.drawString(100, 700, "Created for testing PDF integrity analysis")
    can.save()
    packet.seek(0)
    
    # Create a new PDF with the content
    new_pdf = PdfWriter()
    new_pdf.add_page(PdfReader(packet).pages[0])
    
    # Add metadata with proper PDF date format
    creation_date = datetime.now().strftime("D:%Y%m%d%H%M%S+00'00'")
    if is_original:
        # Original document metadata
        new_pdf.add_metadata({
            "/Title": "Test PDF Document",
            "/Author": "Original Author",
            "/Subject": "Test Document",
            "/Keywords": "test, pdf, integrity",
            "/Creator": "PDF Test Creator",
            "/Producer": "Test PDF Producer",
            "/CreationDate": creation_date,
            "/ModDate": creation_date
        })
    else:
        # Modified document metadata
        new_pdf.add_metadata({
            "/Title": "Modified Test Document",
            "/Author": "Modified Author",
            "/Subject": "Modified Test Document",
            "/Keywords": "test, pdf, modified",
            "/Creator": "Adobe Acrobat",  # Suspicious editor
            "/Producer": "PDF Editor Tool",  # Suspicious editor
            "/CreationDate": creation_date,
            "/ModDate": datetime.now().strftime("D:%Y%m%d%H%M%S+00'00'")  # Different modification date
        })
    
    # Write the PDF to a file
    filename = "original.pdf" if is_original else "modified.pdf"
    with open(filename, "wb") as output_file:
        new_pdf.write(output_file)
    return filename

if __name__ == "__main__":
    # Create both original and modified versions
    original_file = create_test_pdf(True)
    modified_file = create_test_pdf(False)
    print(f"Created {original_file} and {modified_file} for testing") 