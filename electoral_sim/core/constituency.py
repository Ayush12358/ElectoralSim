# Copyright 2025-2026 Ayush Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Constituency Metadata Management

Provides structures for handling real-world constituency data including
names, states, types (reserved/general), reserved seat constraints,
candidate eligibility, and voter demographics.
"""

from dataclasses import dataclass, field
from typing import Any

import polars as pl

# Reserved constituency types (India-style)
RESERVED_TYPES = frozenset({"General", "SC", "ST"})


@dataclass
class ConstituencyMetadata:
    """Metadata for a single electoral district."""

    id: int
    name: str
    state: str
    seats: int = 1
    type: str = "General"  # e.g., SC, ST, General
    metadata: dict[str, Any] = field(default_factory=dict)
    lat: float | None = None
    lon: float | None = None


def is_candidate_eligible(
    constituency_type: str,
    candidate_category: str,
    reserved_map: dict[str, str] | None = None,
) -> bool:
    """
    Check if a candidate is eligible to contest in a constituency.

    In General constituencies, all candidates are eligible. In reserved
    constituencies (SC/ST), only candidates of the matching category
    can contest. A reserved_map can override the default mapping.

    Args:
        constituency_type: 'General', 'SC', or 'ST'
        candidate_category: Candidate's demographic category
        reserved_map: Optional override mapping category→allowed_types

    Returns:
        True if candidate is eligible
    """
    if reserved_map is not None:
        return constituency_type in reserved_map.get(candidate_category, ["General"])

    if constituency_type == "General":
        return True  # All candidates eligible
    return candidate_category == constituency_type


class ConstituencyManager:
    """Manages a collection of constituencies for a simulation."""

    def __init__(self, constituencies: list[ConstituencyMetadata] | pl.DataFrame):
        if isinstance(constituencies, pl.DataFrame):
            self.df = constituencies
        else:
            data = [
                {
                    "id": c.id,
                    "name": c.name,
                    "state": c.state,
                    "seats": c.seats,
                    "type": c.type,
                    "lat": c.lat,
                    "lon": c.lon,
                    **c.metadata,
                }
                for c in constituencies
            ]
            self.df = pl.DataFrame(data)

    def get_name(self, const_id: int) -> str:
        """Return constituency name for a given ID.

        Args:
            const_id: Constituency identifier

        Returns:
            Name string, or 'District {id}' if not found
        """
        res = self.df.filter(pl.col("id") == const_id)
        if len(res) > 0:
            return res["name"][0]
        return f"District {const_id}"

    def get_state(self, const_id: int) -> str:
        """Return state/province for a given constituency ID.

        Args:
            const_id: Constituency identifier

        Returns:
            State name string, or 'Unknown' if not found
        """
        res = self.df.filter(pl.col("id") == const_id)
        if len(res) > 0:
            return res["state"][0]
        return "Unknown"

    def get_type(self, const_id: int) -> str:
        """Return constituency type (General, SC, ST).

        Args:
            const_id: Constituency identifier

        Returns:
            Constituency type string, or 'General' if not found
        """
        res = self.df.filter(pl.col("id") == const_id)
        if len(res) > 0 and "type" in res.columns:
            return res["type"][0]
        return "General"

    def to_dict_list(self) -> list[dict]:
        return self.df.to_dicts()
