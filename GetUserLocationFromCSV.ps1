# Open File Diolog to get the file.
#  Add-Type -AssemblyName System.Windows.Forms
#  $FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
#  $FileBrowser.filter = "Csv (*.csv)| *.csv"
#  [void]$FileBrowser.ShowDialog()
#  $importFile = $FileBrowser.FileName

# Import the data from the csv file
$dataFromCSV = Import-Csv -Path /username_extracted.csv

# loop through each line and get the location of the user
foreach ($lineInCSV in $dataFromCSV) {
    
    # Get the username and catch the error if the username is not found
    try {
        $userName = get-aduser $lineInCSV.UserName_Extracted
        $fullLocation = $userName.DistinguishedName
        $locationArray = $fullLocation -split ","
        $location = $locationArray[-4]

    }
    catch {
        $fullLocation = "Not Found"
        $location = "Not Found"
    }
        
    # Add the location to the csv file
    $lineInCSV | Add-Member -MemberType NoteProperty -Name 'Location_Extracted' -Value $location -Force
    $lineInCSV | Add-Member -MemberType NoteProperty -Name 'FullLocation_Extracted' -Value $fullLocation -Force
}

# Save the csv file
$dataFromCSV | Export-Csv -Path /Location_Extracted.csv -NoTypeInformation