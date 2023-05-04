import json
import os
from case_project.coffecrawler.coffecrawler.spiders.coffeespider import CoffeespiderSpider
from scrapy.crawler import CrawlerProcess
from pprint import pprint

PATH_TO_JSON_FILE = os.path.abspath(os.path.dirname(__file__)) + '/data.json'


class CoffeInfoJSON:

    def __init__(self, initiate: bool):
        if initiate:
            self.init_json_file()
        pass

    @staticmethod
    def init_json_file():
        process = CrawlerProcess(settings={
            'ITEM_PIPELINES': {
                f'{__name__}.SaveToJSON': 300,
            },
            'FEED_EXPORT_ENCODING': 'utf-8',
        })
        process.crawl(CoffeespiderSpider)
        process.start()

    def get_coffee(self, coffee_id: int):
        pass

    @staticmethod
    def get_all_coffee():
        return {'coffee': CoffeInfoJSON.get_json_file_data()}

    @staticmethod
    def get_json_file_data():
        """Gets the information held in JSON database file"""
        with open(PATH_TO_JSON_FILE, 'r', encoding='utf-8') as file:
            file_data = json.load(file)
            return file_data

    def get_coffee_search(self, search_word: str):
        coffee_dict = self.get_all_coffee()
        search_result = {'coffee': []}
        for coffee in coffee_dict['coffee']:
            if search_word.strip().lower() in coffee['name'].strip().lower():
                search_result['coffee'].append(coffee)
        return search_result

    def add_coffee(self, name, url):
        pass


class SaveToJSON:
    def __init__(self):
        self.data = None

    def open_spider(self, spider):
        self.data = []

    def close_spider(self, spider):
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        item['id'] = item['id'][0]  # Save the ID as a str and not a list.
        self.data.append(dict(item))
        return item


if __name__ == '__main__':
    pprint(CoffeInfoJSON(initiate=False).get_all_coffee())
