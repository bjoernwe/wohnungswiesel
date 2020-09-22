# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wohnungswiesel'

SPIDER_MODULES = ['scraper.spiders']

LOG_LEVEL = 'ERROR'
LOG_FILE = './log/logging.log'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scraper.pipelines.duplicate_filter.DuplicateFilterPipeline': 300,
    'scraper.pipelines.flat_filter.FlatFilterPipeline': 800,
}


SPIDER_MIDDLEWARES = {
    'scraper.middlewares.SlackExceptionNotificationMiddleware': 543,
}



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True


SLACK_CHANNELS_FILTERS = {
        '#all_flats': {},
        '#städtische': {
            'agencies': ['degewo', 'gewobag', 'stadt-und-land', 'wbm'],
            'rooms': (2, None),
            'wbs_required': False
        },
        '#wg-geeignet': {
            'rooms': (4, None),
            'wbs_required': False
        },
        #'#test': {
        #    'agencies': ['degewo', 'gewobag', 'stadt-und-land', 'wbm'],
        #    'wbs_required': None
        #},
    }


FEEDS = {
    './log/all_items.jsonl': {
        'format': 'jsonlines'
    }
}
