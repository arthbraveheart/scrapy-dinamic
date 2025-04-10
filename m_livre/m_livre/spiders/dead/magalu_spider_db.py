import scrapy
from scrapy_playwright.page import PageMethod
from itemloaders.processors import TakeFirst
import re
import time
from m_livre.m_livre.spiders.tools import load_pkl
from m_livre.items import ProductItem
from m_livre.itemloaders import ProductLoader


class MagaluSpider(scrapy.Spider):
    name = 'magalu_spider_db'
    today = time.strftime("%d-%m-%Y")
    search = load_pkl('dular_eans')
    base_url = 'https://www.magazineluiza.com.br/busca/{}/?from=submit'

    def start_requests(self):
        for i, row in self.search.iterrows():
            yield scrapy.Request(
                url=self.base_url.format(row['Ean']),
                headers={"x-oxylabs-geo-location": "Brazil"},
                meta={
                    "proxy": 'https://bravebrave_xJSab:Proxy_1728_Brave@unblock.oxylabs.io:60000',
                    "row": row,
                    "dont_verify_ssl": True,
                },
                callback=self.parse
            )

    async def parse(self, response):
        row = response.meta["row"]
        element = response.xpath('//script[@type="application/ld+json"]/text()').get()

        # Use ItemLoader to process the data
        loader = ProductLoader(item=ProductItem(), response=response)
        loader.add_value('name', element)
        loader.add_value('price', element)
        loader.add_value('url', element)
        loader.add_value('ean', row['Ean'])
        loader.add_value('date_now', self.today)
        yield loader.load_item()



