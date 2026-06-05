"""
Metrics — verify electoral indices return expected types and ranges.

Mirrors README Metrics section.
"""

import numpy as np
from electoral_sim import (
    gallagher_index,
    effective_number_of_parties,
    efficiency_gap,
)


def test_gallagher_index():
    """Gallagher index returns float between 0 and 100."""
    vote_shares = np.array([0.40, 0.35, 0.25])
    seat_shares = np.array([0.50, 0.30, 0.20])
    gi = gallagher_index(vote_shares, seat_shares)
    assert isinstance(gi, float)
    assert 0 <= gi <= 100


def test_effective_number_of_parties():
    """ENP returns float >= 1.0."""
    shares = np.array([0.50, 0.30, 0.20])
    enp = effective_number_of_parties(shares)
    assert enp >= 1.0
    assert enp <= len(shares)


def test_efficiency_gap():
    """Efficiency gap returns float."""
    party_a_votes = np.array([60, 55, 40, 45, 50])
    party_b_votes = np.array([40, 45, 60, 55, 50])
    party_a_seats = np.array([1, 1, 0, 0, 1])
    gap = efficiency_gap(party_a_votes, party_b_votes, party_a_seats)
    assert isinstance(gap, float)


if __name__ == "__main__":
    test_gallagher_index()
    test_effective_number_of_parties()
    test_efficiency_gap()
    print("All metrics snippets: OK")
