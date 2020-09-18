from scrapy.crawler import CrawlerProcess

from tutorial.spiders.covivio_spider import CovivioSpider


def main():
    process = CrawlerProcess()
    process.crawl(CovivioSpider)
    process.start()


if __name__ == '__main__':
    main()
