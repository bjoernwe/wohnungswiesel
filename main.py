from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.degewo_spider import DegewoSpider
from scraper.spiders.covivio_spider import CovivioSpider
from scraper.spiders.stadt_haus_spider import StadtHausSpider
from scraper.spiders.stadt_und_land_spider import StadtUndLandSpider


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(DegewoSpider)
    process.crawl(CovivioSpider)
    process.crawl(StadtHausSpider)
    process.crawl(StadtUndLandSpider)
    process.start()


if __name__ == '__main__':
    main()
