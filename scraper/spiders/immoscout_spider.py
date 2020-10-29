import json
import random
import scrapy
import urllib.parse

from pydantic import ValidationError
from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable, Optional

from scraper.items import FlatItem, FlatSource
from scraper.spiders.immoscout_data import ImmoScoutData, RealEstateType
from scraper.spiders.immoscout_realtors import realtors


class ImmoscoutSpider(scrapy.Spider):

    name = FlatSource.immo

    _request_url = 'https://www.immobilienscout24.de/anbieter/api/branchenbuch/v1.0/realestates'

    _query_params = {
        'pageNumber': 1,
        'pageSize': 100,
        'offerType': 'RENT',
        'i': None,
        'encryptedRealtorId': None,
    }

    def start_requests(self) -> Iterable[Request]:
        for realtor, encrypted_id in random.sample(realtors.items(), k=len(realtors)):
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
                address=str(data.address),
                district=None,
                rent_cold=data.price,
                image_urls=data.pictureUrl
            )
        except ValidationError as e:
            self.logger.error(msg=f'Error processing {ImmoScoutData.__class__.__name__} into flat: {data}', exc_info=e)
            raise e

        return flat
