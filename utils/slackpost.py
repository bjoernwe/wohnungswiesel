import os

from itemadapter import ItemAdapter
from slack import WebClient
from slack.errors import SlackApiError
from typing import Optional, List

from scraper.items import FlatItem


def post_markdown_to_slack(text: str, channel: str):
    block = _generate_markdown_block(text=text)
    _send_blocks_to_slack(blocks=[block], channel=channel)


def post_flat_to_slack(flat_item: FlatItem, channel: str):

    flat = ItemAdapter(flat_item)
    rent = f"{int(flat['rent_total'])} (warm) €" if flat['rent_total'] else f"{int(flat['rent_cold'])} €"
    district_str = f"in {flat['district']}" if flat['district'] else ''

    description = (f"> <{flat['link']}|*{flat['title']}*> *[{flat['agency']}]*\n"
                   f"> {flat['rooms']} Zimmer ({flat['size']} qm) {district_str}\n"
                   f"> <https://maps.google.com/?q={flat['address']}|{flat['address']}>\n"
                   f"> Miete: {rent}"
                   )

    thumbnail_url = flat['image_urls'][0] if flat['image_urls'] else None

    block = _generate_markdown_block(text=description, image_url=thumbnail_url)
    _send_blocks_to_slack(blocks=[block], channel=channel)


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


def _send_blocks_to_slack(blocks: List[dict], channel: str, icon_url: str = 'https://i.imgur.com/OkldsAZ.jpg'):
    slack = WebClient(token=os.environ['SLACK_API_TOKEN'])
    try:
        slack.chat_postMessage(
            channel=channel,
            blocks=blocks,
            icon_url=icon_url
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")
