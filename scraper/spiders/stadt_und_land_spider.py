import scrapy

from scrapy import Selector
from scrapy.http import TextResponse

from scraper.items import FlatItem
from utils.parsers import parse_euro


class StadtUndLandSpider(scrapy.Spider):

    name = "stadt-und-land"

    start_urls = [
        'https://www.stadtundland.de/Mieten/010-Angebote-Bestand.php?form=stadtundland-expose-search-1.form&sp%3AroomsTo%5B%5D=1&action=submit'
    ]

    def parse(self, response: TextResponse, **kwargs) -> FlatItem:
        for result in response.xpath('//li[@class="SP-TeaserList__item"]'):
            flat = self._parse_flat_from_selector(result, response=response)
            yield flat

    def _parse_flat_from_selector(self, s: Selector, response: TextResponse) -> FlatItem:
        flat_id = s.xpath('.//tr//th[contains(., "Objekt-Nr:")]/../td/text()').get()
        link = response.urljoin(s.xpath('.//a[contains(@class, "SP-Link--info")]/@href').get())
        title = s.xpath('.//header[contains(@class, "SP-Teaser__header")]//text()').get()
        size = float(s.xpath('.//tr//th[contains(., "Wohnfläche:")]/../td/text()').get().split()[0])
        rooms = s.xpath('.//tr//th[contains(., "Zimmer:")]/../td/text()').get()
        address = s.xpath('.//tr//th[contains(., "Adresse:")]/../td/text()').get()
        district = None
        rent_cold = parse_euro(s.xpath('.//tr//th[contains(., "Kaltmiete:")]/../td/text()').get())
        rent_total = parse_euro(s.xpath('.//tr//th[contains(., "Warmmiete:")]/../td/text()').get())
        image_urls = [response.urljoin(url) for url in s.xpath('.//ul[contains(@class, "SP-MiniGallery__list")]//a/@href').getall()]
        flat = FlatItem(id=flat_id, agency=self.name, link=link, title=title, size=size, rooms=rooms,
                        address=address, district=district, rent_cold=rent_cold, rent_total=rent_total,
                        image_urls=image_urls)
        return flat
