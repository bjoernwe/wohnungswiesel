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
    '#all_flats': {
        'zip_range': (10115, 14199),
    },
    '#big': {
        'rooms': (5, None),
        'wbs_required': False,
        'zip_range': (10115, 14199),
    },
    '#städtische': {
        'sources': [
            'degewo', 'gewobag', 'stadt-und-land', 'wbm',
            'immo/degewo', 'immo/gewobau-1', 'immo/gewobau-2', 'immo/gewobau-3', 'immo/gewobag', 'immo/stadt&land', 'immo/wbm'
        ],
        'rooms': (2, None),
        'wbs_required': False,
        'zip_range': (10115, 14199),
    },
    '#tki': {
        'sources': ['tki', 'immo/tki'],
    },
    '#wg-geeignet': {
        'rooms': (4, None),
        'wbs_required': False,
        'zip_range': (10115, 14199),
    },
    #'#test': {
    #    'sources': ['immo'],
    #    'zip_range': (10115, 14199),
    #},
}


FEEDS = {
    './log/all_items.jsonl': {
        'format': 'jsonlines'
    }
}
