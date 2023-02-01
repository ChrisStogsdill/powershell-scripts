Import-Csv -Path 'C:\Users\cstogsdill\Downloads\all-users5.csv' | ForEach-Object {
    $firstName = $_.'First-Name' -split ' ' | Select-Object -First 1
    $lastName = $_.'Last-Name' -split ' ' | Select-Object -First 1
    $employeeCode = $_.'Employee_Code'
    $username = $firstName[0] + $lastName
    $user = Get-ADUser -Filter "samAccountName -eq '$username'" -ErrorAction SilentlyContinue
    if ($user -eq $null) {
      $_.'Code-Added' = 'NO'
    }
    elseif ($user.Count -eq 1) {
      Set-ADUser -Identity $user.DistinguishedName -EmployeeID $employeeCode
      $_.'Code-Added' = 'YES'
    }
    else {
      $_.'Code-Added' = 'NO'
    }
    $_ | Export-Csv -Path 'C:\Users\cstogsdill\Downloads\all-users6.csv' -NoTypeInformation -Append
  }
  