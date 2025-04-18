import scrapy
from scrapy_playwright.page import PageMethod
import re
import csv
import time
from .tools import load_pkl
from .settings import out_path
from ..items import ProductItem

class MLSpider(scrapy.Spider):
    name = 'ml_simple_db'
    today = time.strftime("%d-%m-%Y")
    search = load_pkl('dular_eans')#.iloc[:20,:]
    base_url = 'https://lista.mercadolivre.com.br/{}#D[A:{}]'

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
        ean = response.meta["ean"]
        element = response.xpath('//script[@type="application/ld+json"]/text()').get()
        names, prices, urls = self.get_things_done(element)
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


    def get_things_done(self, element):
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

    def save_to_csv(self, linha):
        with open(f"{out_path}/Prices_Magalu_{self.today}.csv", "a", newline="", encoding="utf-8-sig") as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow(linha)