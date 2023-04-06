# I got tired of having to look through every report to find a user's subscription.
# This script will go through the subscriptions and find the user you need
# NOTE - you may need to login with support credentials to find everything
# Chris Stogsdill 2023-03-17

# Set up variables
$ReportServerUri = "http://corp-reports-01/ReportServer/ReportService2010.asmx?WSDL"
$User = Read-Host "Target Username: "
$Credentials = Get-Credential
Write-Host "`n"

# Connect to SSRS web service
$rs = New-WebServiceProxy -Uri $ReportServerUri -Credential $Credentials

# Get a list of subscriptions for the user
$Subscriptions = $rs.ListSubscriptions("/") #| Where-Object { $_.SubscriberName -eq $User }

# loop through all subscriptions
foreach ($Subscription in $Subscriptions) {
    # loop through all parameters in a subscription
    # this will find To and CC/BCC
    foreach ($parametervalue in $Subscription.DeliverySettings.ParameterValues){
        if ($parametervalue.Value -like "*$User*"){
            # get the folder it is located in
            Write-Host "Path " $Subscription.Path
            # get the date it was last run
            Write-Host "Last run: " $Subscription.LastExecuted
            # get the name of the subscription
            Write-Host "$($parametervalue.Value) In $($Subscription.Description) `n" 
        }
    }

}

Read-Host "Completed, Press Enter to continue"