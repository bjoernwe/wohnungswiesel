MUNICIPAL_VENDORS = ['degewo', 'gewobag', 'stadt-und-land', 'wbm', 'immo/degewo', 'immo/gewobau-1', 'immo/gewobau-2',
                     'immo/gewobau-3', 'immo/gewobag', 'immo/stadt&land', 'immo/wbm']


SLACK_CHANNELS_FILTERS = {
    '#all_flats': {},
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
