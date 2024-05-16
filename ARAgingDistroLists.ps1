# Connect to Exchange Online PowerShell (requires Exchange Online PowerShell module)
# Make sure you have the necessary permissions to run these commands

# Connect to Exchange Online PowerShell
# $UserCredential = Get-Credential
Connect-ExchangeOnline 

# Define the pattern to match distribution lists (change "araging*" to your desired pattern)
$Pattern = "araging*"

# Get all distribution lists matching the pattern
$DistributionLists = Get-DistributionGroup -ResultSize Unlimited | Where-Object { $_.Name -like $Pattern }

# Loop through each distribution list
foreach ($DL in $DistributionLists) {
    Write-Host "Distribution List: $($DL.Name)"
    Write-Host "Members:"

    # Get members of the distribution list
    $Members = Get-DistributionGroupMember -Identity $DL.Identity

    # Output each member
    foreach ($Member in $Members) {
        Write-Host "- $($Member.Name) ($($Member.RecipientType))" 
        # $Member.RecipientType will show the type of member (User, MailContact, etc.)
    }

    Write-Host "---------------------"
}

# Disconnect from Exchange Online PowerShell session
Disconnect-ExchangeOnline -Confirm:$false
