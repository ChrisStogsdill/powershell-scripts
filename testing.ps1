$accounts = Get-WmiObject Win32_UserAccount -filter "LocalAccount=True and SIDType=1"
foreach ($account in $accounts) {
    if ($account.Name -ne "mwhadmin") {
        write-host $account
    }
}