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
    coordinates: RealEstateCoordinates
    numberOfRooms: float
    buy: bool
    pictureUrl: Optional[HttpUrl] = None
    lastDeactivationDate: Optional[float] = None
    rentalStartDate: Optional[float] = None

    @validator('pictureUrl', pre=True)
    def _picture_url_not_empty(cls, v):
        if v == '':
            return None
        return v
