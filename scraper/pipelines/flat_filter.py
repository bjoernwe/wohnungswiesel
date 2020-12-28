import logging

from pydantic.dataclasses import dataclass
from scrapy.settings import Settings
from typing import Dict

from scraper.filters import FlatFilter
from scraper.items import FlatItem
from utils.slackpost import post_flat_to_slack


log = logging.getLogger('flat_filter_pipeline')


@dataclass
class ChannelToFilterMap:
    c2f: Dict[str, FlatFilter]


class FlatFilterPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        settings: Settings = crawler.settings
        c2f_dict = settings.getdict('SLACK_CHANNELS_FILTERS', default=None)
        if not c2f_dict:
            log.warning(f'No SLACK_CHANNELS_FILTERS found. Nothing will be posted to Slack.')
        c2f = ChannelToFilterMap(c2f_dict)
        return cls(c2f=c2f)

    def __init__(self, c2f: ChannelToFilterMap):
        self._c2f = c2f

    def process_item(self, item, spider) -> FlatItem:
        for channel, flat_filter in self._c2f.c2f.items():
            is_match = flat_filter.is_match(flat=item)
            log.debug(f'Matching filter {flat_filter} to flat {item}: {is_match}')
            if is_match:
                post_flat_to_slack(flat=item, channel=channel)
        return item
