# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os
import pickle
import time

from typing import Optional

from slackpost import post_flat_to_slack
from scraper.items import CovivioItem


class CovivioNotificationPipeline:

    def __init__(self):
        self._filename = 'covivio_known_items.pkl'
        self._known_items = {}

    def open_spider(self, spider):
        self._load_known_items()

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

    def process_item(self, item, spider) -> CovivioItem:
        if self._is_known_item(item):
            return item
        # TODO: Forget old items
        return self._process_new_item(item=item)

    def _remember_item(self, item: CovivioItem):
        item_id = item['id']
        now = time.time()
        self._known_items[item_id] = now

    def _is_known_item(self, item: CovivioItem):
        is_known = item['id'] in self._known_items
        return is_known

    def _process_new_item(self, item: CovivioItem) -> CovivioItem:
        post_flat_to_slack(title=item['title']['rendered'],
                           rooms=item['anzahl_zimmer'],
                           address=item['adresse'],
                           price=item['kaltmiete'],
                           size=item.get('wohnflaeche', '[n/a]'),
                           link_url=item['link'],
                           district=item['regionaler_zusatz'],
                           merkmale=item['merkmale'],
                           image_url=item['bilder'][0]['url']
                           )
        self._remember_item(item)
        return item
