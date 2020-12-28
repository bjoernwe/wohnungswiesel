import scrapy

from scrapy import Request, Selector
from scrapy.http import TextResponse
from typing import Iterable

from scraper.items import FlatItem, FlatSource, RealEstateType
from utils.parsers import parse_qm


class GcpSpider(scrapy.Spider):

    name = FlatSource.gcp

    _request_url = 'https://www.grandcityproperty.de/real-estate-ajax?language=de'

    _form_data = {
        'city': 'Städte|Berlin',
        'type': 'M'
     }

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.FormRequest(url=self._request_url, formdata=self._form_data, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> FlatItem:
        for result in response.xpath('//div[contains(@class, "real-estate-item")]'):
            flat = self._parse_flat_from_selector(result, response=response)
            yield flat

    def _parse_flat_from_selector(self, s: Selector, response: TextResponse) -> FlatItem:
        flat_id = s.xpath('./@data-id').get()
        link = response.urljoin(s.xpath('.//a/@href').get())
        title = s.xpath('.//h2/text()').get().replace('\n', '').strip()
        size = parse_qm(s.xpath('.//div/text()[contains(., "Fläche")]/../text()').getall()[0])
        rooms = float(s.xpath('.//div/text()[contains(., "Zimmer")]/../text()').get().split()[0].replace(',', '.'))
        address = s.xpath('./@data-street').get() + ', ' + s.xpath('./@data-city').get()
        district = None
        rent_cold = float(s.xpath('./@data-price').get())
        image_urls = [response.urljoin(s.xpath('.//picture/@data-default-src').get())]
        flat = FlatItem(id=flat_id, source=self.name, link=link, title=title, size=size, rooms=rooms,
                        address=address, district=district, rent_cold=rent_cold, image_urls=image_urls,
                        wbs_required=False, type=RealEstateType.apartment_rent)
        return flat
