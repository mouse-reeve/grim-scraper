''' defines what data will be collected '''
import scrapy

class GrimItem(scrapy.Item):
    ''' metadata about a book '''
    title = scrapy.Field()
    text = scrapy.Field()
    number = scrapy.Field()
    grimoire = scrapy.Field()
    source = scrapy.Field()
