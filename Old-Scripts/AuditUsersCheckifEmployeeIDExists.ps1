Import-Csv -Path C:\Users\cstogsdill\Downloads\all-users2.csv | ForEach-Object {
    $employeeCode = $_.'Employee_Code'
    $user = Get-ADUser -Filter "employeeID -eq '$employeeCode'" -ErrorAction SilentlyContinue
    if ($user) {
        $_ | Add-Member -Force -MemberType NoteProperty -Name 'In_AD' -Value 'YES'
    } else {
        $_ | Add-Member -Force -MemberType NoteProperty -Name 'In_AD' -Value 'NO'
    }
    $_
} | Export-Csv -Path C:\Users\cstogsdill\Downloads\all-users3.csv -NoTypeInformation
