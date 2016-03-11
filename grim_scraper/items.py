''' defines what data will be collected '''
import scrapy

class GrimItem(scrapy.Item):
    ''' metadata about a book '''
    identifier = scrapy.Field()
    text = scrapy.Field()
    grimoire = scrapy.Field()
    source = scrapy.Field()
    label = scrapy.Field()
