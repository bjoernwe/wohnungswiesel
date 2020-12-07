from scraper.filters import FlatFilter


MUNICIPAL_VENDORS = ['degewo', 'gewobag', 'stadt-und-land', 'wbm', 'immo/degewo', 'immo/gewobau-1', 'immo/gewobau-2',
                     'immo/gewobau-3', 'immo/gewobag', 'immo/stadt&land', 'immo/wbm']


EXCLUDED_ZIP_CODES = [
    10315, 10318, 10319, 10365, 10367, 10409,
    12105, 12107, 12157, 12163, 12167, 12207, 12247, 12249, 12277, 12279, 12309, 12349, 12459, 12487, 12489,
    12529, 12555, 12557, 12559, 12587, 12589, 12619, 12627, 12685, 12687, 12689,
    13051, 13053, 13086, 13088, 13125, 13127, 13156, 13187, 13189, 13359, 13405, 13407, 13409,
    13507, 13509, 13581, 13583, 13585, 13587, 13589, 13591, 13593, 13597, 13599, 13627, 13629,
    14059, 14089, 14109, 14129, 14163, 14169, 14195
]


SLACK_CHANNELS_FILTERS = {
    '#all_flats': FlatFilter(),
    '#big': FlatFilter(
        rooms=(5, None),
        wbs_required=False,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    '#municipal': FlatFilter(
        sources=MUNICIPAL_VENDORS,
        rooms=(2, None),
        wbs_required=False,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    '#medium': FlatFilter(
        rooms=(3, 4),
        wbs_required=False,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    '#single': FlatFilter(
        rooms=(1, 1.9),
        wbs_required=False,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    '#small': FlatFilter(
        rooms=(2, 3),
        wbs_required=False,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    '#wbs': FlatFilter(
        rooms=(2, None),
        wbs_required=True,
        excluded_zips=EXCLUDED_ZIP_CODES,
    ),
    #'#test': {
    #    'sources': ['immo'],
    #    'zip_range': (10115, 14199),
    #},
}
