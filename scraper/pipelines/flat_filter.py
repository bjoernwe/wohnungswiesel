from scraper.filters import FlatFilter
from scraper.items import FlatItem
from utils.slackpost import post_flat_to_slack


class FlatFilterPipeline:

    _filter = {
        '#all_flats': FlatFilter(),
        '#städtische': FlatFilter(
            agencies=['degewo', 'gewobag', 'stadt-und-land', 'wbm'],
            rooms=(2, None),
            wbm_required=False
        ),
        '#wg-geeignet': FlatFilter(
            rooms=(4, None),
            wbm_required=False
        )
    }

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider) -> FlatItem:
        for channel, filter in self._filter.items():
            if filter.is_match(flat=item):
                post_flat_to_slack(flat_item=item, channel=channel)
        return item
