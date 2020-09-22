import json
import scrapy
import urllib.parse

from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable, Optional

from scraper.items import FlatItem


class ImmoscoutSpider(scrapy.Spider):

    name = "immoscout"

    _realtors = {
        '4_rent_and_sale':      ('1600801303985', 'ade62695f24f3dca58b443c'),
        'ado':                  ('1600797134665', 'a625521eb5a410e8f57cc'),
        'carolin_weiss':        ('1600801203632', 'a76ce930e46c42a8975'),
        'claudia_koehn':        ('1600799502004', 'ac75d7b78eded13d11d'),
        'cramer_immobilien':    ('1600801252615', 'aa38aca9696dfe2b61a'),
        'eb':                   ('1600801368708', 'a4f284f473b53cc1765'),
        'gesobau':              ('1600800319663', 'a11c223a99f96571de5'),
        'homes_and_service':    ('1600799498871', 'afea67b90e71d7562a2aa8a'),
        'immo_next':            ('1600799509269', 'ae81f6ec5468cd9'),
        'stadt_und_land':       ('1600799453223', 'a92a678d73456eed04d'),
        'stuck_und_fuetting':   ('1600799504774', 'a5532d12e73740bb09b85'),
        'wbm':                  ('1600799567329', 'a97efe8583d1da8'),
    }

    _request_url = 'https://www.immobilienscout24.de/anbieter/api/branchenbuch/v1.0/realestates'

    _query_params = {
        'pageNumber': 1,
        'pageSize': 500,
        'offerType': 'RENT',
        'i': None,
        'encryptedRealtorId': None,
    }

    def start_requests(self) -> Iterable[Request]:
        for name, (immo_id, encrypted_id) in self._realtors.items():
            query_params = dict(self._query_params)
            query_params['i'] = immo_id
            query_params['encryptedRealtorId'] = encrypted_id
            query_args = urllib.parse.urlencode(query_params)
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
        title = f'ImmoScout {flat_id}'
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
