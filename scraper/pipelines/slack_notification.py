from scraper.items import FlatItem
from utils.slackpost import post_flat_to_slack


class SlackNotificationPipeline:

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider) -> FlatItem:
        post_flat_to_slack(item)
        return item
