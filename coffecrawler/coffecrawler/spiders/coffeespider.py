import scrapy
from coffecrawler.items import CoffeeProduct
from coffecrawler.itemloaders import CoffeeProductLoader

class CoffeespiderSpider(scrapy.Spider):

    name = "coffeespider"

    allowed_domains = ["nybryggt.nu"]
    start_urls = ["http://nybryggt.nu/kaffe"]

    def parse(self, response):
        products = response.css('div.l-main')

        for product in products:
            products = CoffeeProductLoader(item=CoffeeProduct(), selector=product)
            products.add_css('name', 'div.product-item__body h3::text')
            products.add_css('url', 'div.product-item__img img::attr(src)')
            # print(products)
            yield products.load_item()

