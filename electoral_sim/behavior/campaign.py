"""
Campaign Finance Model for ElectoralSim.

Models spending, fundraising, ad saturation, diminishing returns,
incumbency fundraising advantage, and district targeting effects.
Campaign effects connect to valence/media exposure rather than
direct vote overrides.
"""

import numpy as np


class CampaignFinance:
    """
    Campaign finance model with spending-to-valence conversion.

    Models the effect of campaign spending on party valence with
    diminishing returns. Incumbents have a fundraising advantage.
    """

    def __init__(
        self,
        base_spending: float = 1_000_000.0,
        incumbent_advantage: float = 1.5,
        diminishing_factor: float = 0.5,
    ):
        """
        Args:
            base_spending: Base campaign spending per party (monetary units)
            incumbent_advantage: Multiplier for incumbent fundraising
            diminishing_factor: Diminishing returns exponent (<1 = steeper curve)
        """
        self.base_spending = base_spending
        self.incumbent_advantage = incumbent_advantage
        self.diminishing_factor = diminishing_factor

    def compute_spending(
        self,
        n_parties: int,
        incumbents: np.ndarray | None = None,
        rng: np.random.Generator | None = None,
    ) -> np.ndarray:
        """
        Compute campaign spending per party.

        Args:
            n_parties: Number of parties
            incumbents: Boolean array indicating incumbent parties
            rng: Random generator for spending variation

        Returns:
            Array of spending per party
        """
        if rng is None:
            rng = np.random.default_rng()

        spending = np.full(n_parties, self.base_spending, dtype=float)

        if incumbents is not None:
            spending[incumbents] *= self.incumbent_advantage

        spending *= rng.uniform(0.8, 1.2, n_parties)
        return spending

    def spending_to_valence(
        self,
        spending: np.ndarray,
    ) -> np.ndarray:
        """
        Convert campaign spending to valence boost with diminishing returns.

        Args:
            spending: Per-party campaign spending

        Returns:
            Valence boost per party (additive to base valence)
        """
        return np.log1p(spending) ** self.diminishing_factor * 5.0

    def district_targeting(
        self,
        spending: np.ndarray,
        n_districts: int,
        marginal_seats: np.ndarray | None = None,
    ) -> np.ndarray:
        """
        Allocate campaign spending across districts.

        Parties allocate more resources to marginal (competitive) districts.

        Args:
            spending: Per-party total spending
            n_districts: Number of districts
            marginal_seats: (n_parties, n_districts) marginality scores (0-1)

        Returns:
            (n_parties, n_districts) spending allocation matrix
        """
        n_parties = len(spending)
        if marginal_seats is None:
            allocation = np.ones((n_parties, n_districts)) / n_districts
        else:
            allocation = marginal_seats / (marginal_seats.sum(axis=1, keepdims=True) + 1e-10)

        return spending[:, np.newaxis] * allocation
