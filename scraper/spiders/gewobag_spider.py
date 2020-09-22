import scrapy
import urllib
import urllib.parse

from scrapy import Request, Selector
from scrapy.http import TextResponse
from typing import Iterable

from scraper.items import FlatItem
from utils.parsers import parse_qm, parse_euro


class GewobagSpider(scrapy.Spider):

    name = "gewobag"

    _query_params = {
        'bezirke[]': [
            'friedrichshain-kreuzberg',
            'friedrichshain-kreuzberg-friedrichshain',
            'friedrichshain-kreuzberg-kreuzberg',
            'neukoelln',
            'pankow-prenzlauer-berg',
            'tempelhof-schoeneberg',
            'tempelhof-schoeneberg-schoeneberg'
        ],
        'nutzungsarten[]': ['wohnung'],
        'keinwbs': 1
     }

    def start_requests(self) -> Iterable[Request]:
        api_endpoint = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/'
        query_args = urllib.parse.urlencode(self._query_params, doseq=True)
        url = f'{api_endpoint}?{query_args}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> FlatItem:
        for result in response.xpath('//article[contains(@class, "angebot")]'):
            flat = self._parse_flat_from_selector(result, response=response)
            yield flat

    def _parse_flat_from_selector(self, s: Selector, response: TextResponse) -> FlatItem:
        flat_id = s.xpath('./@id').get()
        link = s.xpath('.//a[contains(@class, "angebot-header")]/@href').get()
        title = s.xpath('.//h3[contains(@class, "angebot-title")]/text()').get()
        size = parse_qm(s.xpath('.//li[contains(@class, "angebot-area")]/strong/text()').get().split(' | ')[1])
        rooms = s.xpath('.//li[contains(@class, "angebot-area")]/strong/text()').get().split(' | ')[0].split()[0]
        address = s.xpath('.//address/text()').get().strip().split('/')[0]
        district = s.xpath('.//address/text()').get().strip().split('/')[1]
        rent_total = parse_euro(s.xpath('.//li[contains(@class, "angebot-kosten")]/strong/text()').get())
        image_urls = s.xpath('.//section[contains(@class, "angebot-slider")]//img/@src').getall()
        flat = FlatItem(id=flat_id, agency=self.name, link=link, title=title, size=size, rooms=rooms,
                        address=address, district=district, rent_total=rent_total, image_urls=image_urls,
                        wbs_required=False)
        return flat
