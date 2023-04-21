from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class CoffeeProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    url_in = MapCompose(lambda x: 'http://nybryggt.nu/kaffe' + x)