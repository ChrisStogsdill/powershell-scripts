#####
#
# Created 20220422 by Chris Stogsdill
# The script will take a csv file as an imput and try to get usernames from it.
# 
#####


# Open File Diolog to get the file.
 Add-Type -AssemblyName System.Windows.Forms
 $FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
 $FileBrowser.filter = "Csv (*.csv)| *.csv"
 [void]$FileBrowser.ShowDialog()
 $importFile = $FileBrowser.FileName


 $dataFromCSV = Import-Csv -Path $importFile  


# Function to loop through the keys and find the username key using the input as a search term
function getUserNameKey {
    param (
        [Parameter(Mandatory)]
        $searchTerm
    )

    # Put Header Row Key into a variable
    $listOfKeys = $dataFromCSV[0].psobject.properties.name

    # Loop through the keys and find the username key
    foreach ($key in $listOfKeys) {
        if ($key -like $searchTerm) {
            return $key
        }
    }
}

# Function to for a menu to select a header row
function headerSelectionMenu {
    Write-Host "Please make a selection `n"
    for ($i = 0; $i -lt $dataFromCSV[0].psobject.properties.name.count; $i++) {
        $menuNumber = $i + 1
        Write-Host "$menuNumber) - "  $dataFromCSV[0].psobject.properties.name[$i]
    }    
    $menuInput = read-host "Enter the number of the header row you want to use"
    $userNameKey = $dataFromCSV[0].psobject.properties.name[$menuInput -1]
}

$userNameKey = getUserNameKey -searchTerm '*name*'

if ($userNameKey -eq '') {
    Write-Host "Could not find a username key `n"
    headerSelectionMenu
}

Write-Host $dataFromCSV[0].psobject.properties.Name[1]


# Loop through the CSV objects 
foreach ($lineObject in $dataFromCSV) {
    
    # Get the username from the object
    $fullName = $lineObject."$userNameKey"
    $lastName = $fullName.split(',').split(' ')[0]
    $firstNameWhole = $fullName.split(',')[1]
    $firstName = $firstNameWhole.split(' ')[1]
    $firstInitial = $firstName[0]
    $userNameSearchTerm = $firstInitial + $lastName
    
    # Search for the username
    try {
        $userName = get-aduser -Filter "Name -like ""*$lastName"" -and Name -like ""$firstInitial*"""

        # Get a count of the output
        $userNameOutputCount = $userName.Count

        # If the count is greater than 1, then we have a duplicate
        if ($userNameOutputCount -gt 1) {
            Write-Host "Duplicate found for $fullName `n"
            Write-Host "Please Select the correct user `n `n"
            
            for ($i = 0; $i -lt $userNameOutputCount; $i++) {
                $menuNumber = $i + 1
                Write-Host "$menuNumber) - "  $userName[$i].Name
            }
            Write-Host "$($i+1)) - SKIPPED `n"
            $menuInput = read-host "Enter the number of the user you want to use"
            $userName = $userName[$menuInput -1]

            if ($menuInput -eq $($i+1)) {
                $userName = "SKIPPED"                
            }
            
            Write-Host "User Selected: $($userName.Name) `n"

        }

        #  if the count is null, then set $userName to SKIPPED
        if ($userNameOutputCount -eq 0) {
            Write-Host "No user found for $fullName `n"
            $userName = 'NO USERNAME'
        }   

        Write-Host $userName.SamAccountName
    }
    catch {
        $userName = "error"
        Write-Host $userName
        Write-Host $_
    }
  
    # Make sure SamAccountName is not null
    if ($userName.SamAccountName) {
        # Update $lineObject with the username
        $lineObject | Add-Member -MemberType NoteProperty -Name 'UserName_Extracted' -Value $userName.SamAccountName -Force
    }
    else {
        $lineObject | Add-Member -MemberType NoteProperty -Name 'UserName_Extracted' -Value $userName -Force
    }

}

# Write the an output csv file
$dataFromCSV | Export-Csv -Path ./username_extracted.csv

#open the csv file
start ./username_extracted.csv


Read-Host "Press Enter to Exit"





