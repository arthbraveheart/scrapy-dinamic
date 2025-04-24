import scrapy
from scrapy_playwright.page import PageMethod
import re
import csv
import time
from .tools import load_pkl
from .settings import out_path
from ..items import ProductItem
from ..settings import DATABASE_URI
from sqlalchemy import create_engine, text
from contextlib import closing

class MLNewSpider(scrapy.Spider):
    name = 'ml_curva'
    today = time.strftime("%d-%m-%Y")
    #search = load_pkl('dular_eans')#.iloc[:20,:]
    base_url = 'https://lista.mercadolivre.com.br/{}#D[A:{}]'
    engine = create_engine(DATABASE_URI)

    def __init__(self, eans=None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.eans = eans

    def start_requests(self):
        """
        Generate scrapy requests for each EAN code retrieved from the database.
        If specific EANs are provided during initialization, only those are queried.
        Otherwise, all EANs from the 'dular_eans' table are used.
        """
        with closing(self.engine.connect()) as conn:
            eans_query = self._build_eans_query()
            query_params = self._get_query_params()

            # Execute query with streaming for memory efficiency
            result = conn.execution_options(stream_results=True).execute(
                text(eans_query), parameters=query_params
            )

            # Process each EAN code
            for row in result:
                ean = row[0]  # Access by index for better performance
                url = self.base_url.format(ean, ean)
                yield scrapy.Request(
                    url,
                    meta={
                        "ean": ean,
                        "dont_verify_ssl": True,
                    },
                    callback=self.parse
                )

    async def parse(self, response):
        ean = response.meta["ean"]
        element = response.xpath('//script[@type="application/ld+json"]/text()').get()
        names, prices, urls = self._get_things_done(element)
        for name, price, url in zip(names, prices, urls):
            if name != 'empty':
                linha = dict(name=name, price=price.replace('.', ','), url=url, ean=ean, ) #+ row.to_list()
                #products_items = ProductItem(**linha)
                products_items = ProductItem()
                products_items['seller'] = 'Mercado Livre'
                products_items['name'] = name
                products_items['price'] = price#.replace('.', ',')
                products_items['url'] = url.replace('\\u002F','/')
                products_items['ean'] = ean
                yield products_items
                #self.save_to_csv(linha)


    def _get_things_done(self, element):
        try:
            pattern_price = re.compile(r'"price":(\d+\.\d{2}|\d+)')
            pattern_name = re.compile(r'"Product","name":"(.*?)"')
            pattern_url = re.compile(r'"url":"(.*?)"')
            prices = re.findall(pattern_price, element)
            names = re.findall(pattern_name, element)
            url = re.findall(pattern_url, element)
            return names, prices, url
        except:
            print("****************** Fail to get PRICE *******************")
            return ['empty'] , ['empty'] , ['empty']

    def _save_to_csv(self, linha):
        with open(f"{out_path}/Prices_Magalu_{self.today}.csv", "a", newline="", encoding="utf-8-sig") as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow(linha)

    def _build_eans_query(self):
        """Build the appropriate SQL query based on whether specific EANs were provided"""
        if self.eans:
            return """SELECT ean \
                      FROM "dular_eans" \
                      WHERE ean IN :eans"""
        else:
            return """SELECT ean \
                      FROM "dular_eans" """

    def _get_query_params(self):
        """Return query parameters dictionary if needed, otherwise empty dict"""
        if self.eans:
            return {'eans': tuple(self.eans)}
        return {}
