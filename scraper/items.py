# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from pydantic import HttpUrl
from pydantic.dataclasses import dataclass
from typing import List, Optional


@dataclass
class FlatItem:
    id: str
    agency: str
    title: str
    link: HttpUrl
    size: float
    rooms: float
    address: str
    district: Optional[str]
    rent_cold: Optional[float] = None
    rent_total: Optional[float] = None
    image_urls: Optional[List[HttpUrl]] = None
