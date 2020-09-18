import json
import scrapy
import urllib
import urllib.parse

from scrapy import Request
from scrapy.http import TextResponse
from typing import Optional, Iterable


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

    def start_requests(self) -> Iterable[Request]:
        api_endpoint = 'https://www.covivio.immo/wp-json/wp/v2/objekt'
        query_args = urllib.parse.urlencode(self._query_params)
        url = f'{api_endpoint}?{query_args}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse):
        objects = json.loads(response.text)
        for obj in objects:
            yield obj
