import json
import scrapy
import urllib.parse

from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable, Optional

from scraper.items import FlatItem


class ImmoscoutSpider(scrapy.Spider):

    name = "immo"

    _realtors = {
        '4r&s':             'ade62695f24f3dca58b443c',
        'ado':              'a625521eb5a410e8f57cc',
        'carolin_weiss':    'a76ce930e46c42a8975',
        'claudia_koehn':    'ac75d7b78eded13d11d',
        'cramer':           'aa38aca9696dfe2b61a',
        'deutsche_wohnen':  'a8f9031eb35e66b77',
        'eb':               'a4f284f473b53cc1765',
        'gcp':              'a1ff114efd22049c6bd19',
        'gesobau_1':        'a11c223a99f96571de5',
        'gesobau_2':        'a6c23d1c589c4ab50ed85',
        'gesobau_3':        'a13e21300d4dd4ae8fd85ac',
        'gewobag':          'a54af8451045fd1',
        'homes6service':    'afea67b90e71d7562a2aa8a',
        'immo_next':        'ae81f6ec5468cd9',
        'stadt&land':       'a92a678d73456eed04d',
        'stuck&fuetting':   'a5532d12e73740bb09b85',
        'tki':              'a2e90a5aaf2ba013e406d9e',
        'wbm':              'a97efe8583d1da8',
    }

    _request_url = 'https://www.immobilienscout24.de/anbieter/api/branchenbuch/v1.0/realestates'

    _query_params = {
        'pageNumber': 1,
        'pageSize': 100,
        'offerType': 'RENT',
        'i': None,
        'encryptedRealtorId': None,
    }

    def start_requests(self) -> Iterable[Request]:
        for realtor, encrypted_id in self._realtors.items():
            query_params = dict(self._query_params)
            query_params['encryptedRealtorId'] = encrypted_id
            query_args = urllib.parse.urlencode(query_params)
            url = f'{self._request_url}?{query_args}'
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'realtor': realtor})

    def parse(self, response: TextResponse, realtor: Optional[str] = None) -> FlatItem:
        for result in json.loads(response.text)['realEstates']:
            flat = self._parse_flat_from_selector(result, response=response, realtor=realtor)
            yield flat

    def _parse_flat_from_selector(self, d: dict, response: TextResponse, realtor: Optional[str] = None) -> Optional[FlatItem]:
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
        agency_name = f'{self.name}/{realtor}'
        flat = FlatItem(id=flat_id, agency=agency_name, link=link, title=title, size=size, rooms=rooms,
                        address=address, district=district, rent_cold=rent_cold, image_urls=image_urls,
                        wbs_required=False)
        return flat
