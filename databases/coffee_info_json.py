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

    def coffee_exists(self, coffee_id: str) -> bool:
        """Checks coffee database to see if coffee id exists"""
        search_result = self.get_coffee(coffee_id=coffee_id)
        if len(search_result['coffee']) != 0:
            return True
        return False

    def get_coffee(self, coffee_id: str):
        return self.get_coffee_search(coffee_id=coffee_id)

    @staticmethod
    def get_all_coffee():
        return {'coffee': CoffeInfoJSON.get_json_file_data()}

    @staticmethod
    def get_json_file_data():
        """Gets the information held in JSON database file"""
        with open(PATH_TO_JSON_FILE, 'r', encoding='utf-8') as file:
            file_data = json.load(file)
            return file_data

    def get_coffee_search(self, search_word: str = None, coffee_id: str = None):
        coffee_dict = self.get_all_coffee()
        search_result = {'coffee': []}
        for coffee in coffee_dict['coffee']:
            if search_word:
                if search_word.strip().lower() in coffee['name'].strip().lower():
                    search_result['coffee'].append(coffee)
            if coffee_id:
                if coffee_id == coffee['id']:
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
        with open(PATH_TO_JSON_FILE, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        item['id'] = item['id'][0]  # Save the ID as a str and not a list.
        self.data.append(dict(item))
        return item


if __name__ == '__main__':
    CoffeInfoJSON(initiate=False).coffee_exists('7310731101611')
    # pprint(CoffeInfoJSON(initiate=False).get_all_coffee())
