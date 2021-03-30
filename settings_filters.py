from scraper.filters import FlatFilter
from scraper.items import RealEstateType
from zip_codes import *


MUNICIPAL_VENDORS = ['degewo', 'gewobag', 'stadt-und-land', 'wbm', 'immo/degewo', 'immo/gewobau-1', 'immo/gewobau-2',
                     'immo/gewobau-3', 'immo/gewobag', 'immo/stadt&land', 'immo/wbm']


SLACK_CHANNELS_FILTERS = {
    '#all_flats': FlatFilter(),
    '#alt-treptow': FlatFilter(zip_whitelist=ZIPS_ALT_TREPTOW),
    '#baumschulenweg': FlatFilter(zip_whitelist=ZIPS_BAUMSCHULENWEG),
    '#big': FlatFilter(
        rooms=(5, None),
        wbs_required=False,
        zip_blacklist=ZIPS_BLACKLIST,
    ),
    '#britz': FlatFilter(zip_whitelist=ZIPS_BRITZ),
    '#charlottenburg': FlatFilter(zip_whitelist=ZIPS_CHARLOTTENBURG),
    '#commercial': FlatFilter(
        types=[RealEstateType.office, RealEstateType.industry, RealEstateType.special_purpose, RealEstateType.store],
    ),
    '#friedenau': FlatFilter(zip_whitelist=ZIPS_FRIEDENAU),
    '#friedrichsfelde': FlatFilter(zip_whitelist=ZIPS_FRIEDRICHSFELDE),
    '#friedrichshain': FlatFilter(zip_whitelist=ZIPS_FRIEDRICHSHAIN),
    '#houses': FlatFilter(types=[RealEstateType.house_rent]),
    '#kreuzberg': FlatFilter(zip_whitelist=ZIPS_KREUZBERG),
    '#lichtenberg': FlatFilter(zip_whitelist=ZIPS_LICHTENBERG),
    '#mariendorf': FlatFilter(zip_whitelist=ZIPS_MARIENDORF),
    '#marzahn': FlatFilter(zip_whitelist=ZIPS_MARZAHN),
    '#medium': FlatFilter(
        rooms=(3, 4),
        wbs_required=False,
        zip_blacklist=ZIPS_BLACKLIST,
        types=[RealEstateType.apartment_rent],
    ),
    '#mitte': FlatFilter(zip_whitelist=ZIPS_MITTE),
    '#municipal': FlatFilter(
        sources=MUNICIPAL_VENDORS,
        rooms=(2, None),
        wbs_required=False,
        zip_blacklist=ZIPS_BLACKLIST,
        types=[RealEstateType.apartment_rent],
    ),
    '#neukölln': FlatFilter(zip_whitelist=ZIPS_NEUKOELLN),
    '#niederschöneweide': FlatFilter(zip_whitelist=ZIPS_NIEDERSCHOENEWEIDE),
    '#nikolasee': FlatFilter(zip_whitelist=ZIPS_NIKOLASEE),
    '#oberschöneweide': FlatFilter(zip_whitelist=ZIPS_OBERSCHOENEWEIDE),
    '#pankow': FlatFilter(zip_whitelist=ZIPS_PANKOW),
    '#plänterwald': FlatFilter(zip_whitelist=ZIPS_PLAENTERWALD),
    '#prenzlauer_berg': FlatFilter(zip_whitelist=ZIPS_PRENZLAUER_BERG),
    '#rummelsburg': FlatFilter(zip_whitelist=ZIPS_RUMMELSBURG),
    '#schöneberg': FlatFilter(zip_whitelist=ZIPS_SCHOENEBERG),
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
    '#spandau': FlatFilter(zip_whitelist=ZIPS_SPANDAU),
    '#steglitz': FlatFilter(zip_whitelist=ZIPS_STEGLITZ),
    '#tempelhof': FlatFilter(zip_whitelist=ZIPS_TEMPELHOF),
    '#tiergarten': FlatFilter(zip_whitelist=ZIPS_TIERGARTEN),
    '#wedding': FlatFilter(zip_whitelist=ZIPS_WEDDING),
    '#weißensee': FlatFilter(zip_whitelist=ZIPS_WEISSENSEE),
    '#wilmersdorf': FlatFilter(zip_whitelist=ZIPS_WILMERSDORF),
    '#zehlendorf': FlatFilter(zip_whitelist=ZIPS_ZEHLENDORF),
}
