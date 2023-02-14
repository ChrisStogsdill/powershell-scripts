# Written by Chris Stogsdill 2023-02-10
# Imagequest will not re-try failed files on its own, so this script 
# will have it check all the folders listed below. 

$folders = @(
    "\\corp-fs-01\data\Unrestricted IT\IQ Packing List Processing\Failure", 
    "\\corp-fs-01\data\IQ Hose Test Graphs\Failure",
    "\\corp-fs-01\data\IQ CO Receipts\CounterOrderCustomerReceipts\Failure",
    "\\corp-fs-01\data\IQ Rotary Test Certificates\Failure",
    "\\corp-fs-01\data\IQ AR SO Packing Slip\Failure",
    "\\corp-fs-01\data\IQ Non-Trade Receipts\Failure",
    "\\corp-fs-01\data\Unrestricted IT\IQ Invoice Expense Processing\Failure",
    "\\corp-fs-01\data\IQ Tax Forms\Failure",
    "\\corp-fs-01\data\Unrestricted IT\IQ Invoice Processing\Failure",
    "\\corp-fs-01\data\IQ AR Barcode\CounterOrderCustomerReceipts\Failure",
    "\\corp-fs-01\data\IQ AR Checks\Failure"
    )

foreach ($folder in $folders) {
  Write-Host "Checking for empty files in $folder..."
  $emptyFiles = Get-ChildItem $folder | Where-Object { $_.Length -eq 0 }
  if ($emptyFiles) {
    Write-Host "Deleting empty files..."
    $emptyFiles | ForEach-Object { Remove-Item $_.FullName -Force }
    Write-Host -ForegroundColor Green "Empty files deleted successfully."
  } else {
    Write-Host "No empty files found."
  }

  Write-Host "Moving files from $folder to $($folder.TrimEnd('\'))\.."
  Get-ChildItem $folder | ForEach-Object {
    Write-Host "Moving file $_"
    Move-Item $_.FullName "$($folder.TrimEnd('\'))\.."
  }
  Write-Host -ForegroundColor Green "Files moved successfully."
}

Write-Host "Waiting, then re-checking the folder..."
$total = 60
for ($i = 1; $i -le $total; $i++) {
  Write-Progress -Activity "Waiting" -Status "Time remaining: $($total-$i) seconds" -PercentComplete (($i / $total) * 100)
  Start-Sleep -Seconds 1
}

Write-Host "Re-checking folders..."
foreach ($folder in $folders) {
  Write-Host "Files in $($folder)..:"
  $files = Get-ChildItem $folder
  Write-Output $files

  if ($files) {
    $deletePrompt = Read-Host -Prompt "Do you want to delete the files in $($folder.TrimEnd('\'))\..? (y/n) [default: n]"
    if ($deletePrompt -eq "y") {
      Write-Host "Deleting files..."
      $files | ForEach-Object { Remove-Item $_.FullName -Force }
      Write-Host -ForegroundColor Green "Files deleted successfully."
    }
  } else {
    Write-Host "Folder is empty, no files to delete."
  }
}
Write-Host "Press Enter to close."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
