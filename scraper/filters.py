from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional, Tuple

from scraper.items import FlatItem


@dataclass
class FlatFilter:

    agencies: Optional[List[str]] = None
    rooms: Tuple[Optional[int], Optional[int]] = field(default=(None, None))
    wbm_required: Optional[bool] = None

    def is_match(self, flat: FlatItem):

        if self.agencies and flat.agency not in self.agencies:
            return False

        if self.rooms[0] and flat.rooms < self.rooms[0]:
            return False

        if self.rooms[1] and flat.rooms > self.rooms[1]:
            return False

        if self.wbm_required is not None and flat.wbm_required is not None:
            if self.wbm_required != flat.wbm_required:
                return False

        return True
