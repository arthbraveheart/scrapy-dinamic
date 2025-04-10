import scrapy
from scrapy_playwright.page import PageMethod
import re
import csv
import time
from .tools import load_pkl
from .settings import out_path
from m_livre.items import ProductItem
from ..settings import DATABASE_URI
from sqlalchemy import create_engine, text
from contextlib import closing


class CarrefaSpider(scrapy.Spider):
    name = 'carrefas_simple_db'
    today = time.strftime("%d-%m-%Y")
    search = load_pkl('dular_eans')#.iloc[:20,:]
    base_url = 'https://www.carrefour.com.br/busca/{}'
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
                        # "db_row": dict(row)  # Optional: preserve row data
                    },
                    callback=self.parse
                )

    async def parse(self, response):
        ean = response.meta["ean"]
        names = response.xpath('//h2[@class="text-xs leading-4 text-[#333] text-left my-3 truncate-text h-12"]/text()').getall()
        prices = response.xpath('//span[@class="text-base font-bold text-primary"]/text()').getall()
        urls = response.xpath('//a[@class="border rounded-lg border-[#f2f2f2] p-2 cursor-pointer overflow-hidden hover:shadow-md undefined flex flex-col gap-4"]/@href').getall()

        for name, price, url in zip(names, prices, urls):
            if name:
                #linha = dict(name=name, price=price.replace('.', ','), url=url, ean=ean, ) #+ row.to_list()
                #products_items = ProductItem(**linha)
                products_items = ProductItem()
                products_items['seller'] = 'Carrefour'
                products_items['name'] = name
                products_items['price'] = price.replace('R$','').replace('.','').replace(',','.').strip()
                products_items['url'] = f'https://www.carrefour.com.br{url}'
                products_items['ean'] = ean
                yield products_items
                #self.save_to_csv(linha)
