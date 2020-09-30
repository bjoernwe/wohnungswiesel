from scraper.filters import FlatFilter


MUNICIPAL_VENDORS = ['degewo', 'gewobag', 'stadt-und-land', 'wbm', 'immo/degewo', 'immo/gewobau-1', 'immo/gewobau-2',
                     'immo/gewobau-3', 'immo/gewobag', 'immo/stadt&land', 'immo/wbm']


EXCLUDED_ZIP_CODES = [10409, 12107, 12279, 12309, 12349, 12627, 12685, 13053, 13086, 13127, 13405, 13407, 13587, 13627]


SLACK_CHANNELS_FILTERS = {
    '#all_flats': FlatFilter(),
    '#big': {
        'rooms': (5, None),
        'wbs_required': False,
    },
    '#municipal': FlatFilter(
        sources=MUNICIPAL_VENDORS,
        rooms=(2, None),
        wbs_required=False,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    '#sharable': FlatFilter(
        rooms=(4, None),
        wbs_required=False,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    '#small': FlatFilter(
        rooms=(2, 3),
        wbs_required=False,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    '#tki': FlatFilter(
        sources=['tki', 'immo/tki'],
    ),
    #'#test': {
    #    'sources': ['immo'],
    #    'zip_range': (10115, 14199),
    #},
}
