# Copyright 2025-2026 Ayush Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


from electoral_sim.metrics._gerrymandering import (  # noqa: E402, F401
    convex_hull_compactness,
    efficiency_gap,
    mean_median_gap,
    partisan_bias,
    partisan_gini,
    polsby_popper,
)
