import scrapy
import urllib.parse

from scrapy import Request, Selector
from scrapy.http import TextResponse
from typing import Iterable, Optional

from scraper.items import FlatItem, FlatSource, RealEstateType
from utils.parsers import parse_euro


class TkiSpider(scrapy.Spider):

    name = FlatSource.tki

    _request_url = 'https://tki.berlin/immobilien/'

    _query_params = {
        'post_type': 'immomakler_object',
        'vermarktungsart': 'miete',
        'nutzungsart': 'wohnen',
        'typ': 'wohnung',
        'ort': 'berlin',
        'im_order': 'datedesc'
    }

    def start_requests(self) -> Iterable[Request]:
        query_args = urllib.parse.urlencode(self._query_params, doseq=True)
        url = f'{self._request_url}?{query_args}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> FlatItem:
        for result in response.xpath('//div[@class="property"]'):
            flat = self._parse_flat_from_selector(result, response=response)
            yield flat

    def _parse_flat_from_selector(self, s: Selector, response: TextResponse) -> Optional[FlatItem]:
        is_rented = s.xpath('.//div[contains(@class, "property-status-vermietet")]').get() is not None
        if is_rented:
            return
        link = s.xpath('.//a/@href').get()
        flat_id = link
        title = s.xpath('.//a/text()').get()
        size = float(s.xpath('.//ul[@class="sizes"]/li[1]/text()').get().split()[1])
        rooms = float(s.xpath('.//ul[@class="sizes"]/li[2]/text()').get().split()[0])
        address = None
        district = ''.join(s.xpath('.//div[contains(@class, "dataort")]/text()').getall()).replace('\n', '').strip()
        rent_cold = parse_euro(s.xpath('.//ul[contains(@class, "prices")]/li/span/text()').get())
        image_urls = [s.xpath('.//img/@src').get()]
        flat = FlatItem(id=flat_id, source=self.name, link=link, title=title, size=size, rooms=rooms,
                        address=address, district=district, rent_cold=rent_cold, image_urls=image_urls,
                        wbs_required=False, type=RealEstateType.apartment_rent)
        return flat
