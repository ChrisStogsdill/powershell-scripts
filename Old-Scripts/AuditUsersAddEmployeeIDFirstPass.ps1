Import-Csv -Path 'C:\Users\cstogsdill\Downloads\all-users-compare.csv' | ForEach-Object {
    $employeeCode = $_.'Employee_Code'
    $user = Get-ADUser -Filter "EmployeeID -eq '$employeeCode'" -Properties DisplayName, samAccountName, Enabled, LastLogonDate, employeeID, Description, Department -ErrorAction SilentlyContinue
    $_.AD_Name = $user.DisplayName
    $_.AD_Enabled = $user.Enabled
    $_.AD_Description = $user.Description
    $_.AD_Location = $user.Department
    $_.AD_Distinguished_Name = $user.DistingueshedName
    $_
  } | Export-Csv -Path 'C:\Users\cstogsdill\Downloads\all-users-compare2.csv' -NoTypeInformation 