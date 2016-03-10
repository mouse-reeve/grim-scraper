''' Scrapes content out of grimoires hosted on sacred texts '''
import re
import scrapy
from grim_scraper.items import GrimItem

class SacredTextsSpider(scrapy.Spider):
    ''' Defines the behavior of the crawling spider '''
    name = 'SacredTexts'
    allowed_domains = ['sacred-texts.com']
    start_urls = ['http://www.sacred-texts.com/ame/pow/index.htm']

    def parse(self, response):
        ''' reads pages' markup '''
        for link in response.xpath('//a/@href'):
            path = link.extract()
            if re.match(r'pow\d\d\d.htm', path):
                yield scrapy.http.Request('http://www.sacred-texts.com/ame/pow/' + path)

        item = GrimItem()

        item['grimoire'] = 'long lost friend'
        item['source'] = response.url
        try:
            item['title'] = response.xpath('//title/text()').extract()[0].split(': ')[-1]
        except IndexError:
            return
        item['text'] = '\n'.join(response.xpath('//p/text()').extract()[1:])
        item['number'] = item['source'].split('.htm')[0][-3:]

        item = {key:value for key, value in item.iteritems() if value}
        if len(item) > 1:
            yield item

