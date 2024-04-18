from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

def create_cover_page(fileName="CoverPage.pdf", poNumber="", vendorName="", customerName="", invoiceID="", invoiceTotal=""):
    # Create a new PDF file
    c = canvas.Canvas(fileName, pagesize=letter)

    # Get Current Time
    now = datetime.datetime.now()

    # Set font properties
    c.setFont("Courier-Bold", 18)  # Increased font size and bold for the header

    # Header: Midwest Hose and Specialty
    header_text = "Midwest Hose and Specialty"
    c.drawString(100, 700, header_text)

    # Date/time, PO Number, Vendor Name, Customer Name, Invoice ID, Invoice Total
    details = [
        ("Processed Date/time:", now.strftime("%m/%d/%Y, %H:%M:%S")),
        ("PO Number:", poNumber),
        ("Vendor Name:", vendorName),
        ("Customer Name:", customerName),
        ("Invoice ID:", invoiceID),
        ("Invoice Total:", invoiceTotal),
    ]

    # Draw the details
    y = 650
    for label, value in details:
        c.setFont("Courier", 12)  # Regular font size for details
        c.drawString(100, y, label)
        c.drawString(250, y, value)
        y -= 30

    # Save the PDF
    c.save()
    
    # return the filename so it can be used to merge with the original pdf. 
    return fileName


# output_pdf_file = "./CoverPages/cover_page.pdf"
# create_cover_page(fileName=output_pdf_file)
# print(f"Cover page saved as {output_pdf_file}")
