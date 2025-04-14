# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductItem(scrapy.Item):
    seller   = scrapy.Field()
    name     = scrapy.Field()
    price    = scrapy.Field()
    url      = scrapy.Field()
    ean      = scrapy.Field()
    date_now = scrapy.Field()