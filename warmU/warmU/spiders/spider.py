import scrapy
from scrapy.spiders import XMLFeedSpider

try:
    from ..items import WarmuItem
except Exception: #ImportError
    from warmU.warmU.items import WarmuItem


class SiteSpider(scrapy.Spider):
    name = "site"
    allowed_domains = ['www.w3schools.com']
    start_urls = ["http://www.w3schools.com/xml/"]
    itertag = 'note'

    # need to instantiate a WarmuItem
    def parse_node(self, selector):
        item = WarmuItem()
        item['to'] = selector.xpath('//to/text()').extract()
        item['who'] = selector.xpath('//from/text()').extract()
        item['heading'] = selector.xpath('//heading/text()').extract()
        item['body'] = selector.xpath('//body/text()').extract()
        return item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//p")
        for titles in titles:
            title = titles.select("a/text()").extract() # XPath to call the text for the tile
            link = titles.select("@/href").extract()
            print(title, link)

