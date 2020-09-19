# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
import time

from json import JSONDecodeError

from tutorial.items import CovivioItem


class CovivioNotificationPipeline:

    def __init__(self):
        self._filename = 'covivio_known_items.json'
        self._known_items = {}

    def open_spider(self, spider):
        with open(self._filename, 'w+') as f:
            try:
                self._known_items = json.load(f)
            except JSONDecodeError:
                pass

    def close_spider(self, spider):
        with open(self._filename, 'w') as f:
            json.dump(self._known_items, f)

    def process_item(self, item, spider):
        if self._is_known_item(item):
            return item
        self._remember_item(item)
        return item

    def _remember_item(self, item: CovivioItem):
        key = item['id']
        value = time.time()
        self._known_items[key] = value

    def _is_known_item(self, item: CovivioItem):
        is_known = item['id'] in self._known_items
        return is_known
