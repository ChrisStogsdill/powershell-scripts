####### 
# Created 2022-05-17 by Chris Stogsdill
# this script will add a teams phone number to a user
#######

# Setup Parameters
Param
(
    [Parameter(Mandatory, HelpMessage="Username the User to add the phone number to `n ex: cstogsdill")]
    $userNameInput,
    [Parameter(Mandatory, HelpMessage="Phone number to add to the user. `n Usually just add a 9 to the begginning of their existing extengion. `n ex: +191082")]
    $phoneNumberInput
)

Read-Host "Do not forget to add teams phone license to the user(press enter to continue)"

# setup a Do While loop to re-ask for user if not found
Do
{
    $userNameCheckFailure = $false
    try 
    {
        $user = Get-ADUser -Identity $userNameInput
        # extract email from the user object
        $userEmail = $user.UserPrincipalName
        Write-Host "User found"
        Write-Host $userEmail
        
    } 
    catch 
    {
        Write-Host "User not found, please try again"
        $userNameInput = Read-Host "Enter the Username"
        $userNameCheckFailure = $true
    }
} While ($userNameCheckFailure -eq $true) 

# istall module only needs to happen once. Set a try catch to make sure it only happens once
try
{
    Set-ExecutionPolicy Unrestricted -Force; Import-Module MicrosoftTeams; Connect-MicrosoftTeams
}
catch
{
    Install-Module MicrosoftTeams -Force -AllowClobber
    Set-ExecutionPolicy Unrestricted -Force; Import-Module MicrosoftTeams; Connect-MicrosoftTeams
}

Grant-CsOnlineVoiceRoutingPolicy -Identity "$($userEmail)" -PolicyName "UTOVRP"

Set-CsPhoneNumberAssignment -Identity $userEmail -PhoneNumber $phoneNumberInput -PhoneNumberType DirectRouting; Set-CsOnlineVoicemailUserSettings -Identity sip:$userEmail -VoicemailEnabled $true

Read-Host "Press Enter to exit"
