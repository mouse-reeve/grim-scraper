''' Scrapes data on books in a librarything user's collection '''
import re
import scrapy
from grim_scraper.items import GrimItem

class SacredTextsSpider(scrapy.Spider):
    ''' Defines the behavior of the crawling spider '''
    name = 'SacredTexts'
    allowed_domains = ['librarything.com']
    start_urls = ['https://www.librarything.com/catalog_bottom.php?view=tripofmice']

    def parse(self, response):
        ''' reads pages' markup '''
        for link in response.xpath('//a/@href'):
            path = link.extract()
            if re.match(r'\/work\/\d+\/book\/\d+', path)\
                    or re.match(r'\/catalog_bottom.php\?view\=tripofmice\&offset=\d+', path):
                yield scrapy.http.Request('https://www.librarything.com/' + path)

        item = GrimItem()

        try:
            item['isbn'] = response.xpath('//meta[@property="books:isbn"]/@content').extract()[0]
        except IndexError:
            pass

        # About page (with common knowledge)
        table = response.xpath('//div[@id="fwikiContainerTablediv"]//tr')
        for row in table:
            rowData = row.extract()
            if 'Original publication date' in rowData:
                try:
                    year = row.xpath('.//a/text()').extract()[0]
                    # normalizes dates assuming the formats YYYY-MM-DD or
                    # YYYY-YY, both of which I've seen in the data.
                    year = year[0:4]
                    item['date_first_published'] = year
                except IndexError:
                    pass

            elif 'Important places' in rowData:
                item['places'] = row.xpath('.//div[@class="fwikiAtomicValue"]//a/text()').extract()

            elif 'People/Characters' in rowData:
                item['characters'] = row.xpath('.//div[@class="fwikiAtomicValue"]//a/text()') \
                                        .extract()

            elif 'Important events' in rowData:
                item['events'] = row.xpath('.//div[@class="fwikiAtomicValue"]//a/text()').extract()

        if item:
            item = {key:value for key, value in item.iteritems() if value}
            if len(item) > 1:
                yield item

