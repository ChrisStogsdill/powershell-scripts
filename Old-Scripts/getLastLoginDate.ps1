# Import the CSV file
$users = Import-Csv .\last-login.csv

# Loop through each user and update the LastLogin column
foreach ($user in $users) {
    # Get the last login attribute for the user
    $lastLogin = get-aduser -identity $user.username -properties lastLogonDate

    $user.LastLogin = $lastLogin.LastLogonDate

}

# Export the updated CSV file
$users | Export-Csv .\last-login2.csv -NoTypeInformation
