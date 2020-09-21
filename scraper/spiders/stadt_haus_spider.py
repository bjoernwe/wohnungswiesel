import logging
import scrapy
import urllib
import urllib.parse

from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable

from scraper.items import FlatItem


log = logging.getLogger('stadt_haus_spider')


class StadtHausSpider(scrapy.Spider):

    name = "stadt-haus"

    _query_params = {
        'field_woh_zimmer_value': 2,
        'sort_bef_combine': 'field_woh_gesamtmiete_value ASC',
        'tid[]': [6, 8, 14, 19, 20, 23, 25, 28, 29, 30, 32, 34]
    }

    def start_requests(self) -> Iterable[Request]:
        api_endpoint = 'https://stadt-haus.com/de/mietobjekte/wohnen-ergebnisse'
        query_args = urllib.parse.urlencode(self._query_params, doseq=True)
        url = f'{api_endpoint}?{query_args}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> FlatItem:
        for result in response.xpath('//div[@id="block-system-main"]//div[@class="view-content"]/div'):
            flat = FlatItem(
                id=result.xpath('.//div[contains(@class, "objektnummer")]/text()').get(),
                agency='stadt-haus',
                link=response.urljoin(result.xpath('.//a/@href').get()),
                title=result.xpath('.//div[contains(@class, "objektnummer")]/text()').get(),
                size=result.xpath('.//div[contains(@class, "woh-wohnflaeche")]/text()').get().split()[0],
                rooms=float(result.xpath('.//div[contains(@class, "woh-zimmer")]/text()').get().split()[0].replace(',','.')),
                address=', '.join(result.xpath('.//div[contains(@id, "woh-adresse")]/div/text()').getall()[:3]),
                district=result.xpath('.//div[contains(@id, "woh-adresse")]/div/text()').getall()[3],
                rent_cold=int(result.xpath('.//div[contains(@class, "nettokaltmiete")]/div[2]/text()').get().split()[0].split(',')[0]),
                rent_total=int(result.xpath('.//div[contains(@class, "gesamtmiete")]/div[2]/text()').get().split()[0].split(',')[0]),
                image_urls=[result.xpath('.//img/@src').get()]
            )
            yield flat
