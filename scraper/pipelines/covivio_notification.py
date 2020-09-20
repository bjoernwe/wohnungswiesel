# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from slackpost import post_flat_to_slack
from scraper.items import CovivioItem


class CovivioNotificationPipeline:

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider) -> CovivioItem:
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
        return item
