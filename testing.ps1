$dataFromCSV = Import-Csv -Path /username_extracted_final.csv

foreach ($dataLine in $dataFromCSV) {
    Set-ADUser -Identity $dataLine.UserName_Extracted -OfficePhone $dataLine.Label
}
