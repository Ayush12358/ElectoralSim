"""
Constituency Metadata Management

Provides structures for handling real-world constituency data including
names, states, types (reserved/general), and geographic coordinates.
"""

from dataclasses import dataclass, field
from typing import Any

import polars as pl


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
        res = self.df.filter(pl.col("id") == const_id)
        if len(res) > 0:
            return res["name"][0]
        return f"District {const_id}"

    def get_state(self, const_id: int) -> str:
        res = self.df.filter(pl.col("id") == const_id)
        if len(res) > 0:
            return res["state"][0]
        return "Unknown"

    def to_dict_list(self) -> list[dict]:
        return self.df.to_dicts()
