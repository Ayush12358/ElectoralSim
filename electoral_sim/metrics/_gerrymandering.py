"""Gerrymandering and compactness metrics.

Extracted from indices.py to keep each file under the 250-LOC ceiling.
"""

import numpy as np


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
    if total_votes == 0:
        return 0.0

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


def partisan_bias(
    party_votes: np.ndarray,
    party_seats: np.ndarray,
) -> float:
    """
    Partisan bias: asymmetry in how a party's votes translate to seats.

    Measures the seat share a party would receive at 50% of the two-party
    vote, minus 50%. Positive = advantage for party A.

    Args:
        party_votes: District-level vote totals for party A (shape: n_districts,)
        party_seats: Binary (1=won, 0=lost) per district

    Returns:
        Bias value (-0.5 to 0.5, 0 = symmetric)
    """
    total_votes = party_votes.sum() + party_votes.sum()  # assumes 2-party
    if total_votes == 0:
        return 0.0
    seat_share = party_seats.sum() / len(party_seats) if len(party_seats) > 0 else 0.0
    # At 50% vote, predicted seat share via uniform swing
    vote_share = party_votes.sum() / total_votes if total_votes > 0 else 0.5
    # Linear interpolation: seat_share at vote_share=0.5
    return seat_share - vote_share


def mean_median_gap(
    district_vote_shares: np.ndarray,
) -> float:
    """
    Mean-Median Gap: difference between mean and median district vote share.

    Positive value = party's voters are "cracked" across districts
    (mean > median), suggesting gerrymandering against the party.

    Args:
        district_vote_shares: Party's vote share in each district (0-1)

    Returns:
        Mean - median gap (positive = disadvantage for the party)
    """
    if len(district_vote_shares) == 0:
        return 0.0
    mean_share = np.mean(district_vote_shares)
    median_share = np.median(district_vote_shares)
    return float(mean_share - median_share)


def partisan_gini(
    district_vote_shares: np.ndarray,
) -> float:
    """
    Partisan Gini: inequality in district-level vote shares.

    Uses the standard Gini coefficient formula applied to sorted
    district vote shares. Higher values = more concentrated voters.

    Args:
        district_vote_shares: Party's vote share in each district (0-1)

    Returns:
        Gini coefficient (0 = equal, 1 = maximum inequality)
    """
    n = len(district_vote_shares)
    if n <= 1:
        return 0.0
    sorted_shares = np.sort(district_vote_shares)
    index = np.arange(1, n + 1)
    return float((2 * index - n - 1).dot(sorted_shares) / (n * sorted_shares.sum()))


def polsby_popper(area: float, perimeter: float) -> float:
    """
    Polsby-Popper compactness: measures how close a district shape is to a circle.

    Values range from 0 to 1, where 1 is a perfect circle. Low values indicate
    irregular (potentially gerrymandered) districts.

    Args:
        area: District area
        perimeter: District perimeter length

    Returns:
        Polsby-Popper score (0-1)
    """
    if perimeter <= 0:
        return 0.0
    return float(4 * np.pi * area / (perimeter**2))


def convex_hull_compactness(area: float, convex_hull_area: float) -> float:
    """
    Convex hull compactness: ratio of district area to its convex hull area.

    Values range from 0 to 1, where 1 means the district is convex.
    Low values indicate indented shapes.

    Args:
        area: District area
        convex_hull_area: Area of the district's convex hull

    Returns:
        Compactness score (0-1)
    """
    if convex_hull_area <= 0:
        return 0.0
    return float(area / convex_hull_area) if area <= convex_hull_area else 0.0
