import pytest
from scrapy.exceptions import DropItem

from scraper.pipelines.duplicate_filter import DuplicateFilterPipeline


class TestDuplicateFilter:

    def test_duplicate_filter_throws_drop_exception(self, flat_item):

        # GIVEN a DuplicateFilterPipeline and a flat_item
        pipeline = DuplicateFilterPipeline()

        # WHEN the flat has been seen before
        try:
            pipeline.process_item(item=flat_item)
        except DropItem:
            pass

        # THEN it is dropped the second time
        with pytest.raises(DropItem):
            pipeline.process_item(item=flat_item)
