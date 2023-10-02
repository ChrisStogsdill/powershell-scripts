from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText
import os
import boto3
import json
import trp
import sys


def get_text_from_pdf(pdf_path):
    extractedPONumber = ''
    #create a Textract Client
    textract = boto3.client('textract')

    response = None

    with open(pdf_path, "rb") as document:
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

    # Get the query result out of the json response
    
    for item in response['Blocks']:
        if item['BlockType'] == 'QUERY_RESULT':
            extractedPONumber = item['Text']

    # return the PO number to be used in another script
    return extractedPONumber


def add_annotation_to_pdf(pdf_path, annotationText):
    # Create a PdfReader and a writer
    # Create the annotation and add it
    # Write the annotated file to disk

    # Fill the writer with the pages you want
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    writer = PdfWriter()
    writer.add_page(page)

    # Create the annotation and add it
    annotation = FreeText(
        text=f"Extracted PO number: {annotationText}",
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

PONumber = get_text_from_pdf(sys.argv[1])
add_annotation_to_pdf(sys.argv[1], PONumber)