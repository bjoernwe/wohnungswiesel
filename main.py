from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from tutorial.spiders.covivio_spider import CovivioSpider


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(CovivioSpider)
    process.start()


if __name__ == '__main__':
    main()
