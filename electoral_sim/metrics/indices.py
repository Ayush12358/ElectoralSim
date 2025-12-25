"""
Metrics and Indices for Electoral Analysis
"""

import numpy as np


def gallagher_index(vote_shares: np.ndarray, seat_shares: np.ndarray) -> float:
    """
    Gallagher Least Squares Index of disproportionality.

    LSq = √(½ Σ(v_i - s_i)²)

    Args:
        vote_shares: Vote shares per party (0-1, should sum to 1)
        seat_shares: Seat shares per party (0-1, should sum to 1)

    Returns:
        Gallagher index (0-100 scale, lower = more proportional)
    """
    # Ensure we're working with shares, not percentages
    if vote_shares.sum() > 1.5:
        vote_shares = vote_shares / vote_shares.sum()
    if seat_shares.sum() > 1.5:
        seat_shares = seat_shares / seat_shares.sum()

    squared_diff = (vote_shares - seat_shares) ** 2
    return np.sqrt(0.5 * squared_diff.sum()) * 100


def loosemore_hanby_index(vote_shares: np.ndarray, seat_shares: np.ndarray) -> float:
    """
    Loosemore-Hanby Index of disproportionality.

    D = ½ Σ|v_i - s_i|

    Args:
        vote_shares: Vote shares per party (0-1)
        seat_shares: Seat shares per party (0-1)

    Returns:
        L-H index (0-100 scale)
    """
    if vote_shares.sum() > 1.5:
        vote_shares = vote_shares / vote_shares.sum()
    if seat_shares.sum() > 1.5:
        seat_shares = seat_shares / seat_shares.sum()

    return 0.5 * np.abs(vote_shares - seat_shares).sum() * 100


def effective_number_of_parties(shares: np.ndarray) -> float:
    """
    Effective Number of Parties (Laakso-Taagepera).

    N = 1 / Σ(p_i²)

    Can be applied to votes (ENEP) or seats (ENPP).

    Args:
        shares: Party shares (0-1, should sum to 1)

    Returns:
        ENP value
    """
    if shares.sum() > 1.5:
        shares = shares / shares.sum()

    # Filter out zero shares
    shares = shares[shares > 0]

    return 1.0 / (shares**2).sum()


def herfindahl_hirschman_index(shares: np.ndarray) -> float:
    """
    Herfindahl-Hirschman Index (HHI) of concentration.

    HHI = Σ(p_i²) × 10000

    Args:
        shares: Party shares (0-1)

    Returns:
        HHI (0-10000 scale, higher = more concentrated)
    """
    if shares.sum() > 1.5:
        shares = shares / shares.sum()

    return (shares**2).sum() * 10000


def efficiency_gap(
    party_a_votes: np.ndarray,
    party_b_votes: np.ndarray,
    party_a_seats: np.ndarray,
) -> float:
    """
    Efficiency Gap for gerrymandering detection.

    Wasted votes = losing votes + (winning votes - 50% - 1)
    EG = (Party A wasted - Party B wasted) / total votes

    Note: >7% threshold suggests potential gerrymandering

    Args:
        party_a_votes: Votes for party A in each district
        party_b_votes: Votes for party B in each district
        party_a_seats: Binary array (1 if A won, 0 if B won)

    Returns:
        Efficiency gap (-1 to 1, positive favors A)
    """
    total_votes = party_a_votes.sum() + party_b_votes.sum()

    a_wasted = 0
    b_wasted = 0

    for i in range(len(party_a_seats)):
        votes_a = party_a_votes[i]
        votes_b = party_b_votes[i]
        district_total = votes_a + votes_b
        votes_to_win = district_total // 2 + 1

        if party_a_seats[i] == 1:  # A won
            a_wasted += votes_a - votes_to_win  # Surplus votes
            b_wasted += votes_b  # All losing votes
        else:  # B won
            b_wasted += votes_b - votes_to_win
            a_wasted += votes_a

    return (a_wasted - b_wasted) / total_votes


def turnout_rate(votes_cast: int, eligible_voters: int) -> float:
    """
    Calculate turnout rate.

    Args:
        votes_cast: Total votes cast
        eligible_voters: Total eligible voters

    Returns:
        Turnout rate (0-1)
    """
    return votes_cast / eligible_voters if eligible_voters > 0 else 0.0


def vote_share(party_votes: int, total_votes: int) -> float:
    """
    Calculate vote share for a party.

    Args:
        party_votes: Votes for the party
        total_votes: Total votes cast

    Returns:
        Vote share (0-1)
    """
    return party_votes / total_votes if total_votes > 0 else 0.0


def seat_share(party_seats: int, total_seats: int) -> float:
    """
    Calculate seat share for a party.

    Args:
        party_seats: Seats won by party
        total_seats: Total seats

    Returns:
        Seat share (0-1)
    """
    return party_seats / total_seats if total_seats > 0 else 0.0


def seats_votes_ratio(seat_share: float, vote_share: float) -> float:
    """
    Calculate seats-to-votes ratio (advantage ratio).

    > 1 means overrepresented, < 1 means underrepresented.

    Args:
        seat_share: Party's seat share (0-1)
        vote_share: Party's vote share (0-1)

    Returns:
        Ratio
    """
    return seat_share / vote_share if vote_share > 0 else 0.0
