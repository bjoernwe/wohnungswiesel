import json
import logging
import re
import scrapy
import urllib
import urllib.parse

from scrapy import Request
from scrapy.http import TextResponse
from typing import Iterable

from scraper.items import FlatItem


log = logging.getLogger('degewo_spider')


class DegewoSpider(scrapy.Spider):

    name = "degewo"

    _re_euro = re.compile(r'(\d+)[.,]*\d*\s*[€]?')

    _query_params = {
        'property_type_id': 1,
        'categories[]': 1,
        #'address[raw]': None,
        #'address[street]':  None,
        #'address[city]': None,
        #'address[zipcode]': None,
        #'address[district]': '33, 46, 3, 2, 28, 29, 71, 64, 4-8, 58, 60, 7',
        'district': '46, 28, 29, 60',
        #'price_switch': 'false',
        'price_switch': 'on',
        #'price_from': None,
        #'price_to': None,
        'price_radio': 'null',
        #'qm_radio': 'null',
        #'qm_from': None,
        #'qm_to': None,
        'rooms_radio': 'custom',
        'rooms_from': 1,
        'rooms_to': 6,
        #'features[]': '1, 13',
        'wbs_required': 0,
        #'order': 'rent_total_without_vat_asc'
    }

    _map_to_flat = {
        'id': 'id',
        #'link': 'link',
        'headline': 'title',
        #'bilder': 'pictures',
        #'full_address': 'address',
        #'regionaler_zusatz': 'district',
        'living_space': 'size',
        'number_of_rooms': 'rooms',
        #'rent_cold': 'rent_cold',
        #'rent_total_with_vat': 'rent_total',
        #'merkmale': 'features'
    }

    def start_requests(self) -> Iterable[Request]:
        api_endpoint = 'https://immosuche.degewo.de/de/search.json'
        query_args = urllib.parse.urlencode(self._query_params)
        url = f'{api_endpoint}?{query_args}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs):
        response_json = json.loads(response.text)
        for flat_dict in response_json['immos']:
            log.debug(f'found raw item: {flat_dict}')
            flat_args = {k_out: flat_dict[k_in] for k_in, k_out in self._map_to_flat.items()}
            flat_args['link'] = response.urljoin(flat_dict['property_path'])
            flat_args['image_urls'] = [flat_dict['thumb_url']]
            flat_args['address'] = ', '.join([s.strip() for s in flat_dict['full_address'].split('|')])
            flat_args['district'] = flat_dict['neighborhood']['district']
            flat_args['rent_cold'] = self._currency_to_int(flat_dict['rent_cold'])
            flat_args['rent_total'] = self._currency_to_int(flat_dict['rent_total_with_vat'])
            flat_item = FlatItem(**flat_args)
            yield flat_item

        # pagination
        next_page = response_json['pagination'].get('next_page')
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def _currency_to_int(self, currency: str) -> int:
        return int(self._re_euro.match(currency).groups()[0])
