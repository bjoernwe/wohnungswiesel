from scraper.filters import FlatFilter


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
