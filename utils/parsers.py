# -*- coding: utf-8 -*-

import re


re_qm = r'(\d+[.,]?\d*)\s*(qm|m2|m²|m)'
re_euro = r'([\d.]+[,]?\d*)\s*(€|Euro|Eur)'


def parse_qm(s: str) -> float:
    matches = re.search(re_qm, s, re.IGNORECASE)
    if not matches:
        raise ValueError(f'Could not parse qm: {s}')
    number_str = matches.group(1)
    number = float(number_str.replace(',', '.'))
    return number


def parse_euro(s: str) -> float:
    if s is None:
        return None
    matches = re.search(re_euro, s, re.IGNORECASE)
    if not matches:
        raise ValueError(f'Could not parse Euro: {s}')
    number_str = matches.group(1)
    number_str = number_str.replace('.', '')
    number = float(number_str.replace(',', '.'))
    return number
