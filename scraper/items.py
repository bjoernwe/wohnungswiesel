from enum import Enum
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass
from typing import List, Optional


class FlatSource(str, Enum):
    covivio = 'covivio'
    degewo = 'degewo'
    gcp = 'gcp'
    gewobag = 'gewobag'
    immo = 'immo'
    stadt_haus = 'stadt_haus'
    stadt_und_land = 'stadt_und_land'
    tki = 'tki'


@dataclass
class FlatItem:
    id: str
    source: FlatSource
    title: str
    link: HttpUrl
    size: float
    rooms: float
    address: Optional[str]
    district: Optional[str]
    rent_cold: Optional[float] = None
    rent_total: Optional[float] = None
    image_urls: Optional[List[HttpUrl]] = None
    wbs_required: Optional[bool] = None
    source_qualifier: Optional[str] = None
