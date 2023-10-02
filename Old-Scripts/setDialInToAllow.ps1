# This needs to be ran on a DC to work. 
$users = Get-ADUser -Filter *
foreach ($user in $users) {

    netsh RAS set user $user.samAccountName PERMIT
    
    }