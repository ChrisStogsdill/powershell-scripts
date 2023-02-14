$inputCSV = Import-Csv -Path .\ignored\licenseoutput.csv
$inputCSV | ForEach-Object {
    $userName = $_.username
    $currentUser = Get-ADUser $userName -Properties Description
    $description = "Disabled 2023-02-08 - " + $currentUser.Description 
    Set-ADUser $userName -Enabled $false
    Set-ADUser $username -Description $description

}