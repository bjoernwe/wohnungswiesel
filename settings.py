BOT_NAME = 'wohnungswiesel'
SPIDER_MODULES = ['scraper.spiders']


LOG_LEVEL = 'ERROR'
LOG_FILE = './log/logging.log'


ROBOTSTXT_OBEY = True
AUTOTHROTTLE_ENABLED = True


ITEM_PIPELINES = {
    'scraper.pipelines.duplicate_filter.DuplicateFilterPipeline': 300,
    'scraper.pipelines.flat_filter.FlatFilterPipeline': 800,
}


SPIDER_MIDDLEWARES = {
    'scraper.middlewares.SlackExceptionNotificationMiddleware': 543,
}


FEEDS = {
    './log/all_items.jsonl': {
        'format': 'jsonlines'
    }
}
