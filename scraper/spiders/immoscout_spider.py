import json
import scrapy
import urllib.parse

from pydantic import ValidationError
from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable, Optional

from scraper.items import FlatItem, FlatSource
from scraper.spiders.immoscout_data import ImmoScoutData, RealEstateType


class ImmoscoutSpider(scrapy.Spider):

    name = FlatSource.immo

    _realtors = {
        '4r&s':             'ade62695f24f3dca58b443c',
        'ado':              'a625521eb5a410e8f57cc',
        'ajs':              'a71914fc943a00e35f3e7f3',
        'berlinhaus':       'a1413c71bfaf8155d53b180',
        'carolin_weiss':    'a76ce930e46c42a8975',
        'claudia_koehn':    'ac75d7b78eded13d11d',
        'cramer':           'aa38aca9696dfe2b61a',
        'deutsche_wohnen':  'a8f9031eb35e66b77',
        'eb':               'a4f284f473b53cc1765',
        'gcp':              'a1ff114efd22049c6bd19',
        'gesobau-1':        'a11c223a99f96571de5',
        'gesobau-2':        'a6c23d1c589c4ab50ed85',
        'gesobau-3':        'a13e21300d4dd4ae8fd85ac',
        'gewobag':          'a54af8451045fd1',
        'homes&service':    'afea67b90e71d7562a2aa8a',
        'immo_next':        'ae81f6ec5468cd9',
        'immohold':         'a9fb2eb8829bc560909',
        'stadt&land':       'a92a678d73456eed04d',
        'stuck&fuetting':   'a5532d12e73740bb09b85',
        'tki':              'a2e90a5aaf2ba013e406d9e',
        'wbm':              'a97efe8583d1da8',
        'zebitz':           'aedf2aff8d2ed18cc303b81',
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
            flat = self._parse_flat_from_selector(result=result, response=response, realtor=realtor)
            yield flat

    def _parse_flat_from_selector(self, result: dict, response: TextResponse, realtor: str) -> Optional[FlatItem]:

        if result.get('realEstateType') != RealEstateType.apartment_rent:
            return

        try:
            data = ImmoScoutData(**result)
        except ValidationError as e:
            self.logger.error(msg=f'Error processing {ImmoScoutData.__class__.__name__}: {result}', exc_info=e)
            raise e

        try:
            flat = FlatItem(
                id=data.realEstateId,
                source=self.name,
                source_qualifier=realtor,
                title=f'ImmoScout {data.realEstateId}',
                link=f'https://www.immobilienscout24.de/expose/{data.realEstateId}/',
                size=data.address.area,
                rooms=data.numberOfRooms,
                address=f'{data.address.street} {data.address.houseNumber}, {data.address.postalCode} {data.address.city}',
                district=None,
                rent_cold=data.price,
                image_urls=data.pictureUrl
            )
        except ValidationError as e:
            self.logger.error(msg=f'Error processing {ImmoScoutData.__class__.__name__} into flat: {data}', exc_info=e)
            raise e

        return flat
