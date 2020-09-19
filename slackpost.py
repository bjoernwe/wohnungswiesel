import os

from slack import WebClient
from slack.errors import SlackApiError
from typing import List, Optional, Union


def post_flat_to_slack(title: str, rooms: Union[int, float], address: str, price: int, size: int, link_url: str,
                       image_url: Optional[str] = None, district: Optional[str] = None,
                       merkmale: Optional[List[str]] = None):

    slack = WebClient(token=os.environ['SLACK_API_TOKEN'])

    district_str = f'in {district}' if district else ''

    descr_block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
             "text": f"> <{link_url}|*{title}*>\n> {rooms} Zimmer ({size} qm) {district_str}\n> <https://maps.google.com/?q={address}|{address}>\n> {price}€"
        },
        "accessory": {
            "type": "image",
            "image_url": image_url,
            "alt_text": "Wohnung"
        }
    }

    blocks = [descr_block]

    try:
        slack.chat_postMessage(
            channel='#flat-hunt-berlin',
            blocks=blocks,
            icon_url='https://www.covivio.immo/wp-content/uploads/LOGO_PROFILE-FAVICOM_400x400.jpg'
        )

    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")
