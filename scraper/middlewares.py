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
        error_msg = repr(exception)
        error_mrkdwn = f'```{error_msg}```'
        post_markdown_to_slack(text=error_mrkdwn, channel='#exceptions')
