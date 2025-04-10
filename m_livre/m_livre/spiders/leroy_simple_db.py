import scrapy
from scrapy_playwright.page import PageMethod
import re
import csv
import time
from .settings import out_path
from m_livre.items import ProductItem
from ..settings import DATABASE_URI
from sqlalchemy import create_engine, text
from contextlib import closing

class MLSpider(scrapy.Spider):
    name = 'leroy_simple_db'
    today = time.strftime("%d-%m-%Y")
    base_url = 'https://www.leroymerlin.com.br/search?term={}&searchTerm={}&searchType=EAN'
    engine = create_engine(DATABASE_URI)

    def start_requests(self):
        with closing(self.engine.connect()) as conn:
            # Use stream_results for PostgreSQL
            result = conn.execution_options(stream_results=True).execute(
                text("""SELECT ean FROM "dular_eans" """)  # Only get needed column
            )

            # Use itertools.islice for chunking if needed
            for row in result:
                ean = row[0]  # Access by index for better performance
                url = self.base_url.format(ean, ean)
                yield scrapy.Request(
                    url,
                    meta={
                        "ean": ean,
                        "dont_verify_ssl": True,
                        #"db_row": dict(row)  # Optional: preserve row data
                    },
                    callback=self.parse
                )

    async def parse(self, response):
        name = response.xpath("//h1[@itemprop='name']/text()").get()
        price = response.css("div.product-title-container::text").get()
        if price and price.strip()!='':
            products_items = ProductItem()
            products_items['seller'] = 'Leroy Merlin'
            products_items['name'] =  name.strip()
            products_items['price'] = price
            products_items['url'] = response.url
            products_items['ean'] = response.meta["ean"]
            yield products_items
        else:
            print("****************** Fail to get PRICE *******************")