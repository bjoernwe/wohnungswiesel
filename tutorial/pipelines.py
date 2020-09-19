# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pickle
import time

from slackpost import post_flat_to_slack
from tutorial.items import CovivioItem


class CovivioNotificationPipeline:

    def __init__(self):
        self._filename = 'covivio_known_items.pkl'
        self._known_items = {}

    def open_spider(self, spider):
        with open(self._filename, 'rb+') as f:
            self._known_items = pickle.load(f)

    def close_spider(self, spider):
        with open(self._filename, 'wb+') as f:
            pickle.dump(self._known_items, f)

    def process_item(self, item, spider):
        if self._is_known_item(item):
            return item
        self._remember_item(item)
        # TODO: Forget old items
        return self._process_new_item(item=item)

    def _remember_item(self, item: CovivioItem):
        item_id = item['id']
        now = time.time()
        self._known_items[item_id] = now

    def _is_known_item(self, item: CovivioItem):
        is_known = item['id'] in self._known_items
        return is_known

    def _process_new_item(self, item: CovivioItem):
        post_flat_to_slack(title=item['id'], rooms=0, address='n/a', price=0, size=0)
