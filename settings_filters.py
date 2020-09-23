from scraper.filters import FlatFilter


MUNICIPAL_VENDORS = ['degewo', 'gewobag', 'stadt-und-land', 'wbm', 'immo/degewo', 'immo/gewobau-1', 'immo/gewobau-2',
                     'immo/gewobau-3', 'immo/gewobag', 'immo/stadt&land', 'immo/wbm']


EXCLUDED_ZIP_CODES = [10409, 12309, 13086, 13405, 13407, 13627]


SLACK_CHANNELS_FILTERS = {
    '#all_flats': FlatFilter(),
    '#big': {
        'rooms': (5, None),
        'wbs_required': False,
    },
    '#municipal': {
        'sources': MUNICIPAL_VENDORS,
        'rooms': (2, None),
        'wbs_required': False,
    },
    '#sharable': {
        'rooms': (4, None),
        'wbs_required': False,
    },
    '#tki': {
        'sources': ['tki', 'immo/tki'],
    },
    #'#test': {
    #    'sources': ['immo'],
    #    'zip_range': (10115, 14199),
    #},
}
