#####
# Created by Chris 2022-03-22
# to use, put a csv of usernames in the same dir and give the script the file name.
# This script will disable the account
#   Put the date the account was disabled in the description
#   And move the account to the Disabled Resources OU in AD
#####
Param (
    [Parameter(Mandatory, HelpMessage = "Enter CSV File name")]
    $importFile
)

$disabledDate = get-date -Format yyyy/MM/dd

# Extract content from file
$userList = Get-Content -Path ".\$($importFile)"

foreach ($user in $userList) {
    $userData = Get-ADUser $user -Properties Description 
    
    Write-Host "Disable account for $($user)"
    Write-Host " "

    # Disable the account
    Disable-ADAccount $user
    Write-Host " "

    Write-Host "Updating Description for $($user)"
    Write-Host " "

    # Update description to include disabled date.
    Set-Aduser $user -Description "Disabled $($disabledDate) $($userData.Description)"
    Write-Host " "

    Write-Host "Moving $($user) to Disabled Resources OU"
    Write-Host " "

    # Move user to Disabled Resources OU
    Get-ADUser $user | Move-ADObject -TargetPath "OU=Disabled Resources,DC=MidwestHose,DC=com"

}

Read-Host "Press Enter to exit"