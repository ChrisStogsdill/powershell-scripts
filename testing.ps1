# ---------------------------------------------------------------------------
#
# This script requires a computer name.  It will return the computer's 
# currently logged-in user's default printer.
#
# ---------------------------------------------------------------------------

# Set the variable below to choose your computer
$Computer = "computer_name"


# get the logged-in user of the specified computer
$user = Get-WmiObject –ComputerName $computer –Class Win32_ComputerSystem | Select-Object UserName

# get that user's AD object
$AdObj = New-Object System.Security.Principal.NTAccount($user.UserName)

# get the SID for the user's AD Object 
$strSID = $AdObj.Translate([System.Security.Principal.SecurityIdentifier])

# get a handle to the "USERS" hive on the computer
$reg = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey("Users", $Computer)

# get a handle to the current user's USERS Registry key where the default printer value lives
$regKey = $reg.OpenSubKey("$strSID\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Windows")

# read and show the new value from the Registry for verification
$regValue = $regKey.GetValue("Device")
write-output $regValue
write-output " "
write-output " "
[void](Read-Host 'Press Enter to continue…')