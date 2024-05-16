from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText
import os
import boto3
import json



#create a Textract Client
textract = boto3.client('textract')

sourcePDF = r"M:\Unrestricted IT\Testing\Invoices\7894-ConsolidatedInvoicingDetailViewer_APG01_4770998-2024-04-18-91720 PM.pdf"

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



print(response)