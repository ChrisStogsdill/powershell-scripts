$Users = Get-MsolUser | Where-Object {$_.IsLicensed -eq $false -and $_.EmailAddress -ne $null}
foreach ($User in $Users)
{
    Write-Output "User: $($User.UserPrincipalName) does not have an Office license but has a mailbox."
}
