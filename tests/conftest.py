import pytest

from scraper.items import FlatItem


@pytest.fixture
def flat_item():
    return FlatItem(
        id='42',
        source='Test',
        link='http://google.com',
        title='Title',
        size=100,
        rooms=3,
        address='Hauptstr. 1, Berlin',
        district=None,
        rent_cold=500,
        rent_total=600,
        image_urls=None
    )
