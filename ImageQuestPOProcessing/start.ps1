# Get all PDF files in the current folder
$pdfs = Get-ChildItem -Filter ./TestWatchFolder/*.pdf
$outputFolder = "C:\Users\cstogsdill\Desktop\code\powershell-scripts\ImageQuestPOProcessing\TestOutput"
$today = (Get-Date).ToString("yyyy-MM-dd")
$logFolder = "./logs/"

# Check if TestWatchFolder directory exists
if (-not (Test-Path -Path "./TestWatchFolder")) {
    Write-Host "TestWatchFolder directory does not exist."
    Exit
}

# Check if logs directory exists
if (-not (Test-Path -Path "./logs")) {
    Write-Host "logs directory does not exist."
    Exit
}

Start-Transcript -Path "${logFolder}${today}.log" -Append

# Iterate through each PDF file in parallel
$pdfs | ForEach-Object {
    $pdf = $_
    Write-Host $pdf
    # Run the script on the PDF file
    python.exe .\ProcessPOFile.py "$pdf" "$outputFolder"
}

Stop-Transcript
