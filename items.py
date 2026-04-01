# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StoresInfoItem(scrapy.Item):
    # define the fields for your item here like:
    brand_name = scrapy.Field()
    city = scrapy.Field()
    store_ID = scrapy.Field()
    store_branch = scrapy.Field()
    store_address = scrapy.Field()
    store_phone = scrapy.Field()
    store_timing = scrapy.Field()
    map_url = scrapy.Field()
    store_url = scrapy.Field()
    menu = scrapy.Field()
    page_url = scrapy.Field()
    
    
    
