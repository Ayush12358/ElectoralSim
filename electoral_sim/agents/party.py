"""
Party/Candidate Agents for Electoral Simulation
Uses Polars DataFrame for high-performance vectorized operations
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import polars as pl

if TYPE_CHECKING:
    from electoral_sim.core.model import ElectionModel


class PartyAgents:
    """
    Party agents stored as Polars DataFrame.

    This class wraps a Polars DataFrame to provide high-performance
    party data storage with high performance.

    Attributes (DataFrame columns):
        - unique_id: Party identifier
        - name: Party name
        - position_x: Economic left-right (-1 to 1)
        - position_y: Social liberal-conservative (-1 to 1)
        - valence: Non-policy appeal (0-100)
        - incumbent: Whether currently in government
        - seats: Current seat count
        - vote_share: Last election vote share
    """

    def __init__(self, model: ElectionModel, df: pl.DataFrame):
        self.model = model
        self.df = df
        self._cache: dict = {}

    def __len__(self) -> int:
        return len(self.df)

    def invalidate_cache(self):
        self._cache = {}

    @property
    def n_parties(self) -> int:
        """Number of parties."""
        return len(self.df)

    def get_positions(self) -> np.ndarray:
        """Return party positions as (n_parties, 2) array (cached)."""
        if "positions" not in self._cache:
            self._cache["positions"] = np.column_stack(
                [self.df["position_x"].to_numpy(), self.df["position_y"].to_numpy()]
            )
        return self._cache["positions"]

    def get_valence(self) -> np.ndarray:
        """Return party valence scores (cached)."""
        if "valence" not in self._cache:
            self._cache["valence"] = self.df["valence"].to_numpy()
        return self._cache["valence"]

    def get_names(self) -> list[str]:
        """Return party names."""
        return self.df["name"].to_list()

    def update_results(self, seats: np.ndarray, vote_shares: np.ndarray):
        """Update party results after election."""
        self.df = self.df.with_columns(
            [
                pl.Series("seats", seats),
                pl.Series("vote_share", vote_shares),
            ]
        )

    def step(self):
        """Called each simulation step for party adaptation."""
        pass  # Placeholder for adaptive behavior


# Default party configurations
INDIA_PARTIES = [
    {"name": "BJP", "position_x": 0.4, "position_y": 0.5, "valence": 70},
    {"name": "INC", "position_x": -0.2, "position_y": -0.1, "valence": 55},
    {"name": "AAP", "position_x": -0.3, "position_y": -0.3, "valence": 50},
    {"name": "TMC", "position_x": -0.1, "position_y": 0.1, "valence": 45},
    {"name": "DMK", "position_x": -0.4, "position_y": -0.4, "valence": 45},
    {"name": "SP", "position_x": -0.2, "position_y": 0.2, "valence": 40},
    {"name": "Others", "position_x": 0.0, "position_y": 0.0, "valence": 30},
]

US_PARTIES = [
    {"name": "Democratic", "position_x": -0.4, "position_y": -0.2, "valence": 50},
    {"name": "Republican", "position_x": 0.4, "position_y": 0.3, "valence": 50},
]

UK_PARTIES = [
    {"name": "Conservative", "position_x": 0.3, "position_y": 0.2, "valence": 45},
    {"name": "Labour", "position_x": -0.3, "position_y": -0.1, "valence": 50},
    {"name": "LibDem", "position_x": 0.0, "position_y": -0.2, "valence": 40},
    {"name": "SNP", "position_x": -0.2, "position_y": -0.3, "valence": 45},
]
