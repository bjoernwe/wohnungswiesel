import re

from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from scraper.items import FlatItem, RealEstateType
from zip_codes import BERLIN_ZIP_RANGE


@dataclass
class FlatFilter:

    sources: Optional[List[str]] = None
    source_qualifiers: Optional[List[str]] = None
    types: Optional[List[RealEstateType]] = field(default_factory=lambda: [RealEstateType.apartment_rent,
                                                                           RealEstateType.house_rent])
    rooms: Tuple[Optional[float], Optional[float]] = field(default=(None, None))
    zip_range: Tuple[Optional[int], Optional[int]] = field(default=BERLIN_ZIP_RANGE)
    zip_whitelist: Optional[Set[int]] = None
    zip_blacklist: Optional[Set[int]] = None

    def is_match(self, flat: FlatItem):

        # Sources
        if not self._has_matching_source(flat):
            return False

        # Source qualifiers
        if not self._has_matching_source_qualifier(flat=flat):
            return False

        # Types
        if not self._is_matching_type(flat):
            return False

        # Rooms
        if not self._has_matching_number_of_rooms(flat):
            return False

        # ZIP range
        if not self._has_matching_zip_range(flat):
            return False

        # ZIP whitelist
        if not self._has_matching_zip(flat):
            return False

        # ZIP blacklist
        if self._has_excluded_zip(flat):
            return False

        return True

    def _has_matching_source(self, flat: FlatItem) -> bool:

        if not self.sources or not flat.source:
            return True

        matches = {flat.source.startswith(src) for src in self.sources}
        has_matching_source = True in matches

        return has_matching_source

    def _has_matching_source_qualifier(self, flat: FlatItem) -> bool:

        if not self.source_qualifiers or not flat.source_qualifier:
            return True

        matches = {flat.source_qualifier.startswith(qualifier) for qualifier in self.source_qualifiers}
        has_matching_qualifier = True in matches

        return has_matching_qualifier

    def _is_matching_type(self, flat: FlatItem) -> bool:

        # keep flats without type or when no type is filtered
        if not self.types or not flat.type:
            return True

        return flat.type in self.types

    def _has_matching_number_of_rooms(self, flat: FlatItem) -> bool:

        if not flat.rooms:
            return True

        rooms_min = self.rooms[0]
        rooms_max = self.rooms[1]

        if rooms_min and flat.rooms < rooms_min:
            return False

        if rooms_max and flat.rooms > rooms_max:
            return False

        return True

    def _has_matching_zip_range(self, flat: FlatItem) -> bool:

        if not self.zip_range:
            return True

        zip_min = self.zip_range[0]
        zip_max = self.zip_range[1]

        if not zip_min and not zip_max:
            return True

        zip_code = self._extract_zip(flat.address)

        if not zip_code:
            return True

        if zip_min and zip_code < zip_min:
            return False

        if zip_max and zip_code > zip_max:
            return False

        return True

    def _has_matching_zip(self, flat: FlatItem) -> bool:

        if not self.zip_whitelist:
            return True

        zip_code = self._extract_zip(flat.address)

        if not zip_code:
            return True

        if zip_code not in self.zip_whitelist:
            return False

        return True

    def _has_excluded_zip(self, flat: FlatItem) -> bool:

        if not self.zip_blacklist:
            return False

        zip_code = self._extract_zip(flat.address)

        if not zip_code:
            return False

        if zip_code in self.zip_blacklist:
            return True

        return False

    @staticmethod
    def _extract_zip(address: Optional[str] = None) -> Optional[int]:

        if not address:
            return None

        matches = re.search(r'(\d{4,5})', address)

        if not matches:
            return None

        return int(matches.group(1))
