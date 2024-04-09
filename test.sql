DECLARE @cleanedPLNumber varchar(1000) 
SET @cleanedPLNumber = '[%PLNumber%]' 
While PatIndex('%[^0-9%]%', @cleanedPLNumber) > 0 
Set @cleanedPLNumber = Stuff(@cleanedPLNumber, PatIndex('%[^0-9]%', @cleanedPLNumber), 1, '') 

SELECT co.OrderType AS OrderType, co.HeaderRef AS OrderNumber, co.Location AS Location, co.DateShipped AS ShippedDate, co.PickedBy AS PickedBy, co.ShippedBy AS ShippedBy, co.TrackingNumber AS Tracking, co.CustomerPO AS CustomerPO, co.DatePackListPrinted AS PLPrinted, vpf.CustomerShipTo AS ShipTo, vpf.SellingLocation AS SellingLocation, vpf.QuoteNumber AS QuoteNumber, vpf.WrittenBy AS WrittenBy,
STRING_AGG(CONVERT(NVARCHAR(max), ari.InvoiceNumber), ', ') AS InvoiceNumber, vpf.Type AS SOType, CASE WHEN vpf.HoldInvoice = 1 THEN 'Yes' ELSE 'No' END AS InvoiceHeld
FROM tblwhPickTicket co
LEFT JOIN dbo.tblsoSO vpf ON vpf.SONumber = co.HeaderRef
LEFT JOIN dbo.tblarInvoice ari ON ari.SONumber = co.HeaderRef
WHERE co.PickTicketNumber LIKE ('%'+ @cleanedPLNumber )+ '%'
GROUP BY PickTicketNumber, co.OrderType, co.HeaderRef, Location, co.DateShipped, co.PickedBy, co.TrackingNumber, co.CustomerPO, co.DatePackListPrinted, vpf.customerShipTo, vpf.SellingLocation, vpf.QuoteNumber, vpf.WrittenBy, vpf.Type, co.ShippedBy, vpf.HoldInvoice