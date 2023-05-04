from scrapy.crawler import CrawlerProcess
from coffecrawler.coffecrawler.spiders.coffeespider import CoffeespiderSpider
import json


class SaveToJSON:
    def open_spider(self, spider):
        self.data = []

    def close_spider(self, spider):
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        item['id'] = item['id'][0]  # Save the ID as a str and not a list.
        self.data.append(dict(item))
        return item


process = CrawlerProcess(settings={
    'ITEM_PIPELINES': {
        '__main__.SaveToJSON': 300,
    },
    'FEED_EXPORT_ENCODING': 'utf-8',
})

process.crawl(CoffeespiderSpider)
process.start()
