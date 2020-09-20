# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os

from itemadapter import ItemAdapter
from slack import WebClient
from slack.errors import SlackApiError
from typing import Optional

from scraper.items import FlatItem


class SlackNotificationPipeline:

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider) -> FlatItem:
        self._post_flat_to_slack(item)
        return item

    @classmethod
    def _post_flat_to_slack(cls, flat_item: FlatItem):

        slack = WebClient(token=os.environ['SLACK_API_TOKEN'])

        flat = ItemAdapter(flat_item)
        rent = f"{int(flat['rent_total'])} (warm) €" if flat['rent_total'] else f"{int(flat['rent_cold'])} €"
        district_str = f"in {flat['district']}" if flat['district'] else ''

        description = (f"> <{flat['link']}|*{flat['title']}* *[{flat['agency']}]*>\n"
                       f"> {flat['rooms']} Zimmer ({flat['size']} qm) {district_str}\n"
                       f"> <https://maps.google.com/?q={flat['address']}|{flat['address']}>\n"
                       f"> Miete: {rent}"
                       )

        thumbnail_url = flat['image_urls'][0] if flat['image_urls'] else None

        block = cls._generate_markdown_block(text=description, image_url=thumbnail_url)

        try:
            slack.chat_postMessage(
                channel='#new_flats',
                blocks=[block],
                icon_url='https://i.imgur.com/OkldsAZ.jpg'
            )
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")

    @staticmethod
    def _generate_markdown_block(text: str, image_url: Optional[str] = None) -> dict:
        block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }
        if image_url:
            block['accessory'] = {
                "type": "image",
                "image_url": image_url,
                "alt_text": "Preview"
            }
        return block
