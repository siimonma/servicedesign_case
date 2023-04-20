import scrapy


class CoffeespiderSpider(scrapy.Spider):

    name = "coffeespider"

    allowed_domains = ["nybryggt.nu"]
    start_urls = ["http://nybryggt.nu/kaffe"]

    def parse(self, response):
        pass

