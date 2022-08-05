# Open File Diolog to get the file.
 Add-Type -AssemblyName System.Windows.Forms
 $FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
 $FileBrowser.filter = "Csv (*.csv)| *.csv"
 [void]$FileBrowser.ShowDialog()
 $importFile = $FileBrowser.FileName


 $dataFromCSV = Import-Csv -Path $importFile
 
 foreach ($csvLine in $dataFromCSV) {
     $currentUser = Get-ADUser -Identity $csvLine.UserName_Extracted -Properties Department
     
    #  set email of the current user
     $currentUserEmail =  $csvLine.UserName_Extracted + "@midwesthose.com"
     Set-Aduser -Identity $csvLine.UserName_Extracted -EmailAddress $currentUserEmail

    #  Set the office of the current user
    Set-Aduser -Identity $csvLine.UserName_Extracted -Office $csvLine.Location_Desc

    # Set the Description of the current user
    Set-Aduser -Identity $csvLine.UserName_Extracted -Description "$($csvLine.Location_Desc) - $($csvLine.Position)"

    # Set the Job Title of the current user
    Set-Aduser -Identity $csvLine.UserName_Extracted -Title $csvLine.Position

    # Set the Department of the current user if it is empty
    if ($currentUser.Department -eq $null) {
        Set-Aduser -Identity $csvLine.UserName_Extracted -Department $csvLine.Location_Desc
    }

    # Set the supervisor of the current user if there is one
    if ($csvLine.Superviser_Username -ne $null) {
        Set-Aduser -Identity $csvLine.UserName_Extracted -Manager $csvLine.Superviser_Username
    }
    
     Write-Host $currentUser.Department
 
 }