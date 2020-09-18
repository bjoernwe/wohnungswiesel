import scrapy

from scrapy import Request
from scrapy.http import TextResponse
from typing import Optional


class QuotesSpider(scrapy.Spider):

    name = "quotes"

    #start_urls = [
    #    'http://quotes.toscrape.com/page/1/',
    #    'http://quotes.toscrape.com/page/2/',
    #]

    def start_requests(self) -> Optional[Request]:
        urls = [
            'https://www.wbm.de/wohnungen-berlin/angebote/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
