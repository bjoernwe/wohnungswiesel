import json

from scraper.filters import FlatFilter
from scraper.items import FlatItem


class TestFlatFilter:

    def test_zip_range(self, flat_item):

        flat_item.address = 'Street 42, 12345 City'

        flat_filter = FlatFilter(zip_range=(None, None))
        assert flat_filter.is_match(flat_item)

        flat_filter = FlatFilter(zip_range=(10000, None))
        assert flat_filter.is_match(flat_item)

        flat_filter = FlatFilter(zip_range=(20000, None))
        assert not flat_filter.is_match(flat_item)

        flat_filter = FlatFilter(zip_range=(None, 20000))
        assert flat_filter.is_match(flat_item)

        flat_filter = FlatFilter(zip_range=(None, 10000))
        assert not flat_filter.is_match(flat_item)

    def test_flat_zip_is_filtered(self):

        flat_dict = json.loads('{"id": 82408145, "source": "immo", "title": "ImmoScout 82408145", "link": "https://www.immobilienscout24.de/expose/82408145/", "size": 114.88, "rooms": 5.0, "address": "Zschochernstr. 32, 7545 Gera", "district": null, "rent_cold": 632.0, "rent_total": null, "image_urls": ["https://pictures.immobilienscout24.de/listings/f42818c4-e05b-44cd-8c65-bfdb121568ff-1351768035.jpg"], "wbs_required": null, "source_qualifier": "berlinhaus"}')
        flat = FlatItem(**flat_dict)

        flat_filter = FlatFilter()
        assert not flat_filter.is_match(flat=flat)
