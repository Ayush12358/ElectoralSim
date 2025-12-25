"""
Electoral Systems: Seat allocation methods and electoral rules
"""

import numpy as np
import polars as pl


def dhondt_allocation(votes: np.ndarray, n_seats: int, threshold: float = 0.0) -> np.ndarray:
    """
    D'Hondt (Jefferson) method for proportional seat allocation.
    Favors larger parties slightly.

    Args:
        votes: Array of vote counts per party
        n_seats: Total seats to allocate
        threshold: Minimum vote share to qualify (0-1)

    Returns:
        Array of seats per party
    """
    votes = votes.astype(float)
    total_votes = votes.sum()

    # Apply threshold
    if threshold > 0:
        vote_shares = votes / total_votes
        votes = np.where(vote_shares >= threshold, votes, 0)

    n_parties = len(votes)
    seats = np.zeros(n_parties, dtype=int)

    for _ in range(n_seats):
        quotients = votes / (seats + 1)
        winner = np.argmax(quotients)
        seats[winner] += 1

    return seats


def sainte_lague_allocation(votes: np.ndarray, n_seats: int, threshold: float = 0.0) -> np.ndarray:
    """
    Sainte-Laguë (Webster) method for proportional seat allocation.
    More proportional than D'Hondt.

    Divisors: 1, 3, 5, 7, ...

    Args:
        votes: Array of vote counts per party
        n_seats: Total seats to allocate
        threshold: Minimum vote share to qualify (0-1)

    Returns:
        Array of seats per party
    """
    votes = votes.astype(float)
    total_votes = votes.sum()

    if threshold > 0:
        vote_shares = votes / total_votes
        votes = np.where(vote_shares >= threshold, votes, 0)

    n_parties = len(votes)
    seats = np.zeros(n_parties, dtype=int)

    for _ in range(n_seats):
        # Divisor: 2*seats + 1 = 1, 3, 5, 7, ...
        quotients = votes / (2 * seats + 1)
        winner = np.argmax(quotients)
        seats[winner] += 1

    return seats


def hare_quota_allocation(votes: np.ndarray, n_seats: int, threshold: float = 0.0) -> np.ndarray:
    """
    Hare quota with largest remainder method.

    Quota = total_votes / n_seats

    Args:
        votes: Array of vote counts per party
        n_seats: Total seats to allocate
        threshold: Minimum vote share to qualify (0-1)

    Returns:
        Array of seats per party
    """
    votes = votes.astype(float)
    total_votes = votes.sum()

    if threshold > 0:
        vote_shares = votes / total_votes
        votes = np.where(vote_shares >= threshold, votes, 0)

    quota = total_votes / n_seats

    # Initial allocation: floor(votes / quota)
    seats = np.floor(votes / quota).astype(int)

    # Distribute remaining seats by largest remainder
    remainders = votes - (seats * quota)
    remaining_seats = n_seats - seats.sum()

    if remaining_seats > 0:
        # Get indices of parties sorted by remainder (descending)
        remainder_order = np.argsort(-remainders)
        for i in range(remaining_seats):
            seats[remainder_order[i]] += 1

    return seats


def droop_quota_allocation(votes: np.ndarray, n_seats: int, threshold: float = 0.0) -> np.ndarray:
    """
    Droop quota with largest remainder method.

    Quota = floor(total_votes / (n_seats + 1)) + 1

    Args:
        votes: Array of vote counts per party
        n_seats: Total seats to allocate
        threshold: Minimum vote share to qualify (0-1)

    Returns:
        Array of seats per party
    """
    votes = votes.astype(float)
    total_votes = votes.sum()

    if threshold > 0:
        vote_shares = votes / total_votes
        votes = np.where(vote_shares >= threshold, votes, 0)

    quota = np.floor(total_votes / (n_seats + 1)) + 1

    seats = np.floor(votes / quota).astype(int)
    remainders = votes - (seats * quota)
    remaining_seats = n_seats - seats.sum()

    if remaining_seats > 0:
        remainder_order = np.argsort(-remainders)
        for i in range(remaining_seats):
            seats[remainder_order[i]] += 1

    return seats


def fptp_allocation(
    votes_by_constituency: pl.DataFrame,
    n_constituencies: int,
) -> np.ndarray:
    """
    First Past The Post: winner takes all in each constituency.

    Args:
        votes_by_constituency: DataFrame with columns [constituency, party, votes]
        n_constituencies: Total number of constituencies

    Returns:
        Array of total seats per party
    """
    # Find winner in each constituency
    winners = votes_by_constituency.sort("votes", descending=True).group_by("constituency").first()

    # Count seats per party
    seat_counts = winners.group_by("party").len()

    # Convert to array (assuming party indices 0, 1, 2, ...)
    n_parties = votes_by_constituency["party"].max() + 1
    seats = np.zeros(n_parties, dtype=int)

    for row in seat_counts.iter_rows():
        party, count = row
        seats[party] = count

    return seats


# Allocation method registry
ALLOCATION_METHODS = {
    "dhondt": dhondt_allocation,
    "sainte_lague": sainte_lague_allocation,
    "hare": hare_quota_allocation,
    "droop": droop_quota_allocation,
}


def allocate_seats(
    votes: np.ndarray, n_seats: int, method: str = "dhondt", threshold: float = 0.0
) -> np.ndarray:
    """
    Allocate seats using specified method.

    Uses Numba acceleration when available for dhondt/sainte_lague.

    Args:
        votes: Vote counts per party
        n_seats: Total seats
        method: 'dhondt', 'sainte_lague', 'hare', or 'droop'
        threshold: Minimum vote share (0-1)

    Returns:
        Seats per party
    """
    # Try Numba-accelerated versions for dhondt/sainte_lague
    try:
        from electoral_sim.engine.numba_accel import NUMBA_AVAILABLE, dhondt_fast, sainte_lague_fast

        if NUMBA_AVAILABLE and method in ("dhondt", "sainte_lague"):
            if method == "dhondt":
                return dhondt_fast(votes, n_seats, threshold)
            else:
                return sainte_lague_fast(votes, n_seats, threshold)
    except ImportError:
        pass

    # Fallback to Python implementations
    if method not in ALLOCATION_METHODS:
        raise ValueError(f"Unknown method: {method}. Use one of {list(ALLOCATION_METHODS.keys())}")

    return ALLOCATION_METHODS[method](votes, n_seats, threshold)
