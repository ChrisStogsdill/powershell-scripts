########
# Change Log 2022-03-21 - Created by Chris Stogsdill
#
# This script is to remove permissions from a target mailbox. 
########
Param (
    [Parameter(Mandatory, HelpMessage = "Enter Target Mailbox that the delegate currently has access to")]
    $targetMailbox,

    [Parameter(Mandatory, HelpMessage = "Enter in all Delegate users. Comma Separated usernames")]
    $targetDelegates  
   )


# connect with mwhsupport account because it has admin access
Connect-ExchangeOnline -UserPrincipalName mwhsupport@midwesthose.com

# split text input into array, use Trim function to get rid of whitespace.
$targetDelegatesArray = $targetDelegates.split(',').Trim()
 
# for each loop to run through each delegate 
foreach ($delegate in $targetDelegatesArray) {
    Write-Host "Removing full access for $delegate to access $targetMailbox" 
    Remove-MailboxPermission -Identity $targetMailbox -User $delegate -AccessRights FullAccess -Confirm:$false
    Write-Host " "

    Write-Host "Removing Send On Behalf access for $delegate to send on behalf of  $targetMailbox" 
    Set-Mailbox "$targetMailbox" -GrantSendOnBehalfTo @{remove="$delegate"} -Confirm:$false
    Write-Host " "

    Write-Host "Removing SendAs for $delegate to send as $targetMailbox" 
    Remove-RecipientPermission $targetMailbox -AccessRights SendAs -Trustee $delegate -Confirm:$false
    Write-Host " "
   }

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


