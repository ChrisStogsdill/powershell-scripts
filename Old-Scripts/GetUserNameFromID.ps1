# Open File Diolog to get the file.
Add-Type -AssemblyName System.Windows.Forms
$FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
$FileBrowser.filter = "Csv (*.csv)| *.csv"
[void]$FileBrowser.ShowDialog()
$importFile = $FileBrowser.FileName


$dataFromCSV = Import-Csv -Path $importFile 

# Loop through the data
foreach($dataLine in $dataFromCSV) {
    # set Employee ID Variable
    $currentEmployeeID = $dataLine.Employee_Code
    # find username associated to the Employee_Code
    $currentUser = Get-ADUser -Filter "EmployeeID -eq $($currentEmployeeID)" -Properties "samaccountname"
    $currentUserName = $currentUser.samaccountname
    Write-Host $currentUserName

    #  add currentUserName to the line
    $dataLine | Add-Member -MemberType NoteProperty -Name 'UserName_Extracted' -Value $currentUserName -Force
    
}

# output to csv file
$dataFromCSV | Export-Csv -Path ./username_from_employeeID.csv -NoTypeInformation