from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


def extract_id(value):
    return value[-13:]  # Extract the last 13 characters


class CoffeeProductLoader(ItemLoader):
    name_out = TakeFirst()
    url_out = TakeFirst()
    id_out = MapCompose(extract_id)  # Get the ID from the last 13 chars from the URL
