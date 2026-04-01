import scrapy
from stores_info.items import StoresInfoItem
from stores_info.db_config import create_table , insert_into_db


class StoresSpider(scrapy.Spider):
    name = "stores"
    start_urls = [
        "https://stores.burgerking.in/"
    ]
    
    TABLE_NAME = "burgerking_stores"
    
    def start_requests(self):
        create_table(self.TABLE_NAME)
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield from self.parse_bk_state(response)

    def parse_bk_state(self, response):
        state_names = response.xpath("//select[@id='OutletState']/option/@value").getall()

        for state in state_names:
            state = state.strip()

            if not state or state.lower() == "all":
                continue

            state_url = f"https://stores.burgerking.in/location/{state}"
            yield response.follow(state_url, callback=self.parse_bk_city, meta={"state": state})

    def parse_bk_city(self, response):
        state = response.meta["state"]
        city_names = response.xpath("//select[@id='OutletCity']/option/@value").getall()

        for city in city_names:
            city = city.strip()

            if not city or city.lower() == "all":
                continue

            city_url = f"https://stores.burgerking.in/location/{state}/{city}"
            yield response.follow(city_url, callback=self.parse_bk, meta={"state": state, "city": city})

    def parse_bk(self, response):
        base_path = response.xpath("//div[@class='store-info-box']")

        for store in base_path:
            info = StoresInfoItem()
            
            info["brand_name"] = store.xpath("normalize-space(string(.//li[@class='outlet-name']//a))").get()
            info["city"] = response.meta.get("city")
            
            clean_id = store.xpath("normalize-space(.//a[@class='btn btn-website']/@onclick)").get()
            info["store_ID"] = clean_id.split(",")[-1].replace("'", "").replace(")", "").strip() if clean_id else None

            info["store_branch"] = store.xpath("normalize-space(string(.//li[@class='outlet-address']//span[2]))").get()
            address =  store.xpath("normalize-space(string(.//li[@class='outlet-address']//span))").getall()
            info["store_address"] = " ".join(address)

            info["store_phone"] = store.xpath("normalize-space(.//li[@class='outlet-phone']//a/text())").get()
            info["store_timing"] = store.xpath("normalize-space(string(.//li[@class='outlet-timings']))").get()
            info["map_url"] = store.xpath("normalize-space(.//a[@class='btn btn-map']/@href)").get()
            info["store_url"] = store.xpath("normalize-space(.//a[@class='btn btn-website']/@href)").get()
            info["menu"] = None

            info["page_url"] = response.url
            
            insert_into_db(self.TABLE_NAME, dict(info))

            yield info
            
