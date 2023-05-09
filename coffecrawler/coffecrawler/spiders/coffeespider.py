import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from scrapy.exporters import JsonItemExporter
from case_project.coffecrawler.coffecrawler.items import CoffeeProduct
from case_project.coffecrawler.coffecrawler.itemloaders import CoffeeProductLoader


class CoffeespiderSpider(scrapy.Spider):
    name = "coffeespider"
    allowed_domains = ["www.dittsvenskaskafferi.se"]
    start_urls = ["https://www.dittsvenskaskafferi.se/svensk-mat/dryck/kaffe"]

    def __init__(self, *args, **kwargs):
        super(CoffeespiderSpider, self).__init__(*args, **kwargs)
        self.driver = None
        self.scraped_urls = set()

    def start_requests(self):
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        start_time = time.time()

        while True:
            sel = Selector(text=self.driver.page_source)
            products = sel.css('a.product-item-link')

            for product in products:
                product_url = product.attrib['href']
                if product_url not in self.scraped_urls:
                    self.scraped_urls.add(product_url)
                    product_loader = CoffeeProductLoader(item=CoffeeProduct(), selector=product)
                    product_loader.add_css('name', '::text')
                    product_loader.add_css('url', '::attr(href)')
                    product_loader.add_css('id', '::attr(href)')
                    yield product_loader.load_item()

            # Scroll down to load more content
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            # Break the endless loop
            if time.time() - start_time >= 5:
                break

