import re

from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional, Tuple

from scraper.items import FlatItem


@dataclass
class FlatFilter:

    agencies: Optional[List[str]] = None
    rooms: Tuple[Optional[int], Optional[int]] = field(default=(None, None))
    wbs_required: Optional[bool] = None
    zip_range: Tuple[Optional[int], Optional[int]] = field(default=(None, None))

    def is_match(self, flat: FlatItem):

        # Agency

        if self.agencies and True not in [flat.agency.startswith(agn) for agn in self.agencies]:
            return False

        # Rooms

        rooms_min = self.rooms[0]
        rooms_max = self.rooms[1]

        if rooms_min and flat.rooms < rooms_min:
            return False

        if rooms_max and flat.rooms > rooms_max:
            return False

        # WBS

        if self.wbs_required is not None and flat.wbs_required is not None:
            if self.wbs_required != flat.wbs_required:
                return False

        # ZIP

        zip_min = self.zip_range[0]
        zip_max = self.zip_range[1]

        if zip_min or zip_max:
            zip_code = self._extract_zip(flat.address)
            if zip_min and zip_code < zip_min:
                return False
            if zip_max and zip_code > zip_max:
                return False

        return True

    @staticmethod
    def _extract_zip(address: Optional[str] = None) -> Optional[int]:

        if not address:
            return None

        matches = re.search(r'(\d{5})', address)

        if not matches:
            return None

        return int(matches.group(1))
