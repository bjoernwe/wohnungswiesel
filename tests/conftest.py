import pytest

from scraper.items import FlatItem, FlatSource, RealEstateType


@pytest.fixture
def flat_item() -> FlatItem:
    return FlatItem(
        id='42',
        source=FlatSource.test,
        link='http://google.com',
        title='Title',
        size=100,
        rooms=3,
        type=RealEstateType.apartment_rent,
        address='Hauptstr. 1, 12345 Berlin',
        district=None,
        rent_cold=500,
        rent_total=600,
        image_urls=None,
        source_qualifier='QUALIFIER',
    )
