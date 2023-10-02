import re
import json
import logging
from time import sleep
from datetime import datetime
from typing import List, Dict, Union, Optional
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading

logging.basicConfig(level=logging.INFO)

class Price:
    def __init__(self, currencyID: str, value: str):
        self.currencyID = currencyID
        self.value = value

class ListingDetails:
    def __init__(self, StartTime: datetime, ViewItemURL: str, ViewItemURLForNaturalSearch: str):
        self.StartTime = StartTime
        self.ViewItemURL = ViewItemURL
        self.ViewItemURLForNaturalSearch = ViewItemURLForNaturalSearch

class SellingStatus:
    def __init__(self, CurrentPrice: Price):
        self.CurrentPrice = CurrentPrice

class ShippingDetails:
    def __init__(self, ShippingServiceOptions: Optional[str], ShippingType: str):
        self.ShippingServiceOptions = ShippingServiceOptions
        self.ShippingType = ShippingType

class Profile:
    def __init__(self, ID: str, Name: str):
        self.ID = ID
        self.Name = Name

class SellerProfiles:
    def __init__(self, SellerShippingProfile: Profile, SellerReturnProfile: Profile, SellerPaymentProfile: Profile):
        self.SellerShippingProfile = SellerShippingProfile
        self.SellerReturnProfile = SellerReturnProfile
        self.SellerPaymentProfile = SellerPaymentProfile

class Listing:
    def __init__(self, BuyItNowPrice: Price, ItemID: str, ListingDetails: ListingDetails, 
                 ListingDuration: str, ListingType: str, Quantity: str, SellingStatus: SellingStatus,
                 ShippingDetails: ShippingDetails, TimeLeft: str, Title: str, QuantityAvailable: str,
                 SKU: str, ClassifiedAdPayPerLeadFee: Price, SellerProfiles: Optional[SellerProfiles] = None,
                 WatchCount: Optional[str] = None):
        self.BuyItNowPrice = BuyItNowPrice
        self.ItemID = ItemID
        self.ListingDetails = ListingDetails
        self.ListingDuration = ListingDuration
        self.ListingType = ListingType
        self.Quantity = Quantity
        self.SellingStatus = SellingStatus
        self.ShippingDetails = ShippingDetails
        self.TimeLeft = TimeLeft
        self.Title = Title
        self.QuantityAvailable = QuantityAvailable
        self.SKU = SKU
        self.ClassifiedAdPayPerLeadFee = ClassifiedAdPayPerLeadFee
        self.SellerProfiles = SellerProfiles
        self.WatchCount = WatchCount

