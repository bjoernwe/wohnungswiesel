import re


re_qm = r'(\d+[.,]?\d*)\s*(qm|m2)?'
re_euro = r'(\d+[.,]?\d*)\s*(€|Euro|Eur)?'


def parse_qm(s: str) -> float:
    matches = re.search(re_qm, s, re.IGNORECASE)
    number_str = matches.group(1)
    number = float(number_str.replace(',', '.'))
    return number


def parse_euro(s: str) -> float:
    matches = re.search(re_euro, s, re.IGNORECASE)
    number_str = matches.group(1)
    number = float(number_str.replace(',', '.'))
    return number
