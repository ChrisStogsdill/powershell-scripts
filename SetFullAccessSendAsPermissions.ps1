########
# Change Log 2022-03-18 - Created by Chris Stogsdill
#
# This script will take in A target mailbox parameter, and one or several delegate parameters. 
# It will give Full Access, and Send As permissions to each delegate
#
# It will also enable to copy of sent items to the target mailbox. 
########
Param (
    [Parameter(Mandatory, HelpMessage = "Enter Target Mailbox that other users are getting access to")]
    $targetMailbox,

    [Parameter(Mandatory, HelpMessage = "Enter in all Delegate users. Comma Separated usernames")]
    $targetDelegates  
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



# split text input into array, use Trim function to get rid of whitespace.
$targetDelegatesArray = $targetDelegates.split(',').Trim()
 
# for each loop to run through each delegate 
foreach ($delegate in $targetDelegatesArray) {
    Write-Host "Adding full access for $delegate to access $targetMailbox" 
    Add-MailboxPermission -Identity $targetMailbox -User $delegate -AccessRights FullAccess -Confirm:$false
    Write-Host " "

    Write-Host "Adding Send On Behalf access for $delegate to send on behalf of  $targetMailbox" 
    Set-Mailbox "$targetMailbox" -GrantSendOnBehalfTo @{add="$delegate"} -Confirm:$false
    Write-Host " "

    Write-Host "Adding SendAs for $delegate to send as $targetMailbox" 
    Add-RecipientPermission $targetMailbox -AccessRights SendAs -Trustee $delegate -Confirm:$false
    Write-Host " "
   }

# set the MessageCopy for both send as and send on behalf as true. 
# This lets a copy of sent items be put in the target mailbox's sent items.

Write-Host "Setting MessageCopy for sent items setting for $targetMailbox"
set-mailbox $targetMailbox -MessageCopyForSentAsEnabled $True
set-mailbox $targetMailbox -MessageCopyForSendOnBehalfEnabled $True

Write-Host " "
Write-Host " "


#
# Now output the current permissions
#

# see full access rights
Write-Host "Full Access"
Get-MailboxPermission -Identity $targetMailbox | Select-Object User, AccessRights | Out-Host
Write-Host " "


# see send on behalf of
Write-Host "Users with Send on Behalf Permissions"
Write-Host " "
Get-Mailbox -Identity $targetMailbox | Select-Object -ExpandProperty GrantSendOnBehalfTo  | Out-Host
Write-Host " "
Write-Host " "

# see Send As permissions
Write-Host "Users with Send As permissions"
Get-RecipientPermission -Identity $targetMailbox | Select-Object Trustee, AccessRights | Out-Host
Write-Host " "




Write-Host " "
Read-Host "Press ENTER to exit"


