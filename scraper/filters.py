import re

from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from scraper.items import FlatItem


BERLIN_ZIP_RANGE = (10115, 14199)


@dataclass
class FlatFilter:

    sources: Optional[List[str]] = None
    rooms: Tuple[Optional[float], Optional[float]] = field(default=(None, None))
    wbs_required: Optional[bool] = None
    zip_range: Tuple[Optional[int], Optional[int]] = field(default=BERLIN_ZIP_RANGE)
    excluded_zips: Optional[List[int]] = None

    def is_match(self, flat: FlatItem):

        # Sources
        if not self._has_matching_source(flat):
            return False

        # Rooms
        if not self._has_matching_number_of_rooms(flat):
            return False

        # WBS
        if not self._has_matching_wbs_requirement(flat):
            return False

        # ZIP range
        if not self._has_matching_zip_range(flat):
            return False

        # ZIP blacklist
        if self._has_excluded_zip(flat):
            return False

        return True

    def _has_matching_source(self, flat: FlatItem) -> bool:

        if not self.sources or not flat.source:
            return True

        matches = [flat.source.startswith(src) for src in self.sources]
        has_matching_source = True in matches

        return has_matching_source

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

    def _has_matching_wbs_requirement(self, flat: FlatItem) -> bool:

        if not self.wbs_required or not flat.wbs_required:
            return True

        if self.wbs_required != flat.wbs_required:
            return False

        return True

    def _has_matching_zip_range(self, flat: FlatItem) -> bool:

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

    def _has_excluded_zip(self, flat: FlatItem) -> bool:

        if not self.excluded_zips:
            return False

        zip_code = self._extract_zip(flat.address)

        if not zip_code:
            return False

        if zip_code in self.excluded_zips:
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
