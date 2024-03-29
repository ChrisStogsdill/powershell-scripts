########
# Change Log 2022-03-15 - Created by Chris Stogsdill
# 2022-03-23 - updated to use the get-exo commands
########
Param (
    [Parameter(Mandatory, HelpMessage = "Enter Username of target user. without the @midwesthose.com")]
    $targetUser
   )

   # Connect ExchangeOnline is unable to run in a catch. Have to make a variable for that
$ExchangeConnectSucceeded = $True

# Check if ExchangeOnline is already connected
try {
   Write-Host "Checking if ExchangeOnline is already connected"
   Get-EXOMailbox mwhsupport@midwesthose.com | Select-Object UserPrincipalName
   Write-Host "Success!"
}

catch {
    $ExchangeConnectSucceeded = $false
}

if ($ExchangeConnectSucceeded -eq $false) {
    Write-Host "ExchangeOnline is not connected. Connecting..."
    Connect-ExchangeOnline -UserPrincipalName mwhsupport@midwesthose.com
}


   # see full access rights
Write-Host "Full Access"
Get-EXOMailboxPermission -Identity $targetUser | Select-Object User, AccessRights | Out-Host
Write-Host " "


# see send on behalf of
Write-Host "Users with Send on Behalf Permissions"
Write-Host " "
Get-EXOMailbox -Identity $targetUser -PropertySets Delivery| Select-Object -ExpandProperty GrantSendOnBehalfTo  | Out-Host
Write-Host " "
Write-Host " "

# see Send As permissions
Write-Host "Users with Send As permissions"
Get-EXORecipientPermission -Identity $targetUser | Select-Object Trustee, AccessRights | Out-Host
Write-Host " "




# add prompt so powershell does not end immediatly
Read-Host -Prompt "Press Enter to exit"