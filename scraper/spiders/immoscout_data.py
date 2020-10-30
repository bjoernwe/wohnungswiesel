from enum import Enum

from pydantic import HttpUrl, validator
from pydantic.dataclasses import dataclass
from typing import Optional


class RealEstateType(str, Enum):
    apartment_rent = 'APARTMENT_RENT'


@dataclass
class RealEstateAddress:
    city: str
    postalCode: int
    area: float
    areaLabel: str
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
    price: float
    formattedPrice: str
    priceDimension: str
    showAddress: bool
    address: RealEstateAddress
    numberOfRooms: float
    buy: bool
    pictureUrl: Optional[HttpUrl] = None
    coordinates: Optional[RealEstateCoordinates] = None
    lastDeactivationDate: Optional[float] = None
    rentalStartDate: Optional[float] = None

    @validator('pictureUrl', pre=True)
    def _picture_url_not_empty(cls, v):
        if v == '':
            return None
        return v
