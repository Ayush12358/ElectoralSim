"""
Voter Agent for Electoral Simulation
Uses Polars DataFrame for high-performance vectorized operations
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import polars as pl

if TYPE_CHECKING:
    from electoral_sim.core.model import ElectionModel


class VoterAgents:
    """
    Voter agents stored as Polars DataFrame for vectorized operations.

    This class wraps a Polars DataFrame to provide high-performance
    agent data storage with high performance.

    Attributes (DataFrame columns):
        - unique_id: Agent identifier (auto-generated)
        - constituency: Constituency index (0 to n_constituencies-1)
        - ideology_x: Economic left-right (-1 to 1)
        - ideology_y: Social liberal-conservative (-1 to 1)
        - party_id: Current party identification
        - knowledge: Political knowledge (0-100)
        - turnout_prob: Base probability of voting (0-1)
        - media_susceptibility: Susceptibility to media influence (0-1)
        - is_zealot: Whether agent is a zealot (fixed opinion)
    """

    def __init__(
        self,
        model: ElectionModel,
        df: pl.DataFrame,
    ):
        self.model = model
        self.df = df
        self._cache: dict = {}

    def __len__(self) -> int:
        return len(self.df)

    def invalidate_cache(self):
        """Invalidate the cached arrays."""
        self._cache = {}

    @property
    def n_voters(self) -> int:
        """Total number of voters."""
        return len(self.df)

    def get_positions(self) -> np.ndarray:
        """Return ideology positions as (n_voters, 2) array (cached)."""
        if "positions" not in self._cache:
            self._cache["positions"] = np.column_stack(
                [self.df["ideology_x"].to_numpy(), self.df["ideology_y"].to_numpy()]
            )
        return self._cache["positions"]

    def get_ideology_x(self) -> np.ndarray:
        if "ideology_x" not in self._cache:
            self._cache["ideology_x"] = self.df["ideology_x"].to_numpy()
        return self._cache["ideology_x"]

    def get_ideology_y(self) -> np.ndarray:
        if "ideology_y" not in self._cache:
            self._cache["ideology_y"] = self.df["ideology_y"].to_numpy()
        return self._cache["ideology_y"]

    def get_constituencies(self) -> np.ndarray:
        """Return constituency indices (cached)."""
        if "constituency" not in self._cache:
            self._cache["constituency"] = self.df["constituency"].to_numpy()
        return self._cache["constituency"]

    def get_turnout_prob(self) -> np.ndarray:
        """Return turnout probabilities (cached)."""
        if "turnout_prob" not in self._cache:
            self._cache["turnout_prob"] = self.df["turnout_prob"].to_numpy()
        return self._cache["turnout_prob"]

    def step(self):
        """Called each simulation step."""
        pass
