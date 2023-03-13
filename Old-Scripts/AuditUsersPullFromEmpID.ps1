$csvInput = Import-Csv -Path C:\Users\cstogsdill\Downloads\all-users.csv 
$csvOutput = @()
$csvInput | ForEach-Object {
    $employeeCode = $_.'Employee_Code'
    $user = Get-ADUser -Filter "employeeID -eq '$employeeCode'" -Properties DisplayName, Enabled -ErrorAction SilentlyContinue
    if ($user) {
        $_.AD_Name = $user.DisplayName
        $_.IS_Enabled = $user.Enabled
    }  
    Write-Host $_
    $csvOutput += $_
}  
$csvOutput | Export-Csv -Path C:\Users\cstogsdill\Downloads\all-users4.csv -NoTypeInformation