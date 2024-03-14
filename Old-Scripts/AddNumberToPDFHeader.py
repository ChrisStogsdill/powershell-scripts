from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText
import os
import boto3
import json



#create a Textract Client
textract = boto3.client('textract')

sourcePDF = "Invoice ID  223948.pdf"

response = None

with open(sourcePDF, "rb") as document:
    imageBytes = bytearray(document.read())

# Call Textract AnalyzeDocument by passing a document from local disk
response = textract.analyze_document(
    Document={'Bytes': imageBytes},
    FeatureTypes=["QUERIES"],
    QueriesConfig={
        "Queries": [{
            "Text": "What is the PO number",
            "Alias": "PONumber"
        }]
    })






# Fill the writer with the pages you want
cwd = os.getcwd()
pdf_path = os.path.join(cwd, "Invoice ID  223948.pdf")
reader = PdfReader(pdf_path)
page = reader.pages[0]
writer = PdfWriter()
writer.add_page(page)

# Create the annotation and add it
annotation = FreeText(
    text="Extracted PO number: 12345",
    rect=(5, 5, 200, 20),
    font="Arial",
    bold=True,
    font_size="20pt",
    font_color="000000",
)
writer.add_annotation(page_number=0, annotation=annotation)

# Write the annotated file to disk
with open("annotated-pdf.pdf", "wb") as fp:
    writer.write(fp)