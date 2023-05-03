from scrapy.crawler import CrawlerProcess
from coffecrawler.coffecrawler.spiders.coffeespider import CoffeespiderSpider
import json


class Utf8JsonPipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        self.file = open('databases/data.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


process = CrawlerProcess(settings={
    'ITEM_PIPELINES': {
        '__main__.Utf8JsonPipeline': 300,
    },
    'FEED_EXPORT_ENCODING': 'utf-8',
})

process.crawl(CoffeespiderSpider)
process.start()