import scrapy
from scrapy_playwright.page import PageMethod
import re
import csv
import time
from .tools import load_pkl
from .settings import out_path

class MagaluSpider(scrapy.Spider):
    name = 'magalu_spider'
    today = time.strftime("%d-%m-%Y")
    search = load_pkl('dular_eans')
    base_url = 'https://www.magazineluiza.com.br/busca/{}/?from=submit'

    def start_requests(self):
        for i, row in self.search.iterrows():
            ean = row['Ean']
            url = self.base_url.format(ean, ean)
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", 'script[type="application/ld+json"]'),
                        PageMethod("wait_for_timeout", 5000),
                    ],
                    "row": row,
                },
                callback=self.parse
            )

    async def parse(self, response):
        row = response.meta["row"]
        element = response.xpath('//script[@type="application/ld+json"]/text()').get()
        names, prices = self.get_things_done(element)
        for name, price in zip(names, prices):
            if name != 'empty':
                linha = [name, price.replace('.', ','), response.url] + row.to_list()
                self.save_to_csv(linha)
            else:
                continue

    def get_things_done(self, element):
        try:
            pattern_price = re.compile(r'"price":(\d+\.\d{2}|\d+)')
            pattern_name = re.compile(r'"Product","name":"(.*?)"')
            prices = re.findall(pattern_price, element)
            names = re.findall(pattern_name, element)
            return names, prices
        except:
            print("****************** Fail to get PRICE *******************")
            return ['empty'], ['empty']

    def save_to_csv(self, linha):
        with open(out_path + f"Prices_M_Livre_{self.today}.csv", "a", newline="", encoding="utf-8-sig") as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow(linha)