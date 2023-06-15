# This script will delete all local users on reboot of the server
# Created 2023-06-15 by Chris Stogsdill
# logs will be created in ./logs/date.log

try {
    # list of accounts we do NOT want to delete
    $profilesToKeep = 'NetworkService','LocalService','systemprofile', 'Administrator'

    "Attempting to remove the following accounts" >> ".\logs\$logFileName"
    Get-CimInstance -Class Win32_UserProfile | Where-Object { $_.LocalPath.split('\')[-1] -notin $profilesToKeep } | Select-Object -Property LocalPath | Out-File -FilePath ".\logs\$logFileName" -Append

    # Delete profiles that are not in profilesToKeep
    $deletedProfiles = Get-CimInstance -Class Win32_UserProfile | Where-Object { $_.LocalPath.split('\')[-1] -notin $profilesToKeep } | Remove-CimInstance

    # Get the current date
    $today = Get-Date -Format "yyyy-MM-dd"
    $logFileName = "$today.log"


    $deletedProfiles | Out-File -FilePath ".\logs\$logFileName" -Append


    # cleanup the logs folder. 
    # delete files older than 30 days in logs folder
    "Cleaning up logs older than 30 days" >> ".\logs\$logFileName"
    Get-ChildItem -Path ".\logs" -Recurse | Where-Object {($_.LastWriteTime -lt (Get-Date).AddDays(-30))} | Remove-Item

}
catch {
    "An error occurred: $_" >> ".\logs\$logFileName"
}