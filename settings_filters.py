from scraper.filters import FlatFilter
from scraper.items import RealEstateType
from zip_codes import ZIPS_BLACKLIST, ZIPS_FRIEDRICHSHAIN, ZIPS_KREUZBERG, ZIPS_NEUKOELLN


MUNICIPAL_VENDORS = ['degewo', 'gewobag', 'stadt-und-land', 'wbm', 'immo/degewo', 'immo/gewobau-1', 'immo/gewobau-2',
                     'immo/gewobau-3', 'immo/gewobag', 'immo/stadt&land', 'immo/wbm']


SLACK_CHANNELS_FILTERS = {
    '#all_flats': FlatFilter(),
    '#big': FlatFilter(
        rooms=(5, None),
        wbs_required=False,
        zip_blacklist=ZIPS_BLACKLIST,
        types=[RealEstateType.apartment_rent],
    ),
    '#commercial': FlatFilter(
        types=[RealEstateType.office, RealEstateType.industry, RealEstateType.special_purpose, RealEstateType.store],
    ),
    '#friedrichshain': FlatFilter(
        zip_whitelist=ZIPS_FRIEDRICHSHAIN,
        types=[RealEstateType.apartment_rent],
    ),
    '#kreuzberg': FlatFilter(
        zip_whitelist=ZIPS_KREUZBERG,
        types=[RealEstateType.apartment_rent],
    ),
    '#medium': FlatFilter(
        rooms=(3, 4),
        wbs_required=False,
        zip_blacklist=ZIPS_BLACKLIST,
        types=[RealEstateType.apartment_rent],
    ),
    '#municipal': FlatFilter(
        sources=MUNICIPAL_VENDORS,
        rooms=(2, None),
        wbs_required=False,
        zip_blacklist=ZIPS_BLACKLIST,
        types=[RealEstateType.apartment_rent],
    ),
    '#neukölln': FlatFilter(
        zip_whitelist=ZIPS_NEUKOELLN,
        types=[RealEstateType.apartment_rent],
    ),
    '#single': FlatFilter(
        rooms=(1, 1.9),
        wbs_required=False,
        zip_blacklist=ZIPS_BLACKLIST,
        types=[RealEstateType.apartment_rent],
    ),
    '#small': FlatFilter(
        rooms=(2, 3),
        wbs_required=False,
        zip_blacklist=ZIPS_BLACKLIST,
        types=[RealEstateType.apartment_rent],
    ),
}
