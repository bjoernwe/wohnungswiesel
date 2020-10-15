from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.covivio_spider import CovivioSpider
from scraper.spiders.degewo_spider import DegewoSpider
from scraper.spiders.gcp_spider import GcpSpider
from scraper.spiders.gewobag_spider import GewobagSpider
from scraper.spiders.immoscout_spider import ImmoscoutSpider
from scraper.spiders.stadt_haus_spider import StadtHausSpider
from scraper.spiders.stadt_und_land_spider import StadtUndLandSpider
from scraper.spiders.tki_spider import TkiSpider


def main():
    process = CrawlerProcess(get_project_settings())
    #process.crawl(CovivioSpider)
    process.crawl(DegewoSpider)
    process.crawl(GcpSpider)
    process.crawl(GewobagSpider)
    process.crawl(ImmoscoutSpider)
    process.crawl(StadtHausSpider)
    #process.crawl(StadtUndLandSpider)
    process.crawl(TkiSpider)
    process.start()


if __name__ == '__main__':
    main()
