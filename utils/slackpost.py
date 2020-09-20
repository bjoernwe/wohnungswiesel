import os

from itemadapter import ItemAdapter
from slack import WebClient
from slack.errors import SlackApiError

from scraper.items import FlatItem


def post_flat_to_slack(flat_item: FlatItem):

    slack = WebClient(token=os.environ['SLACK_API_TOKEN'])

    flat = ItemAdapter(flat_item)
    rent = f"{int(flat['rent_total'])} (warm) €" if flat['rent_total'] else f"{int(flat['rent_cold'])} €"
    district_str = f"in {flat['district']}" if flat['district'] else ''

    descr_block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
             "text": f"> <{flat['link']}|*{flat['title']}*>\n> {flat['rooms']} Zimmer ({flat['size']} qm) {district_str}\n> <https://maps.google.com/?q={flat['address']}|{flat['address']}>\n> Miete: {rent}"
        },
    }

    if flat['image_urls']:
        descr_block["accessory"] = {
            "type": "image",
            "image_url": flat['image_urls'][0],
            "alt_text": "Wohnung"
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
