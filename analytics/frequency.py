import json
from collections import defaultdict, OrderedDict

from scraper.items import FlatItem


def main():

    realtor_count = defaultdict(int)

    with open('../log/all_items.jsonl', 'r') as f:
        for line in f.readlines():
            flat = FlatItem(**json.loads(line))
            realtor = flat.source_qualifier
            realtor_count[realtor] = realtor_count[realtor] + 1

    ordered_realtors = OrderedDict(sorted(realtor_count.items(), key=lambda item: item[1], reverse=True))

    for i, (realtor, count) in enumerate(ordered_realtors.items()):
        print(f'{i}. {realtor}: {count}')


if __name__ == '__main__':
    main()
