import os
import pytest

from scraper.items import FlatItem
from unittest import mock

from utils.slackpost import post_flat_to_slack


@pytest.fixture
def flat_item():
    return FlatItem(id='42', agency='Test', link=None, title='Title', size=100, rooms=3, address='Hauptstr. 1, Berlin',
                    district=None, rent_cold=500, rent_total=600, image_urls=None)


@pytest.fixture
def slack_offline():
    os.environ['SLACK_API_TOKEN'] = 'SOME_API_TOKEN'
    with mock.patch('slack.WebClient.chat_postMessage'):
        yield


class TestSlackPost:

    @pytest.mark.usefixtures('slack_offline')
    def test_flat_item_is_accepted(self, flat_item):
        # GIVEN a FlatItem object
        # WHEN a flat is posted to Slack
        post_flat_to_slack(flat_item=flat_item)
        # THEN no exception was thrown
