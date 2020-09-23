import json
import scrapy
import urllib
import urllib.parse

from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable

from scraper.items import FlatItem, FlatSource


class CovivioSpider(scrapy.Spider):

    name = FlatSource.covivio

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

    def parse(self, response: TextResponse, **kwargs):
        objects = json.loads(response.text)
        for obj in objects:
            image_urls = [img['url'] for img in obj['bilder']]
            flat_item = FlatItem(id=obj['id'], source=self.name, title=obj['title']['rendered'], link=obj['link'],
                                 size=obj['wohnflaeche'], rooms=obj['anzahl_zimmer'], address=obj['adresse'],
                                 district=obj['regionaler_zusatz'], rent_cold=obj['kaltmiete'], image_urls=image_urls,
                                 wbs_required=False)
            yield flat_item
