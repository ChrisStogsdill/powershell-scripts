from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import ignored.AzureDocIntelligence as azureLogin
import re

def get_invoice_ocr_data(sourceDocument):
    endpoint = azureLogin.endpoint
    key = azureLogin.key

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    # Open the document and upload it to azure
    with open(sourceDocument, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-invoice", document=f, locale="en-US"
        )
    invoices = poller.result()

    # Initialize Values
    purchase_order = ""
    vendor_name = ""
    customer_name = ""
    invoice_id = ""
    invoice_total = ""


    # Pull data out of ocr results
    for idx, invoice in enumerate(invoices.documents):
        print(f"--------Recognizing invoice #{idx + 1}--------")

        purchase_order_result = invoice.fields.get("PurchaseOrder")
        if purchase_order_result:
            print(f"Purchase Order: {purchase_order_result.value} has confidence: {purchase_order_result.confidence}")
            raw_purchase_order = purchase_order_result.value
            # clean any non numbers out of the purchase order
            purchase_order = re.sub("\D", "", raw_purchase_order)
            print(f"Cleaned Purchase Order: {purchase_order}")
            
        vendor_name_result = invoice.fields.get("VendorName")    
        if vendor_name_result:
            print(f"Vendor Name: {vendor_name_result.value} has confidence: {vendor_name_result.confidence}")
            vendor_name = vendor_name_result.value
            
        customer_name_result = invoice.fields.get("CustomerName")
        if customer_name_result:
            print(f"Customer Name: {customer_name_result.value} has confidence: {customer_name_result.confidence}")
            customer_name = customer_name_result.value
            
        invoice_id_result = invoice.fields.get("InvoiceId")
        if invoice_id_result:
            print(f"Invoice Id: {invoice_id_result.value} has confidence: {invoice_id_result.confidence}")
            invoice_id = invoice_id_result.value

        invoice_total_result = invoice.fields.get("InvoiceTotal")
        if invoice_total_result:
            print(f"Invoice Total: {invoice_total_result.value} has confidence: {invoice_total_result.confidence}")
            invoice_total = str(invoice_total_result.value)

        print("----------------------------------------")

    # If purchase order is still "", try to find it in the text matching 00NNNNNN
    if purchase_order == "":
        for page in invoices.pages:
            for word in page.words:
                cleanedResult = re.search(r"00\d{6}", word.content)
                if cleanedResult is not None:
                    purchase_order = cleanedResult.group()
                    print(f"Purchase Order: {purchase_order} found in text")
                    break
            if purchase_order != "":
                break
    
    # if purchase order is still "", try to find it in the text matching NNNNNN
    if purchase_order == "":
        for page in invoices.pages:
            for word in page.words:
                cleanedResult = re.search(r"\d{6}", word.content)
                if cleanedResult is not None:
                    purchase_order = cleanedResult.group()
                    print(f"Purchase Order: {purchase_order} found in text")
                    break
            if purchase_order != "":
                break


    # print(purchase_order, vendor_name, customer_name, invoice_id, invoice_total)
    return purchase_order, vendor_name, customer_name, invoice_id, invoice_total

# Testing document 
# get_invoice_ocr_data("./TestWatchFolder/testInvoice.pdf")
