# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import List


@dataclass
class FlatItem:
    id: str
    link: str = field(default=None)
    title: str = field(default=None)
    size: float = field(default=None)
    rooms: float = field(default=None)
    address: str = field(default=None)
    district: str = field(default=None)
    rent_cold: float = field(default=None)
    rent_warm: float = field(default=None)
    features: List[str] = field(default=None)
    image_urls: List[str] = field(default=None)
