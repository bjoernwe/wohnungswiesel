import json
import logging
import scrapy
import urllib
import urllib.parse

from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable

from scraper.items import FlatItem


log = logging.getLogger('covivio_spider')


class CovivioSpider(scrapy.Spider):

    name = "covivio"

    _query_params = {
        'address': 'Berlin',
        'anzahl_zimmer_min': 1,
        'anzahl_zimmer_max': 6,
        'distance': 10,
        'googlemapsEnabled': 'true',
        'kaltmiete_min': 15,
        'kaltmiete_max': 48876,
        'lat': '52.491059199999995',
        'lng': '13.405388799999999',
        'objektart': 'wohnung',
        'order': 'asc',
        'orderby': 'distance',
        'page': 1,
        'per_page': 100,
        'wohnflaeche_min': 0,
        'wohnflaeche_max': 250
    }

    _map_to_flat = {
        'id': 'id',
        'link': 'link',
        #'title': 'title',
        #'bilder': 'pictures',
        'adresse': 'address',
        'regionaler_zusatz': 'district',
        'wohnflaeche': 'size',
        'anzahl_zimmer': 'rooms',
        'kaltmiete': 'rent_cold'
        #'merkmale': 'features'
    }

    def start_requests(self) -> Iterable[Request]:
        api_endpoint = 'https://www.covivio.immo/wp-json/wp/v2/objekt'
        query_args = urllib.parse.urlencode(self._query_params)
        url = f'{api_endpoint}?{query_args}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse):
        objects = json.loads(response.text)
        for obj in objects:
            log.debug(f'found raw item: {obj}')
            flat_args = {k_out: obj[k_in] for k_in, k_out in self._map_to_flat.items()}
            flat_args['title'] = obj['title']['rendered']
            flat_args['image_urls'] = [img['url'] for img in obj['bilder']]
            flat_item = FlatItem(**flat_args)
            yield flat_item
