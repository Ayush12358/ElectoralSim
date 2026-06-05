"""
Electoral Systems — verify seat allocation and alternative voting imports.

Mirrors README Key Features / Electoral Systems table.
"""
import numpy as np
from electoral_sim import (
    allocate_seats,
    dhondt_allocation,
    sainte_lague_allocation,
    hare_quota_allocation,
    droop_quota_allocation,
    irv_election,
    approval_voting,
    condorcet_winner,
    generate_rankings,
)


def test_seat_allocation():
    """All four PR allocation methods produce non-negative seat counts."""
    votes = np.array([4000, 3000, 2000, 1000], dtype=float)
    n_seats = 10

    for name, func in [
        ("dhondt", dhondt_allocation),
        ("sainte_lague", sainte_lague_allocation),
        ("hare_quota", hare_quota_allocation),
        ("droop_quota", droop_quota_allocation),
    ]:
        seats = func(votes, n_seats)
        assert len(seats) == len(votes), f"{name}: wrong output length"
        assert np.all(seats >= 0), f"{name}: negative seats"
        assert seats.sum() == n_seats, f"{name}: sum={seats.sum()}, expected {n_seats}"

    # Universal allocate_seats
    for method in ["dhondt", "sainte_lague", "hare", "droop"]:
        seats = allocate_seats(votes, n_seats, method=method)
        assert np.all(seats >= 0) and seats.sum() == n_seats


def test_alternative_voting():
    """IRV, Approval, Condorcet return expected result shapes."""
    rng = np.random.default_rng(42)
    utilities = rng.normal(0, 1, (500, 5))
    rankings = generate_rankings(utilities)

    # IRV
    result = irv_election(rankings, n_candidates=5)
    assert "winner" in result
    assert "rounds" in result

    # Approval
    approvals = rng.integers(0, 2, (200, 3))
    result = approval_voting(approvals, n_candidates=3)
    assert "winner" in result
    assert "approval_counts" in result

    # Condorcet
    result = condorcet_winner(rankings, n_candidates=5)
    assert "has_condorcet" in result


if __name__ == "__main__":
    test_seat_allocation()
    test_alternative_voting()
    print("All electoral systems snippets: OK")
