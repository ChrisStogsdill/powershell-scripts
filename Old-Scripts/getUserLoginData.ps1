########
# Change Log 2022-04-05 - Created by Chris Stogsdill
# 
# This takes too long to run.
#
# This Script will get login information for users from the domain controllers 
#############

# Get a list of all domain controllers
$domainContollers = Get-AdDomainController -Filter *

# Prompt for date range
$startDateInput = Read-Host -Prompt "Enter Time Range (ex: -7):"
$startDate = (get-date).AddDays($startDateInput)

# Promt for username
$userName = Read-Host -Prompt "Enter Username:"

# loop through each domain controller and get the login event logs
foreach ($DC in $domainContollers) {
    $allLogs = Get-Eventlog -LogName Security -ComputerName $DC.hostname -after $startDate | Where-Object {($_.eventID -eq 4624) -or ($_.eventID -eq 4625)}
}

# loop through each log with the usnername and get the computer workstation name
foreach ($log in $allLogs) {
    # Logon Successful Events 
    # Local (Logon Type 2) 
    if (($log.EventID -eq 4624) -and ($log.ReplacementStrings[8] -eq 10) -and ($log.ReplacementString[5] -eq $userName)) {
         write-host "Type: Local Logon`tDate: "$log.TimeGenerated "`tStatus: Success`tUser: "$log.ReplacementStrings[5] "`tWorkstation: "$log.ReplacementStrings[11]
    }
}