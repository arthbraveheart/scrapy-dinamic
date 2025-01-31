import scrapy
from scrapy_playwright.page import PageMethod
import re
import csv
import time
from .tools import load_pkl
from .settings import out_path

class MercadoLivreSpider(scrapy.Spider):
    name = 'mercado_livre'
    today = time.strftime("%d-%m-%Y")
    search = load_pkl('dular_eans')#.iloc[:100,:]
    base_url = 'https://lista.mercadolivre.com.br/{}#D[A:{}]'

    def start_requests(self):
        for i, row in self.search.iterrows():
            ean = row['Ean']
            url = self.base_url.format(ean, ean)
            yield scrapy.Request(
                url,
                meta={

                    "row": row,
                },
                callback=self.parse
            )

    async def parse(self, response):
        row = response.meta["row"]
        element = response.xpath('//script[@type="application/ld+json"]/text()').get()
        names, prices, urls = self.get_things_done(element)
        for name, price, url in zip(names, prices, urls):
            if name != 'empty':
                linha = [name, price.replace('.', ','), url] + row.to_list()
                self.save_to_csv(linha)
            else:
                continue

    def get_things_done(self, element):
        try:
            pattern_price = re.compile(r'"price":"(\d+\.\d{2}|\d+)"')
            pattern_name = re.compile(r'"Product","name":"(.*?)"')
            pattern_url = re.compile(r'"url":"(.*?)"')
            prices = re.findall(pattern_price, element)
            names = re.findall(pattern_name, element)
            url = re.findall(pattern_url, element)
            return names, prices, url
        except:
            print("****************** Fail to get PRICE *******************")
            return ['empty'], ['empty'], ['empty']

    def save_to_csv(self, linha):
        with open(f"{out_path}/Prices_M_Livre_{self.today}.csv", "a", newline="", encoding="utf-8-sig") as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow(linha)