class EbayListingsRetriever:

    def __init__(self, app_id: str, dev_id: str, cert_id: str, token: str):
        self.api = Trading(
            appid=app_id,
            devid=dev_id,
            certid=cert_id,
            token=token,
            config_file=None
        )
        self.items: List[Dict] = []

    def map_api_to_listing(self, item_data):
        BuyItNowPrice_obj = Price(item_data.BuyItNowPrice._currencyID if hasattr(item_data, 'BuyItNowPrice') else None, 
                                item_data.BuyItNowPrice.value if hasattr(item_data, 'BuyItNowPrice') else None)
        ListingDetails_obj = ListingDetails(self.datetime_to_str(str(item_data.ListingDetails.StartTime)),
                                            item_data.ListingDetails.ViewItemURL if hasattr(item_data.ListingDetails, 'ViewItemURL') else None, 
                                            item_data.ListingDetails.ViewItemURLForNaturalSearch if hasattr(item_data.ListingDetails, 'ViewItemURLForNaturalSearch') else None)
        SellingStatus_obj = SellingStatus(Price(item_data.SellingStatus.CurrentPrice._currencyID, 
                                                item_data.SellingStatus.CurrentPrice.value))
        ShippingDetails_obj = ShippingDetails(item_data.ShippingDetails.ShippingServiceOptions, 
                                            item_data.ShippingDetails.ShippingType)
        ClassifiedAdPayPerLeadFee_obj = Price(item_data.ClassifiedAdPayPerLeadFee._currencyID, 
                                            item_data.ClassifiedAdPayPerLeadFee.value)

        if hasattr(item_data, 'SellerProfiles') and item_data.SellerProfiles:
            SellerShippingProfile_obj = Profile(item_data.SellerProfiles.SellerShippingProfile.ShippingProfileID, 
                                                item_data.SellerProfiles.SellerShippingProfile.ShippingProfileName)
            SellerReturnProfile_obj = Profile(item_data.SellerProfiles.SellerReturnProfile.ReturnProfileID, 
                                            item_data.SellerProfiles.SellerReturnProfile.ReturnProfileName)
            SellerPaymentProfile_obj = Profile(item_data.SellerProfiles.SellerPaymentProfile.PaymentProfileID, 
                                            item_data.SellerProfiles.SellerPaymentProfile.PaymentProfileName)
            SellerProfiles_obj = SellerProfiles(SellerShippingProfile_obj, SellerReturnProfile_obj, SellerPaymentProfile_obj)
        else:
            SellerProfiles_obj = None

        SKU_value = item_data.SKU if hasattr(item_data, 'SKU') else None
        WatchCount_value = item_data.WatchCount if hasattr(item_data, 'WatchCount') else None

        return Listing(BuyItNowPrice_obj, item_data.ItemID, ListingDetails_obj, 
                    item_data.ListingDuration if hasattr(item_data, 'ListingDuration') else None, 
                    item_data.ListingType if hasattr(item_data, 'ListingType') else None, 
                    item_data.Quantity if hasattr(item_data, 'Quantity') else None, 
                    SellingStatus_obj, ShippingDetails_obj, 
                    item_data.TimeLeft if hasattr(item_data, 'TimeLeft') else None, 
                    item_data.Title if hasattr(item_data, 'Title') else None, 
                    item_data.QuantityAvailable if hasattr(item_data, 'QuantityAvailable') else None, 
                    SKU_value, ClassifiedAdPayPerLeadFee_obj, SellerProfiles_obj, 
                    WatchCount_value)


    def fetch_page(self, page_number: int, entries_per_page: int = 100) -> Optional[Dict]:
        """Fetch a single page of eBay listings."""
        try:
            response = self.api.execute('GetMyeBaySelling', {
                'ActiveList': {
                    'Include': True,
                    'Pagination': {
                        'EntriesPerPage': entries_per_page,
                        'PageNumber': page_number
                    }
                },
                "SoldList": {
                    "Include": False
                },
                "UnsoldList": {
                    "Include": False
                }
            })

            if response.reply.Ack == 'Success':
                return response.reply.ActiveList
            else:
                logging.error(f"Error fetching items on page {page_number}: {response.reply.Errors}")
                return None

        except Exception as e:
            logging.error(f"Exception on page {page_number}: {e}")
            return None

    def fetch_all_listings(self, max_retry_attempts: int = 3, backoff_factor: float = 3.0):
        """Fetch all eBay listings with retries and exponential backoff."""
        page_number = 1
        entries_per_page = 200
        retry_attempts = max_retry_attempts

        while True:
            active_list_data = self.fetch_page(page_number, entries_per_page)

            if active_list_data is None:
                if retry_attempts > 0:
                    logging.warning(f"active_list_data is None for page {page_number}. Retrying...")
                    sleep(backoff_factor)
                    backoff_factor *= 2
                    retry_attempts -= 1
                    continue
                else:
                    logging.error("Max retry attempts reached for active_list_data being None.")
                    break

            items = active_list_data.ItemArray.Item
            total_number_of_entries = int(active_list_data.PaginationResult.TotalNumberOfEntries)

            if items:
                for item in items:
                    mapped_item = self.map_api_to_listing(item)
                    self.items.append(mapped_item)

                if len(self.items) >= int(total_number_of_entries):
                    break
                else:
                    page_number += 1
                    retry_attempts = max_retry_attempts
                    backoff_factor = 3.0
            else:
                if retry_attempts > 0:
                    logging.warning(f"No items found on page {page_number}. Retrying...")
                    sleep(backoff_factor)
                    backoff_factor *= 2
                    retry_attempts -= 1
                    continue
                else:
                    logging.error("Max retry attempts reached for no items found.")
                    break

    def datetime_to_str(self, date_str: str) -> str:
        """Convert datetime string to formatted string."""
        matches = re.match(r'datetime.datetime\((\d{4}), (\d+), (\d+), (\d+), (\d+), (\d+)\)', date_str)
        if matches:
            year, month, day, hour, minute, second = matches.groups()
            return f"{year}/{month.zfill(2)}/{day.zfill(2)}-{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}"
        return date_str

    def save_to_json(self, filename: str):
        """Save items to a JSON file."""
        if not self.items:
            logging.warning("No items to save.")
            return
        
        items_data = [vars(item) for item in self.items]

        with open(filename, 'w') as jsonfile:
            json.dump(items_data, jsonfile, indent=4, sort_keys=True, default=complex_encoder)

def complex_encoder(obj):
    """
    A utility function to help serialize complex objects into JSON
    """
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == "__main__":
    APP_ID = 'Midwesth-midwesth-PRD-9b1be8d60-1dc498d1'
    DEV_ID = 'd4d042f7-fe9a-46a3-bfdb-0528f35981f9'
    CERT_ID = 'PRD-b1be8d6003ae-fdf0-4f21-96fe-65b9'
    TOKEN = 'v^1.1#i^1#p^3#f^0#I^3#r^1#t^Ul4xMF8xMTo1NDRGMkE3NTYzNkI4NzExMzRDNTQ5MzcyRDYyMkUwNF8zXzEjRV4yNjA='

    retriever = EbayListingsRetriever(APP_ID, DEV_ID, CERT_ID, TOKEN)
    retriever.fetch_all_listings()
    retriever.save_to_json("ebay-listings.json")