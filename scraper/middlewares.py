# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from utils.slackpost import post_markdown_to_slack


class SlackExceptionNotificationMiddleware:

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        exc_str = repr(exception)
        spider_class = spider.__class__.__name__
        error_mrkdwn = f'```{exc_str}```from `{spider_class}`:  ```{response}```'
        error_summary = f'{spider_class}: {exc_str}'
        post_markdown_to_slack(text=error_mrkdwn, channel='#exceptions', preview_text=error_summary)
