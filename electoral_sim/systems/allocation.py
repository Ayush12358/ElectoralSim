"""
Electoral Systems: Seat allocation methods and electoral rules.

Tie-breaking policy: All allocation methods use ``prefer_lower_index`` —
when two or more parties have equal quotients/votes/remainders, the party
with the lowest array index wins. This is the default behavior of
``np.argmax``, loop order, and ``np.argsort`` (which preserves input order
for ties). For tests asserting deterministic tie outcomes, see
``TestFptpTieBreaking`` in tests/test_engine.py.
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

    if n_seats <= 0 or total_votes <= 0:
        return np.zeros(len(votes), dtype=int)

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

    if n_seats <= 0 or total_votes <= 0:
        return np.zeros(len(votes), dtype=int)

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

    if n_seats <= 0 or total_votes <= 0:
        return np.zeros(len(votes), dtype=int)

    if threshold > 0:
        vote_shares = votes / total_votes
        votes = np.where(vote_shares >= threshold, votes, 0)
        total_votes = votes.sum()
        if total_votes <= 0:
            return np.zeros(len(votes), dtype=int)

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

    if n_seats <= 0 or total_votes <= 0:
        return np.zeros(len(votes), dtype=int)

    if threshold > 0:
        vote_shares = votes / total_votes
        votes = np.where(vote_shares >= threshold, votes, 0)
        total_votes = votes.sum()
        if total_votes <= 0:
            return np.zeros(len(votes), dtype=int)

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
        pass  # Intentional: Numba not installed → use Python fallback below

    # Fallback to Python implementations
    if method not in ALLOCATION_METHODS:
        raise ValueError(f"Unknown method: {method}. Use one of {list(ALLOCATION_METHODS.keys())}")

    return ALLOCATION_METHODS[method](votes, n_seats, threshold)


def closed_list_allocation(
    votes: np.ndarray, n_seats: int, candidate_list: list[list[str]], threshold: float = 0.0
) -> dict[str, np.ndarray]:
    """
    Closed-list PR: parties receive seats proportional to votes, candidates
    are elected in party-defined list order.

    Args:
        votes: Vote counts per party
        n_seats: Total seats
        candidate_list: Per-party ordered list of candidate names
        threshold: Minimum vote share

    Returns:
        Dict with 'seats' (per-party), 'elected' (candidate names)
    """
    party_seats = allocate_seats(votes, n_seats, method="dhondt", threshold=threshold)
    elected = []
    for p in range(len(votes)):
        for i in range(int(party_seats[p])):
            if i < len(candidate_list[p]):
                elected.append(candidate_list[p][i])
    return {"seats": party_seats, "elected": elected}


def open_list_allocation(
    votes: np.ndarray,
    n_seats: int,
    candidate_list: list[list[str]],
    preference_votes: list[np.ndarray],
    threshold: float = 0.0,
) -> dict[str, np.ndarray]:
    """
    Open-list PR: parties receive seats proportional to votes, candidates
    are elected by preference vote order within their party.

    Args:
        votes: Vote counts per party
        n_seats: Total seats
        candidate_list: Per-party ordered list of candidate names
        preference_votes: Per-party array of preference votes per candidate
        threshold: Minimum vote share

    Returns:
        Dict with 'seats' (per-party), 'elected' (candidate names)
    """
    party_seats = allocate_seats(votes, n_seats, method="dhondt", threshold=threshold)
    elected = []
    for p in range(len(votes)):
        prefs = preference_votes[p] if p < len(preference_votes) else None
        n = int(party_seats[p])
        if prefs is not None and len(prefs) > 0:
            order = np.argsort(-prefs)
            for i in range(n):
                if order[i] < len(candidate_list[p]):
                    elected.append(candidate_list[p][order[i]])
        else:
            for i in range(n):
                if i < len(candidate_list[p]):
                    elected.append(candidate_list[p][i])
    return {"seats": party_seats, "elected": elected}


def parallel_mixed_allocation(
    district_votes: np.ndarray,
    pr_votes: np.ndarray,
    n_district_seats: int,
    n_pr_seats: int,
    threshold: float = 0.0,
) -> dict[str, np.ndarray]:
    """
    Parallel mixed system (Japan-style): FPTP district seats + PR list seats
    allocated independently, without compensatory leveling.

    Args:
        district_votes: Per-party vote totals for FPTP tier
        pr_votes: Per-party vote totals for PR list tier
        n_district_seats: Total FPTP district seats
        n_pr_seats: Total PR list seats
        threshold: Minimum vote share for PR tier

    Returns:
        Dict with 'district_seats', 'pr_seats', and 'total_seats' arrays
    """
    n_parties = max(len(district_votes), len(pr_votes))
    district_seats = np.zeros(n_parties, dtype=int)
    pr_seats = np.zeros(n_parties, dtype=int)

    if district_votes.sum() > 0 and n_district_seats > 0:
        padded = np.zeros(n_parties, dtype=float)
        padded[:len(district_votes)] = district_votes
        district_seats = dhondt_allocation(padded, n_district_seats)

    if pr_votes.sum() > 0 and n_pr_seats > 0:
        padded = np.zeros(n_parties, dtype=float)
        padded[:len(pr_votes)] = pr_votes
        pr_seats = dhondt_allocation(padded, n_pr_seats, threshold)

    return {
        "district_seats": district_seats,
        "pr_seats": pr_seats,
        "total_seats": district_seats + pr_seats,
    }


def mmp_allocation(
    district_votes: np.ndarray,
    list_votes: np.ndarray,
    n_district_seats: int,
    n_total_seats: int,
    threshold: float = 0.0,
) -> dict[str, np.ndarray]:
    """
    Mixed-Member Proportional (MMP, Germany-style) with overhang and leveling seats.

    District seats are allocated first. List seats are then allocated to make
    the overall seat distribution proportional to list votes. Overhang seats
    are kept (no negative adjustment). Leveling seats are NOT explicitly
    modeled here (they require an iterative process that expands total seats).

    Args:
        district_votes: Per-party vote totals for FPTP district tier
        list_votes: Per-party vote totals for PR list tier
        n_district_seats: Number of FPTP district seats
        n_total_seats: Target total seats in parliament
        threshold: Minimum vote share for list seat qualification (e.g., 0.05)

    Returns:
        Dict with 'district_seats', 'list_seats', 'overhang', 'total_seats'
    """
    n_parties = max(len(district_votes), len(list_votes))

    # Pad arrays to same length
    d_votes = np.zeros(n_parties, dtype=float)
    d_votes[:len(district_votes)] = district_votes
    l_votes = np.zeros(n_parties, dtype=float)
    l_votes[:len(list_votes)] = list_votes

    # Step 1: Allocate district seats (FPTP)
    district_seats = np.zeros(n_parties, dtype=int)
    if d_votes.sum() > 0 and n_district_seats > 0:
        district_seats = dhondt_allocation(d_votes, n_district_seats)

    # Step 2: Apply threshold to list votes
    qualified = np.ones(n_parties, dtype=bool)
    if threshold > 0 and l_votes.sum() > 0:
        vote_shares = l_votes / l_votes.sum()
        qualified = vote_shares >= threshold

    # Step 3: Proportional allocation based on list votes
    list_seats = np.zeros(n_parties, dtype=int)
    list_allocation = np.zeros(n_parties, dtype=int)
    if l_votes.sum() > 0:
        list_allocation = dhondt_allocation(l_votes, n_total_seats)

    # Step 4: Determine target list seats (proportional share minus district seats)
    for p in range(n_parties):
        target = max(0, list_allocation[p] - district_seats[p])
        list_seats[p] = target

    # Step 5: Detect overhang (district seats exceed proportional share)
    overhang = np.maximum(0, district_seats - list_allocation)

    # Step 6: Only qualified parties get list seats
    list_seats[~qualified] = 0

    return {
        "district_seats": district_seats,
        "list_seats": list_seats,
        "overhang": overhang,
        "total_seats": district_seats + list_seats,
    }
