#####
#
# Created by Chris Stogsil on 12/31/12.
# This will take in a csv file and disable each computer.
# It will then move the computer to the disabled recources OU.
#
######
Param (
    [Parameter(Mandatory, HelpMessage = "Enter CSV File name")]
    $importFile
)

$disabledDate = get-date -Format yyyy/MM/dd

# Extract content from file
$pcList = Get-Content -Path ".\$($importFile)"

foreach ($computer in $pcList) {
    $computerData = Get-ADComputer -Id $computer -Properties Description

    # Disable the computer
    Write-Host " "
    Write-Host "Disabling $($computer)"
    Write-Host " "
    Set-ADComputer -Identity $computer -Enabled $false
    Write-Host " "

    # Prepend disabled date to computer description
    Write-Host "Prepending the disabled date to the description"
    Set-ADComputer -Identity $computer -Description "Disabled on $($disabledDate)  $($computerData.Description)"
    Write-Host " "

    # Move the computer to the Disabled OU
    Write-Host "Moving $computer to Disabled Resources OU"
    Write-Host " "
    Get-AdComputer $computer | Move-ADObject -TargetPath "OU=Computers,OU=Disabled Resources,DC=MidwestHose,DC=com"
    Write-Host " "

}

Read-Host "Press Enter to Exit"