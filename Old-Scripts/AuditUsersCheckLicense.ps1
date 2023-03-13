$csvInput = Import-Csv -Path c:\Users\cstogsdill\Downloads\UserOldLoginLicenseCheck.csv
$csvOutput = @()
$csvInput | ForEach-Object{
    $userName = $_.username + "@midwesthose.com"
    $userq = Get-MsolUser -UserPrincipalName $userName
    if($userq) {
        $_.isLicensed = $userq.isLicensed
    }
    $csvOutput += $_
}

$csvOutput | Export-Csv -Path .\ignored\licenseoutput.csv -NoTypeInformation