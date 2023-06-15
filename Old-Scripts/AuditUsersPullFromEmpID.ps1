$csvInput = Import-Csv -Path C:\Users\cstogsdill\Downloads\hr-active-users.csv 
$csvOutput = @()
$csvInput | ForEach-Object {
    $employeeCode = $_.'Employee_Code'
    $user = Get-ADUser -Filter "employeeID -eq '$employeeCode'" -Properties DisplayName, Enabled, Description -ErrorAction SilentlyContinue
    if ($user) {
        $_.AD_Name = $user.DisplayName
        $_.IS_Enabled = $user.Enabled
        $_.AD_Description = $user.Description
    }  
    Write-Host $_
    $csvOutput += $_
}  
$csvOutput | Export-Csv -Path C:\Users\cstogsdill\Downloads\all-users20230502.csv -NoTypeInformation