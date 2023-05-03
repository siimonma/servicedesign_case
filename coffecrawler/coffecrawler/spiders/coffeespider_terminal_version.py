import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
import time
from coffecrawler.items import CoffeeProduct
from coffecrawler.itemloaders import CoffeeProductLoader

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
            yield scrapy.Request(url, self.parse)

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
                    yield product_loader.load_item()

            # Scroll down to load more content
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            # Check if reaching the end of the page
            end_of_page = self.driver.find_elements(By.XPATH, "//div[@class='product-listing-container']/p[contains(text(), 'End of page')]")
            if time.time() - start_time >= 5:
                break