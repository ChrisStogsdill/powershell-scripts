Import-Csv -Path 'C:\Users\cstogsdill\Downloads\users-description.csv' | ForEach-Object {
    $employeeCode = $_.'Employee_Code'
    $user = Get-ADUser -Filter "EmployeeID -eq '$employeeCode'" -Properties DisplayName, samAccountName, Enabled, LastLogonDate, employeeID, Description, Department -ErrorAction SilentlyContinue
    Set-ADUser -Identity $user -Description $_.Paycom_Description 
    Set-ADUser -Identity $user -Department $_.Location_Desc
  } 