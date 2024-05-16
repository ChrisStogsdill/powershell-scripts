import os
import sys
from glob import glob
from ImagequestAzureDocumentIntelegence import get_invoice_ocr_data
from CreatePOCoverPage import create_cover_page
from PDFMerge import pdf_merge
import shutil

def ProcessPOFile(sourceFile, outputFolder):
    fileName = os.path.basename(sourceFile)
    # First step is to take the file, upload it to azure and get data back
    print(f"Getting Azure data for file: {sourceFile}")
    purchase_order, vendor_name, customer_name, invoice_id, invoice_total = get_invoice_ocr_data(sourceFile)

    #  Next, pass that data into the cover page
    print("Creating cover page")
    currentCoverPage = create_cover_page(f"./CoverPages/{fileName}-CoverPage.pdf", purchase_order, vendor_name, customer_name, invoice_id, invoice_total)

    # Merge the cover page and the data pdf
    finishedFile = pdf_merge(coverPage=currentCoverPage, dataPDF=sourceFile)


    # Move finishedFile to output folder
    print(outputFolder)
    shutil.move(finishedFile, outputFolder)

    # Delete Temp files
    print ("Archiving Temp files")
    os.remove(currentCoverPage)
    os.remove(sourceFile)




ProcessPOFile(sourceFile=sys.argv[1], outputFolder=sys.argv[2])