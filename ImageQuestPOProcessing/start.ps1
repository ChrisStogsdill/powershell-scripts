# Get all PDF files in the current folder
$pdfs = Get-ChildItem -Filter ./TestWatchFolder/*.pdf

# Iterate through each PDF file
foreach ($pdf in $pdfs) {
    write-host $pdf
    # Run the script on the PDF file
    python.exe .\ProcessPOFile.py $pdf

}