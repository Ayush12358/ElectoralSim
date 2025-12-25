"""
Voting System Efficiency (VSE) Analysis Module

Calculates VSE, a metric for how well an electoral outcome maximizes social welfare.
VSE = (W_actual - W_random) / (W_optimal - W_random)

Where:
- W_actual: Social welfare of the election winner(s).
- W_optimal: Social welfare of the best possible winner(s).
- W_random: Average social welfare of a random winner.

Ref: Jameson Quinn, "Voting System Efficiency"
"""

import numpy as np


def calculate_welfare(utilities: np.ndarray, weights: np.ndarray | None = None) -> float:
    """
    Calculate Social Welfare (Sum of Utilities).

    Args:
        utilities: (n_voters,) array of utilities for the chosen outcome
        weights: (n_voters,) array of voter weights (optional)

    Returns:
        Total Welfare
    """
    if weights is not None:
        return float(np.sum(utilities * weights))
    return float(np.sum(utilities))


def calculate_vse(
    utilities: np.ndarray, seat_shares: np.ndarray, random_iterations: int = 0
) -> float:
    """
    Calculate Voting System Efficiency.

    Args:
        utilities: (n_voters, n_parties) matrix of utilities
        seat_shares: (n_parties,) array of seat shares (0-1) for the actual outcome.
                     For single-winner: one 1.0, rest 0.0.
        random_iterations: unused in this analytical version (w_random = mean of all options)

    Returns:
        VSE Score (typically 0.0 to 1.0)
    """
    # 1. W_optimal
    # The "Optimal" outcome depends on the goal.
    # Goal: Maximize sum of utilities.
    # For single-winner assumption (standard VSE): Best single party.
    total_utility_per_party = np.sum(utilities, axis=0)
    w_optimal = np.max(total_utility_per_party)

    # 2. W_random
    # Expected welfare of a random winner (standard VSE definition)
    w_random = np.mean(total_utility_per_party)

    # 3. W_actual
    # Weighted average of welfare provided by each party, weighted by their seat share.
    # (Assuming parliament utility is linear combination of party utilities)
    w_actual = np.sum(total_utility_per_party * seat_shares)

    if w_optimal == w_random:
        return 0.0  # Division by zero protection (all options equal)

    vse = (w_actual - w_random) / (w_optimal - w_random)
    return float(vse)
