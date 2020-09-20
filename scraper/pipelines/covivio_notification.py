# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from utils.slackpost import post_flat_to_slack
from scraper.items import FlatItem


class CovivioNotificationPipeline:

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider) -> FlatItem:
        post_flat_to_slack(item)
        return item
