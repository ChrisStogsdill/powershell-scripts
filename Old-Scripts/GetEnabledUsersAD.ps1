Get-ADUser -Filter "Enabled -eq 'True'" -Properties DisplayName, samAccountName, Enabled, LastLogonDate, employeeID, Description, Department, Manager, employeeID -ErrorAction SilentlyContinue | Export-Csv -Path 'C:\Users\cstogsdill\Downloads\all-users-AD-20230720.csv' -NoTypeInformation 

