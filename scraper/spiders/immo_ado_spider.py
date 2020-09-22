import json
import scrapy
import urllib.parse

from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable, Optional

from scraper.items import FlatItem
from utils.parsers import parse_euro


class ImmoAdoSpider(scrapy.Spider):

    name = "ado"

    _request_url = 'https://www.immobilienscout24.de/anbieter/api/branchenbuch/v1.0/realestates'

    _query_params = {
        'pageNumber': 1,
        'pageSize': 500,
        'offerType': 'RENT',
        'encryptedRealtorId': 'a625521eb5a410e8f57cc',
        'i': '1600797134665'
    }

    def start_requests(self) -> Iterable[Request]:
        query_args = urllib.parse.urlencode(self._query_params, doseq=True)
        url = f'{self._request_url}?{query_args}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> FlatItem:
        for result in json.loads(response.text)['realEstates']:
            flat = self._parse_flat_from_selector(result, response=response)
            yield flat

    def _parse_flat_from_selector(self, d: dict, response: TextResponse) -> Optional[FlatItem]:
        if d.get('realEstateType') != 'APARTMENT_RENT':
            return
        flat_id = d['realEstateId']
        link = f'https://www.immobilienscout24.de/expose/{flat_id}/'
        title = f'Immo ADO Wohnung {flat_id}'
        size = d['address']['area']
        rooms = d['numberOfRooms']
        address = f'{d["address"]["street"]} {d["address"]["houseNumber"]}, {d["address"]["postalCode"]} {d["address"]["city"]}'
        district = None
        rent_cold = d['price']
        image_url = d['pictureUrl']
        image_urls = [image_url] if image_url else None
        flat = FlatItem(id=flat_id, agency=self.name, link=link, title=title, size=size, rooms=rooms,
                        address=address, district=district, rent_cold=rent_cold, image_urls=image_urls,
                        wbs_required=False)
        return flat
