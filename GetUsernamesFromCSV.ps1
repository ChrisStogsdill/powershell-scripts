#####
#
# Created 20220422 by Chris Stogsdill
# The script will take a csv file as an imput and try to get usernames from it.
# 
#####


# Open File Diolog to get the file.
# Add-Type -AssemblyName System.Windows.Forms
# $FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
# $FileBrowser.filter = "Csv (*.csv)| *.csv"
# [void]$FileBrowser.ShowDialog()
# $importFile = $FileBrowser.FileName


$dataFromCSV = Import-Csv -Path ./users.csv 

$userNameKey = ''



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
        else {
            return ''
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
foreach ($object in $dataFromCSV) {
    # Get the username from the object
    $userName = $object."$userNameKey"
    # Write the username to the console
    Write-Host $userName
}



Read-Host "Press Enter to Exit"





