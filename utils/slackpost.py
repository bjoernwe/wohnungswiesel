import os

from slack import WebClient
from slack.errors import SlackApiError
from typing import Optional, List

from scraper.items import FlatItem, RealEstateType


def post_markdown_to_slack(text: str, channel: str, preview_text: Optional[str] = None):
    block = _generate_markdown_block(text=text)
    _send_blocks_to_slack(blocks=[block], channel=channel, preview_text=preview_text)


def post_flat_to_slack(flat: FlatItem, channel: str):

    # Title
    source_qualifier = f'/{flat.source_qualifier}' if flat.source_qualifier else ''
    description = f"> {flat.type.human_readable()}: <{flat.link}|*{flat.title}*> *[{flat.source}{source_qualifier}]*\n"

    # Add rooms
    if flat.type == RealEstateType.apartment_rent:
        description += f"> {flat.rooms} rooms / ({flat.size} ㎡)\n"

    # Address
    address = _get_address(flat=flat)
    if address:
        description += address + '\n'

    # Rent
    rent = _get_rent(flat)
    description += f"> Rent: {rent}"

    # Add rent per room
    if flat.type == RealEstateType.apartment_rent:
        rent_per_room = flat.get_price_per_room_as_str()
        rent_per_one_room_less = flat.get_price_per_room_as_str(minus_one=True)
        description += f" / {rent_per_room} ({rent_per_one_room_less}) €/room"

    # Generate post
    thumbnail_url = flat.image_urls[0] if flat.image_urls else None
    preview = f"{flat.rooms} rooms / {flat.size} ㎡ / {rent} €"
    block = _generate_markdown_block(text=description, image_url=thumbnail_url)

    # Send to Slack
    _send_blocks_to_slack(blocks=[block], channel=channel, preview_text=preview)


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


def _send_blocks_to_slack(blocks: List[dict], channel: str, icon_url: str = 'https://i.imgur.com/OkldsAZ.jpg',
                          preview_text: Optional[str] = None):
    slack = WebClient(token=os.environ['SLACK_API_TOKEN'])
    try:
        slack.chat_postMessage(
            channel=channel,
            blocks=blocks,
            icon_url=icon_url,
            text=preview_text
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


def _get_address(flat: FlatItem) -> Optional[str]:

    parts = []

    if flat.address:
        parts.append(f'> <https://maps.google.com/?q={flat.address}|{flat.address}>')

    if flat.district:
        parts.append(f' {flat.district}')

    address = ''.join(parts)

    if address:
        return address


def _get_rent(flat: FlatItem) -> str:

    if flat.rent_cold is None and flat.rent_total is None:
        return '[n/a]'

    if flat.rent_total:
        return f'{flat.rent_total}€ (warm)'

    if flat.rent_cold:
        return f'{flat.rent_cold}€ (kalt)'

    return '[n/a]'
