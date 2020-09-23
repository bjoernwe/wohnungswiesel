import pytest

from scraper.items import FlatItem, FlatSource


@pytest.fixture
def flat_item():
    return FlatItem(
        id='42',
        source=FlatSource.test,
        link='http://google.com',
        title='Title',
        size=100,
        rooms=3,
        address='Hauptstr. 1, 12345 Berlin',
        district=None,
        rent_cold=500,
        rent_total=600,
        image_urls=None
    )
