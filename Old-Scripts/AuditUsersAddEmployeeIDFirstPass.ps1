Import-Csv -Path 'C:\Users\cstogsdill\Downloads\PaycomEnabledUsers-20230720.csv' | ForEach-Object {
    $employeeCode = $_.'Employee_Code'
    $user = Get-ADUser -Filter "EmployeeID -eq '$employeeCode'" -Properties DisplayName, samAccountName, Enabled, LastLogonDate, employeeID, Description, Department, Manager -ErrorAction SilentlyContinue
    $_.Department = $user.Department
    $_.Description = $user.Description
    $_.DisplayName = $user.DisplayName
    $_.DisplayName = $user.DistinguishedName
    $_.EmployeeID = $user.EmployeeID
    $_.Enabled = $user.Enabled
    $_.LastLogonDate = $user.LastLogonDate
    $_.Manager = $user.Manager
    $_.Name = $user.Name
    $_.samAccountName = $user.SamAccountName
    $_.Surname = $user.Surname
    $_.UserPrincipalName = $user.UserPrincipalName
    $_
  } | Export-Csv -Path 'C:\Users\cstogsdill\Downloads\EnabledUsersCombinedCompare-20230720.csv' -NoTypeInformation 