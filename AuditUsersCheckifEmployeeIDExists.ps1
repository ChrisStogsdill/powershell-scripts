Import-Csv -Path C:\Users\cstogsdill\Downloads\all-users.csv | ForEach-Object {
    $employeeCode = $_.'Employee_Code'
    $user = Get-ADUser -Filter "employeeID -eq '$employeeCode'" -ErrorAction SilentlyContinue
    if ($user) {
        $_ | Add-Member -MemberType NoteProperty -Name 'In_AD' -Value 'YES'
    } else {
        $_ | Add-Member -MemberType NoteProperty -Name 'In_AD' -Value 'NO'
    }
    $_
} | Export-Csv -Path C:\Users\cstogsdill\Downloads\all-users2.csv -NoTypeInformation
