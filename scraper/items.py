import time

from enum import Enum
from pydantic import HttpUrl, validator
from pydantic.dataclasses import dataclass
from typing import List, Optional, Union


class FlatSource(str, Enum):
    test = 'test'
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
    id: Union[int, str]
    source: FlatSource
    title: str
    link: HttpUrl
    size: float
    rooms: float
    timestamp: float = time.time()
    address: Optional[str] = None
    district: Optional[str] = None
    rent_cold: Optional[float] = None
    rent_total: Optional[float] = None
    image_urls: Optional[List[HttpUrl]] = None
    wbs_required: Optional[bool] = None
    source_qualifier: Optional[str] = None

    @validator('image_urls', pre=True)
    def _normalize_image_urls(cls, v):
        if not v:
            return None
        if not isinstance(v, list):
            return [v]
        return v

    def get_rent(self, prefer_total=True) -> Optional[float]:

        if not self.rent_cold and not self.rent_total:
            return False

        if prefer_total:

            if self.rent_total:
                return self.rent_total
            else:
                return self.rent_cold

        else:

            if self.rent_cold:
                return self.rent_cold
            else:
                return self.rent_total

    def get_price_per_room(self, minus_one: bool = False) -> Optional[float]:

        if self.rooms is None:
            return

        rent = self.get_rent()

        if not rent:
            return

        if minus_one and self.rooms >= 2:
            return rent / (self.rooms - 1)

        return rent / self.rooms
