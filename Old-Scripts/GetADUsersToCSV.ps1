Import-Module ActiveDirectory

$users = Get-ADUser -Filter * -Properties DisplayName, samAccountName, Enabled, LastLogonDate, employeeID, Description, Title | 
         Select-Object DisplayName, Title, samAccountName, Enabled, LastLogonDate, employeeID, Description

$users | Export-Csv -Path ".\ignored\ADUsers2.csv" -NoTypeInformation
