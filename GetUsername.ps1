Add-Type -AssemblyName System.Windows.Forms
$FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
$FileBrowser.filter = "Csv (*.csv)| *.csv"
[void]$FileBrowser.ShowDialog()
$importFile = $FileBrowser.FileName


$dataFromCSV = Import-Csv -Path $importFile 

foreach ($dataLine in $dataFromCSV) {

    $currentUser = Get-ADUser -Filter "EmployeeID -eq $($dataLine.Employee_Code)"
    Write-Host $currentUser.UserPrincipalName

    # Add line to the CSV file
    $dataLine | Add-Member -MemberType NoteProperty -Name 'Email' -Value $currentUser.UserPrincipalName -Force
    

}
    # Write the CSV file
    $dataFromCSV | Export-Csv -Path ./email_extracted.csv -NoTypeInformation
    