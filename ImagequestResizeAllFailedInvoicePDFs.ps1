# Imagequest is unable to process files with non standard page sizes. 
# A lot of the failed invoice expense files have pictures in them
# This script will go through all those file and set them to letter size.
# Created by Chris Stogsdill 2024-04-08

# Define the path to the directory containing the files
$directory = "M:\Unrestricted IT\IQ Invoice Expense Processing\Failure"

# Define the path to your Python script
$pythonScript = "PDFSetSizeToLetter.py"

# Check if the specified directory exists
if (Test-Path $directory -PathType Container) {
    # Get all files in the directory
    $files = Get-ChildItem -Path $directory -File
    
    # Loop through each file
    foreach ($file in $files) {
        # Construct the full path to the Python script and the input file
        # Script path will need to be adjusted for future use.
        #$scriptPath = Join-Path -Path $directory -ChildPath $pythonScript
        $filePath = Join-Path -Path $directory -ChildPath $file.Name
        
        # Run the Python script on this file
        Write-Host "Running Python script on $($file.Name)..."
        python $pythonScript $filePath
    }
} else {
    Write-Host "Directory '$directory' not found."
}
