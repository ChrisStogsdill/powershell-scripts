from pypdf import PdfWriter
import os
from datetime import datetime

def pdf_merge(coverPage, dataPDF):
    
    now = datetime.now() # current date and tim
    date_string = now.strftime("%Y%m%d%H%M%S")
    merger = PdfWriter()
    dataPDFName = os.path.basename(dataPDF)
    saveLocation = f"./FinishedPDF/{dataPDFName}-{date_string}-merged.pdf"

    print(f"Merging {coverPage} and {dataPDF}")

    for pdf in [coverPage, dataPDF]:
        merger.append(pdf)

    merger.write(saveLocation)
    merger.close()

    print (f"File Saved as {saveLocation}")
    # return final file
    return saveLocation

