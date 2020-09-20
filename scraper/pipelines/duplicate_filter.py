# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pathlib
import pickle
import time

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from threading import RLock

from scraper.items import FlatItem


log = logging.getLogger('duplicate_filter_pipeline')


class DuplicateFilterPipeline:

    def __init__(self):
        self._filename = str(pathlib.Path('~/.wohnungswiesel/known_items.pkl').expanduser())
        self._file_lock = RLock()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider) -> FlatItem:
        item_adapter = ItemAdapter(item=item)
        if self._is_known_item(item=item_adapter):
            raise DropItem('Item has been processed before.')
        else:
            self._remember_item(item=item_adapter)
            return item

    def _is_known_item(self, item: ItemAdapter):
        with self._file_lock:
            known_items = self._load_known_items()
        is_known = item['id'] in known_items
        return is_known

    def _remember_item(self, item: ItemAdapter):
        item_id = item['id']
        now = time.time()
        with self._file_lock:
            known_items = self._load_known_items()
            known_items[item_id] = now
            self._save_known_items(known_items)

    def _load_known_items(self) -> dict:
        try:
            with self._file_lock:
                pathlib.Path(self._filename).parent.mkdir(parents=True, exist_ok=True)
                with open(self._filename, 'rb') as f:
                    return pickle.load(f)
        except FileNotFoundError:
            return {}

    def _save_known_items(self, known_items: dict) -> None:
        with self._file_lock:
            with open(self._filename, 'wb+') as f:
                pickle.dump(known_items, f)

    def _forget_old_items(self):
        with self._file_lock:
            known_items = self._load_known_items()
            for item_id, timestamp in list(known_items.items()):
                timestamp_now = time.time()
                is_older_than_two_weeks = timestamp_now >= timestamp + 60*60*24*7*2
                if is_older_than_two_weeks:
                    with self._file_lock:
                        known_items.pop(item_id)
            self._save_known_items(known_items)
