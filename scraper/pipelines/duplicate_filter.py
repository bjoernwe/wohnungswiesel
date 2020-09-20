# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pickle
import time

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from scraper.items import FlatItem


class DuplicateFilterPipeline:

    def __init__(self):
        self._filename = 'covivio_known_items.pkl'
        self._known_items = {}

    def open_spider(self, spider):
        self._load_known_items()
        self._forget_old_items()

    def close_spider(self, spider):
        self._save_known_items()

    def _load_known_items(self) -> None:
        try:
            with open(self._filename, 'rb') as f:
                self._known_items = pickle.load(f)
        except FileNotFoundError:
            pass

    def _save_known_items(self) -> None:
        with open(self._filename, 'wb+') as f:
            pickle.dump(self._known_items, f)

    def process_item(self, item, spider) -> FlatItem:
        item_adapter = ItemAdapter(item=item)
        if self._is_known_item(item=item_adapter):
            raise DropItem('Item has been processed before.')
        else:
            self._remember_item(item=item_adapter)
            return item

    def _remember_item(self, item: ItemAdapter):
        item_id = item['id']
        now = time.time()
        self._known_items[item_id] = now

    def _forget_old_items(self):
        for item_id, timestamp in list(self._known_items.items()):
            timestamp_now = time.time()
            is_older_than_two_weeks = timestamp_now >= timestamp + 60*60*24*7*2
            if is_older_than_two_weeks:
                self._known_items.pop(item_id)

    def _is_known_item(self, item: ItemAdapter):
        is_known = item['id'] in self._known_items
        return is_known
