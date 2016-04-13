''' Scrapes content out of grimoires hosted on sacred texts '''
import re
import scrapy
from grim_scraper.items import GrimItem

class SacredTextsSpider(scrapy.Spider):
    ''' Defines the behavior of the crawling spider '''
    name = 'SacredTexts'
    allowed_domains = ['sacred-texts.com']
    start_urls = ['http://www.sacred-texts.com/grim/kos/index.htm']

    def parse(self, response):
        ''' reads pages' markup '''
        for link in response.xpath('//a/@href'):
            path = link.extract()
            if re.match(r'kos\d\d.htm', path):
                yield scrapy.http.Request('http://www.sacred-texts.com/grim/kos/' + path)

        item = GrimItem()

        item['grimoire'] = 'Key of Solomon'
        item['label'] = 'spell'
        item['source'] = response.url
        try:
            item['identifier'] = response.xpath('//title/text()').extract()[0].split(': ')[-1]
        except IndexError:
            return
        item['text'] = '\n'.join(response.xpath('///text()').extract())

        item = {key:value for key, value in item.iteritems() if value}
        if len(item) > 1:
            yield item

