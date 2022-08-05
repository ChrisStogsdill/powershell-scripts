# get data from csv
$csvFile = Import-Csv -Path /EmployeeIDList.csv

foreach ($line in $csvFile) {
    $EmployeeID =  $line.Employee_Code 
    $username = $line.UserName_Extracted

    # set employee id
    Set-ADUser -Identity $username -EmployeeID $EmployeeID
    
}