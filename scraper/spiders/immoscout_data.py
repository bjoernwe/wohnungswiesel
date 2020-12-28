from pydantic import HttpUrl, validator
from pydantic.dataclasses import dataclass
from typing import Optional, Dict

from scraper.items import RealEstateType


@dataclass
class RealEstateAddress:
    city: str
    postalCode: int
    area: Optional[float] = None
    areaLabel: Optional[str] = None
    street: Optional[str] = None
    houseNumber: Optional[str] = None

    def __str__(self):
        parts = []
        if self.street_as_str:
            parts.append(self.street_as_str)
        if self.city_as_str:
            parts.append(self.city_as_str)
        if parts:
            return ', '.join(parts)
        return 'n/a'

    @property
    def street_as_str(self) -> Optional[str]:
        parts = []
        if self.street:
            parts.append(self.street)
            if self.houseNumber:
                parts.append(self.houseNumber)
        if parts:
            return ' '.join(parts)

    @property
    def city_as_str(self) -> Optional[str]:
        parts = []
        if self.postalCode:
            parts.append(str(self.postalCode))
        if self.city:
            parts.append(self.city)
        if parts:
            return ' '.join(parts)


@dataclass
class RealEstateCoordinates:
    lat: float
    lon: float


@dataclass
class ImmoScoutData:
    realEstateId: int
    realEstateType: RealEstateType
    showAddress: bool
    address: RealEstateAddress
    buy: bool
    price: Optional[float] = None
    numberOfRooms: Optional[float] = None
    formattedPrice: Optional[str] = None
    priceDimension: Optional[str] = None
    pictureUrl: Optional[HttpUrl] = None
    coordinates: Optional[RealEstateCoordinates] = None
    lastDeactivationDate: Optional[float] = None
    rentalStartDate: Optional[Dict] = None

    @validator('pictureUrl', pre=True)
    def _picture_url_not_empty(cls, v):
        if v == '':
            return None
        return v
