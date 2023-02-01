Import-Csv -Path C:\Users\cstogsdill\Downloads\all-users6.csv | ForEach-Object {
    $lastName = $_."Last-Name".Trim()
    $user = Get-ADUser -Filter "Surname -eq '$lastName'" -ErrorAction SilentlyContinue
    if ($user) {
        $_."Last-Name-Found" = "YES"
    } else {
        $_."Last-Name-Found" = "NO"
    }
    $_
} | Export-Csv -Path C:\Users\cstogsdill\Downloads\all-users7.csv -NoTypeInformation
