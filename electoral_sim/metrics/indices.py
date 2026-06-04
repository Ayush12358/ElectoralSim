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

    shares = shares[shares > 0]
    if len(shares) == 0:
        return 1.0

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


def responsiveness(
    party_vote_shares: np.ndarray,
    party_seat_shares: np.ndarray,
) -> float:
    """
    Responsiveness: how much seat share changes for a 1% vote share change.

    Measures the slope of the seats-votes curve. Values > 1 mean the
    electoral system amplifies vote swings into larger seat swings.

    Args:
        party_vote_shares: Party vote shares across districts
        party_seat_shares: Party seat shares across districts

    Returns:
        Responsiveness (seats-votes slope)
    """
    if len(party_vote_shares) == 0:
        return 0.0
    votes = np.array(party_vote_shares)
    seats = np.array(party_seat_shares)
    # Standardize to z-scores and compute slope
    v_std = votes.std()
    if v_std == 0:
        return 0.0
    return float(np.corrcoef(votes, seats)[0, 1] * seats.std() / v_std)


def swing_ratio(
    party_votes_a: np.ndarray,
    party_votes_b: np.ndarray,
    party_seats_a: np.ndarray,
) -> float:
    """
    Swing ratio: seat swing per unit vote swing between two parties.

    A swing ratio of 3 means a 1% vote swing produces a 3% seat swing.
    Typical range: 1.5 (highly proportional) to 5+ (highly majoritarian).

    Args:
        party_votes_a: Party A district vote totals
        party_votes_b: Party B district vote totals
        party_seats_a: Binary (1=A won, 0=B won)

    Returns:
        Swing ratio
    """
    n = len(party_votes_a)
    if n == 0:
        return 0.0
    vote_margin = party_votes_a - party_votes_b
    total = party_votes_a + party_votes_b
    vote_share = np.sum(party_votes_a) / np.sum(total) if np.sum(total) > 0 else 0.5
    seat_share = np.mean(party_seats_a)
    # Swing ratio = responsiveness at the observed vote share
    return float(seat_share / vote_share) if vote_share > 0 else 0.0


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
    return float(4 * np.pi * area / (perimeter ** 2))


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
