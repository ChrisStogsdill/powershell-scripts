# Remember to Connect-ExchangeOnline
$mailbox = "remittances"
$subjectString = "Payment Advice Note from 12/13/2023"
$startDate = "12/01/2023"
$endDate = "12/16/2023"
search-mailboxAuditLog $mailbox -ShowDetails -StartDate $startDate  -EndDate $endDate |`
Where-Object -Property SourceItemSubjectsList -EQ  $subjectString |`
Select-Object -Property SourceItemSubjectsList, Operation, OperationResult, FolderPathName, LogonUserDisplayName, LastAccessed | Format-Table
