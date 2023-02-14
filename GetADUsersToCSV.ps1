Import-Module ActiveDirectory

$users = Get-ADUser -Filter * -Properties DisplayName, samAccountName, Enabled, LastLogonDate, employeeID | 
         Select-Object DisplayName, samAccountName, Enabled, LastLogonDate, employeeID

$users | Export-Csv -Path ".\ignored\ADUsers.csv" -NoTypeInformation
