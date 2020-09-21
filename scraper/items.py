# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import field
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass
from typing import List, Optional


@dataclass
class FlatItem:
    id: str
    agency: str
    link: HttpUrl
    title: str# = field(default=None)
    size: float# = field(default=None)
    rooms: float# = field(default=None)
    address: str# = field(default=None)
    district: Optional[str]
    rent_cold: float# = field(default=None)
    image_urls: List[HttpUrl]
    rent_total: Optional[float]
