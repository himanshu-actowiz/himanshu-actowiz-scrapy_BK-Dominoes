import scrapy
from stores_info.items import StoresInfoItem
from stores_info.db_config import create_table, insert_into_db


class StoresDominoesSpider(scrapy.Spider):
    name = "stores_dominoes"
    allowed_domains = ["www.dominos.co.in"]
    start_urls = ["https://www.dominos.co.in/store-location/"]

    TABLE_NAME = "dominos_stores"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_store_urls = set()

    def start_requests(self):
        create_table(self.TABLE_NAME)
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield from self.parse_dominoes_cities(response)

    def parse_dominoes_cities(self, response):
        store_urls = response.xpath("//li//a[@class='citylink']/@href").getall()

        for url in store_urls:
            if not url or not url.strip():
                continue

            city_url = response.urljoin(url)
            city_name = url.strip("/").split("/")[-1]

            yield response.follow(city_url, callback=self.parse_dominoes, meta={"city": city_name})

    def parse_dominoes(self, response):
        base_path = response.xpath("//div[@class='panel panel-default custom-panel']")

        for stores in base_path:
            store = StoresInfoItem()

            store["brand_name"] = stores.xpath("normalize-space(string(.//div[@class='media-body']//h2))").get()
            store["city"] = response.meta.get("city")
            store["store_ID"] = None

            store["store_branch"] = stores.xpath("normalize-space(string(.//div[@class='media-body']//p[@class='city-main-sub-title']))").get()
            store["store_address"] = stores.xpath("normalize-space(string(.//div[@class='media-body']//p[@class='grey-text mb-0']))").get()
            store["store_phone"] = stores.xpath("normalize-space(string(.//div[contains(@class,'modal-body')]//p[@class='fontsize2 bold zred']))").get()
            store["store_timing"] = stores.xpath("normalize-space(string(.//div[contains(@class,'res-timing')]//div[contains(@class,'search-grid-right-text')]))").get()
            store["map_url"] = None

            store_url = stores.xpath(".//a[contains(@href,'/store-location/')]/@href").get()
            store["store_url"] = response.urljoin(store_url) if store_url else None

            menu_url = stores.xpath(".//a[contains(text(),'Menu')]/@href").get()
            store["menu"] = response.urljoin(menu_url) if menu_url else None

            store["page_url"] = response.url

            if store["store_url"] in self.seen_store_urls:
                continue

            self.seen_store_urls.add(store["store_url"])

            insert_into_db(self.TABLE_NAME, dict(store))
            yield store