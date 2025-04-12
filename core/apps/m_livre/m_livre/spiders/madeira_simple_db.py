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
from urllib.parse import urlencode, quote


# Modify your spider class with these changes
class MLSpider(scrapy.Spider):
    name = 'madeira_simple_db'
    today = time.strftime("%d-%m-%Y")
    base_url = 'https://www.madeiramadeira.com.br/busca?{}'
    engine = create_engine(DATABASE_URI)
    custom_settings = {
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            "headless": True,
            "timeout": 60000,
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage",  # Only include necessary args
            ],
        },
        'PLAYWRIGHT_MAX_CONTEXTS': 4,  # Limit concurrent contexts
        'DOWNLOAD_TIMEOUT': 60,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
    }

    def start_requests(self):
        with closing(self.engine.connect()) as conn:
            result = conn.execution_options(stream_results=True).execute(
                text("""SELECT description,ean FROM "dular_eans" """)
            )

            for row in result:
                ean = row[1]
                product_name = str(row[0]).strip()
                params = {'q': product_name}
                encoded_query = quote(product_name)
                url = f"{self.base_url}?q={encoded_query}"
                yield scrapy.Request(
                    url,
                    meta={
                        "ean": ean,
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_timeout", 2000),
                            #PageMethod("wait_for_selector", "div.product-card", timeout=45000),
                            #PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                            #PageMethod("wait_for_selector", "span[class*='price']", state="attached", timeout=45000)
                        ],
                        "playwright_page_event_handlers": {
                            "response": self.handle_response,
                        },
                        "playwright_include_page": True,
                    },
                    errback=self.errback,
                    callback=self.parse
                )


    async def parse(self, response):
        page = response.meta["playwright_page"]
        try:


            # Extract data from properly loaded page
            name = response.xpath(
                "//h2[@class='cav--c-gNPphv cav--c-gNPphv-epiGtV-textStyle-bodySmallRegular cav--c-gNPphv-iAsWAM-css']/text()").get()
            price = response.xpath(
                '//span[@class="cav--c-gNPphv cav--c-gNPphv-kQaGxl-size-h4 cav--c-gNPphv-hyvuql-weight-bold cav--c-gNPphv-ihtexkH-css"]/text()').get()

            if price:
                products_items = ProductItem()
                products_items['seller'] = 'Madeira Madeira'
                products_items['name'] = name.strip() if name else None
                products_items['price'] = price.replace('R$', '').replace('.', '').replace(',', '.').strip()
                products_items['url'] = response.url
                products_items['ean'] = response.meta["ean"]
                yield products_items
            else:
                self.logger.warning("****************** Fail to get PRICE *******************")
                self.logger.debug(f"Failed URL: {response.url}")

        finally:
            await page.close()

    async def handle_response(self, response):
        # Monitor network responses
        if "api" in response.url:
            self.logger.debug(f"API response: {response.url} ({response.status})")

    def errback(self, failure):
        # Handle failed requests
        self.logger.error(f"Request failed: {failure.request.url}")
        if failure.check(TimeoutError):
            self.logger.warning("Timeout occurred, consider increasing wait times")