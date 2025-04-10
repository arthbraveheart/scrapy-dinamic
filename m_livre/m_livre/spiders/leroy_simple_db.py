import scrapy
from scrapy_playwright.page import PageMethod
import re
import csv
import time
from .tools import load_pkl
from .settings import out_path
from m_livre.items import ProductItem

class MLSpider(scrapy.Spider):
    name = 'leroy_simple_db'
    today = time.strftime("%d-%m-%Y")
    search = load_pkl('dular_eans')#.iloc[:20,:]
    base_url = 'https://www.leroymerlin.com.br/search?term={}&searchTerm={}&searchType=EAN'

    def start_requests(self):
        for i, row in self.search.iterrows():
            ean = row['Ean']
            url = self.base_url.format(ean,ean)
            yield scrapy.Request(
                url,
                meta={
                    #"proxy": 'https://bravebrave_xJSab:Proxy_1728_Brave@unblock.oxylabs.io:60000',
                    "ean": ean,
                    "dont_verify_ssl": True,
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