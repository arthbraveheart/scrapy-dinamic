import scrapy
from scrapy_playwright.page import PageMethod
import re
import csv
import time
from .tools import url_encoded
from m_livre.items import ProductItem
from ..settings import DATABASE_URI
from sqlalchemy import create_engine, text
from contextlib import closing
from urllib.parse import urlencode

class MLSpider(scrapy.Spider):
    name = 'madeira_simple_db'
    today = time.strftime("%d-%m-%Y")
    base_url = 'https://www.madeiramadeira.com.br/busca'
    engine = create_engine(DATABASE_URI)

    def start_requests(self):
        with closing(self.engine.connect()) as conn:

            result = conn.execution_options(stream_results=True).execute(
                text("""SELECT description,ean FROM "dular_eans" """)
            )

            for row in result:
                ean = row[1]
                product_name = row[0]
                url = url_encoded(self.base_url,product_name)
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
            products_items['seller'] = 'Madeira Madeira'
            products_items['name'] =  name.strip()
            products_items['price'] = price
            products_items['url'] = response.url
            products_items['ean'] = response.meta["ean"]
            yield products_items
        else:
            print("****************** Fail to get PRICE *******************")

    def get_things_done(element):

        try:

            json_loads = element
            pattern_price = re.compile(r'R\$(\d+\.\d+\,\d{2}|\d+\,\d{2}|\d+)')
            pattern_name = re.compile(r'(.*?)R\$')
            prices = re.findall(pattern_price, json_loads)[0]
            names = re.findall(pattern_name, json_loads)[0]
            return names, prices

        except:
            print("****************** Fail to get PRICE *******************")
            return 'empty', 0