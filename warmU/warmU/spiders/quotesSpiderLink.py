import scrapy

# Modified Spider to recursively follow the link to the new page. The parse() method looks for the link to the next page, builds a full absolute URL using the urljoin() method and yields a new request to the next page, registering itself as callback to handle the data extraction for the next page and to keep crawling going through all the pages.

class QuotesSpider(scrapy.Spider):
    name = "quotesLink"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
        # recursively follow the link to the next page. Extract data from it.
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)