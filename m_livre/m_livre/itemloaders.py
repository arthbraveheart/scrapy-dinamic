from itemloaders.processors import TakeFirst, MapCompose, Identity, Compose
from scrapy.loader import ItemLoader
from datetime import datetime
import re


def extract_name(dumped_json):
    pattern = re.compile(r'"name":"(.*?)"')
    return re.findall(pattern, dumped_json) or []


def extract_url(dumped_json):
    pattern = re.compile(r'"url":"(.*?)"')
    return re.findall(pattern, dumped_json) or []


def extract_price(dumped_json):
    pattern = re.compile(r'"price":"(\d+\.\d{2}|\d+)"')
    return re.findall(pattern, dumped_json) or []

def validate_ean(ean):
    # Ensure EAN is converted to integer and handle possible string inputs
    try:
        return int(ean)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid EAN value: {ean}")

class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # Input processors with type conversions
    name = MapCompose(lambda x: extract_name(x))
    price = MapCompose(lambda x: extract_price(X))
    url = MapCompose(lambda x: extract_url(x))
    ean = MapCompose(lambda x: validate_ean(x))
    date_now = MapCompose(lambda x: x)#datetime.strptime(x, "%d-%m-%Y"))

