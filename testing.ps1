# Import the Active Directory module
Import-Module ActiveDirectory

# Specify the OUs to exclude 
$excludedOUCorry = "OU=Corry,OU=MWH,DC=MidwestHose,DC=com" 
$excludedOUDisabled = "OU=Disabled Resources,DC=MidwestHose,DC=com"

# Get all disabled users except those in the excluded OUs

$disabledUsers = Get-ADUser -Filter {Enabled -eq $false} -Properties DistinguishedName 

# $disabledUsers = Get-ADUser -Filter {Enabled -eq $false} -Properties DistinguishedName |
#     Where-Object { ($_.DistinguishedName -notlike "*OU=Disabled*" )`
#         -AND ($_.DistinguishedName -notlike "*OU=Corry*")`
#         -AND ($_.DistinguishedName -notlike "*OU=IT Department*")`
#         -AND ($_.DistinguishedName -notlike "*CN=Builtin*")}

# Display the results
# $disabledUsers | Get-Mailbox -ErrorAction SilentlyContinue | Select-Object UserPrincipalName, RecipientTypeDetails

# $disabledUsers | Select-Object UserPrincipalName

 foreach ($user in $disabledUsers) {
    if ($null -ne $user.UserPrincipalName) {
     $userMailbox = Get-Mailbox -ErrorAction SilentlyContinue -Identity $user.UserPrincipalName | Select-Object RecipientTypeDetails, UserPrincipalName  |
        Where-Object -Property RecipientTypeDetails -eq "UserMailbox" 
        
        if ($null -ne $userMailbox) {Set-Mailbox -Identity $userMailbox.UserPrincipalName -Type Shared }
     
    }
 }

