import scrapy
import urllib
import urllib.parse

from scrapy import Request, Selector
from scrapy.http import TextResponse
from typing import Iterable

from scraper.items import FlatItem, FlatSource
from utils.parsers import parse_qm, parse_euro


class StadtHausSpider(scrapy.Spider):

    name = FlatSource.stadt_haus

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
            flat = self._parse_flat_from_selector(result, response=response)
            yield flat

    def _parse_flat_from_selector(self, s: Selector, response: TextResponse) -> FlatItem:
        flat_id = s.xpath('.//div[contains(@class, "objektnummer")]/text()').get()
        link = response.urljoin(s.xpath('.//a/@href').get())
        title = s.xpath('.//div[contains(@class, "objektnummer")]/text()').get()
        size = parse_qm(s.xpath('.//div[contains(@class, "woh-wohnflaeche")]/text()').get())
        rooms = float(s.xpath('.//div[contains(@class, "woh-zimmer")]/text()').get().split()[0].replace(',', '.'))
        address = ', '.join(s.xpath('.//div[contains(@id, "woh-adresse")]/div/text()').getall()[:3])
        district = s.xpath('.//div[contains(@id, "woh-adresse")]/div/text()').getall()[3]
        rent_cold = parse_euro(s.xpath('.//div[contains(@class, "nettokaltmiete")]/div[2]/text()').get().replace(' ', ''))
        rent_total = parse_euro(s.xpath('.//div[contains(@class, "gesamtmiete")]/div[2]/text()').get().replace(' ', ''))
        image_urls = [s.xpath('.//img/@src').get()]
        flat = FlatItem(id=flat_id, source=self.name, link=link, title=title, size=size, rooms=rooms,
                        address=address, district=district, rent_cold=rent_cold, rent_total=rent_total,
                        image_urls=image_urls)
        return flat
