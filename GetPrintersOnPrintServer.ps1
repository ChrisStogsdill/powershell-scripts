# This Script will get all the printers installed on mwh-print and output the results to a csv file
# Created 2022-08-05

# Get all the printers installed on mwh-print
 Get-Printer -ComputerName "mwh-print" | Select-Object -Property Name, DriverName, PortName, ShareName | Export-Csv -Path ./ignored/printers.csv -NoTypeInformation

