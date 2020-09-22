from pydantic.dataclasses import dataclass
from scrapy.settings import Settings
from typing import Dict

from scraper.filters import FlatFilter
from scraper.items import FlatItem
from utils.slackpost import post_flat_to_slack


@dataclass
class ChannelToFilterMap:
    c2f: Dict[str, FlatFilter]


class FlatFilterPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        settings: Settings = crawler.settings
        c2f_dict = settings.getdict('SLACK_CHANNELS_FILTERS', default={})
        c2f = ChannelToFilterMap(c2f_dict)
        return cls(c2f=c2f)

    def __init__(self, c2f: ChannelToFilterMap):
        self._c2f = c2f

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider) -> FlatItem:
        for channel, flat_filter in self._c2f.items():
            if flat_filter.is_match(flat=item):
                post_flat_to_slack(flat_item=item, channel=channel)
        return item
