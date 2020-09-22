import os
import pytest

from scraper.items import FlatItem
from unittest import mock

from utils.slackpost import post_flat_to_slack


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
        post_flat_to_slack(flat=flat_item, channel='#test')
        # THEN no exception was thrown
