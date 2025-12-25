"""
Coalition Formation Models

Implements:
- MCW (Minimum Connected Winning) coalitions
- MWC (Minimum Winning Coalition)
- Coalition strain calculation
"""

from itertools import combinations

import numpy as np


def minimum_winning_coalitions(
    seats: np.ndarray,
    majority_threshold: float = 0.5,
) -> list[tuple[list[int], int]]:
    """
    Find all Minimum Winning Coalitions (MWC).

    A MWC is a coalition where:
    - Total seats >= majority
    - Removing any party makes it lose majority

    Args:
        seats: Seat counts per party
        majority_threshold: Fraction of seats needed (default 0.5 = simple majority)

    Returns:
        List of (party_indices, total_seats) tuples
    """
    total_seats = seats.sum()
    majority = int(np.floor(total_seats * majority_threshold)) + 1
    n_parties = len(seats)

    mwcs = []

    # Check all possible coalitions (2^n - expensive for many parties!)
    for size in range(1, n_parties + 1):
        for coalition in combinations(range(n_parties), size):
            coalition_seats = sum(seats[p] for p in coalition)

            if coalition_seats >= majority:
                # Check if it's minimal (removing any party loses majority)
                is_minimal = True
                for party in coalition:
                    without_party = coalition_seats - seats[party]
                    if without_party >= majority:
                        is_minimal = False
                        break

                if is_minimal:
                    mwcs.append((list(coalition), coalition_seats))

    # Sort by size (fewest parties first)
    mwcs.sort(key=lambda x: len(x[0]))

    return mwcs


def minimum_connected_winning(
    seats: np.ndarray,
    positions: np.ndarray,
    majority_threshold: float = 0.5,
    max_distance: float = 1.0,
) -> list[tuple[list[int], int, float]]:
    """
    Find Minimum Connected Winning (MCW) coalitions.

    A MCW is a MWC where all parties are "connected" -
    within max_distance on the policy dimension.

    Args:
        seats: Seat counts per party
        positions: Policy positions (1D or use first dimension if 2D)
        majority_threshold: Fraction needed for majority
        max_distance: Maximum policy distance for "connected" parties

    Returns:
        List of (party_indices, total_seats, policy_range) tuples
    """
    # Use first dimension if 2D
    if positions.ndim == 2:
        positions = positions[:, 0]

    # Get all MWCs first
    mwcs = minimum_winning_coalitions(seats, majority_threshold)

    mcws = []
    for parties, total in mwcs:
        party_positions = positions[parties]
        policy_range = party_positions.max() - party_positions.min()

        # Check if all parties are within max_distance
        if policy_range <= max_distance:
            mcws.append((parties, total, policy_range))

    # Sort by policy range (most cohesive first)
    mcws.sort(key=lambda x: x[2])

    return mcws


def coalition_strain(
    positions: np.ndarray,
    weights: np.ndarray | None = None,
) -> float:
    """
    Calculate policy strain within a coalition.

    Strain = weighted average of pairwise policy distances.
    Higher strain = less stable coalition.

    Args:
        positions: Policy positions of coalition members (n_members x n_dimensions)
        weights: Optional weights (e.g., seat shares). Default: equal weights.

    Returns:
        Strain value (0 = perfect agreement, higher = more tension)
    """
    if positions.ndim == 1:
        positions = positions.reshape(-1, 1)

    n = len(positions)
    if n < 2:
        return 0.0

    if weights is None:
        weights = np.ones(n)
    weights = weights / weights.sum()

    # Calculate weighted pairwise distances
    total_strain = 0.0
    total_weight = 0.0

    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(positions[i] - positions[j])
            pair_weight = weights[i] * weights[j]
            total_strain += dist * pair_weight
            total_weight += pair_weight

    if total_weight == 0:
        return 0.0

    return total_strain / total_weight


def predict_coalition_stability(
    strain: float,
    majority_margin: float,
    n_parties: int,
    model: str = "sigmoid",
) -> float:
    """
    Predict coalition stability based on strain and composition.

    Args:
        strain: Policy strain (from coalition_strain())
        majority_margin: Seats above majority / total seats
        n_parties: Number of parties in coalition
        model: "sigmoid", "linear", or "exponential"

    Returns:
        Stability score (0-1, higher = more stable)
    """
    # Base stability from strain (inverted - lower strain = more stable)
    strain_factor = 1.0 / (1.0 + strain)

    # Majority margin factor (larger margin = more stable)
    margin_factor = 0.5 + 0.5 * np.clip(majority_margin * 5, 0, 1)

    # Party count penalty (more parties = less stable)
    party_factor = 1.0 / np.sqrt(n_parties)

    # Combine factors
    raw_stability = strain_factor * margin_factor * party_factor

    # Apply model transformation
    if model == "sigmoid":
        return 1.0 / (1.0 + np.exp(-5 * (raw_stability - 0.5)))
    elif model == "exponential":
        return 1.0 - np.exp(-3 * raw_stability)
    else:  # linear
        return np.clip(raw_stability, 0, 1)


def form_government(
    seats: np.ndarray,
    positions: np.ndarray,
    party_names: list[str] | None = None,
    majority_threshold: float = 0.5,
    office_weight: float | None = None,  # P4: Policy vs Office Tradeoff
) -> dict:
    """
    Form a government coalition.

    Args:
        seats: Seat counts
        positions: Policy positions
        party_names: Optional party names for output
        majority_threshold: Fraction needed for majority
        office_weight: If set, uses utility maximization with this weight for Office (vs Policy).

    Returns:
        Dictionary with coalition details
    """
    total_seats = seats.sum()
    majority = int(np.floor(total_seats * majority_threshold)) + 1

    if office_weight is not None:
        # P4: Utility-based formation
        coalition_parties, _ = form_coalition_with_utility(
            seats, positions, office_weight, majority_threshold
        )
        if not coalition_parties:
            return {
                "success": False,
                "reason": "No majority coalition possible (with utility)",
                "coalition": [],
                "seats": 0,
            }

        coalition_seats = sum(seats[p] for p in coalition_parties)
        coalition_positions = positions[coalition_parties]

    else:
        # Default Logic (MCW > MWC)
        # Find MCW coalitions
        mcws = minimum_connected_winning(seats, positions, majority_threshold)

        if not mcws:
            # No connected winning coalition - try regular MWC
            mwcs = minimum_winning_coalitions(seats, majority_threshold)
            if not mwcs:
                return {
                    "success": False,
                    "reason": "No majority coalition possible",
                    "coalition": [],
                    "seats": 0,
                }

            # Use smallest MWC
            coalition_parties, coalition_seats = mwcs[0]
            coalition_positions = positions[coalition_parties]
        else:
            # Use most cohesive MCW
            coalition_parties, coalition_seats, policy_range = mcws[0]
            coalition_positions = positions[coalition_parties]

    # Calculate coalition properties
    strain = coalition_strain(
        (
            coalition_positions
            if coalition_positions.ndim == 2
            else coalition_positions.reshape(-1, 1)
        ),
        seats[coalition_parties],
    )

    margin = (coalition_seats - majority) / total_seats
    stability = predict_coalition_stability(strain, margin, len(coalition_parties))

    if party_names:
        names = [party_names[p] for p in coalition_parties]
    else:
        names = [f"Party {p}" for p in coalition_parties]

    return {
        "success": True,
        "coalition": coalition_parties,
        "coalition_names": names,
        "seats": coalition_seats,
        "majority": majority,
        "margin": margin,
        "strain": strain,
        "stability": stability,
        "n_parties": len(coalition_parties),
    }


def junior_partner_penalty(
    seats: np.ndarray,
    coalition_parties: list[int],
    base_penalty: float = 0.15,
    dominant_bonus: float = 0.05,
) -> dict[int, float]:
    """
    Calculate expected vote loss for junior coalition partners.

    Research shows smaller parties in coalitions often lose votes in
    subsequent elections while the dominant partner may gain slightly.

    Args:
        seats: Seat counts per party
        coalition_parties: Indices of parties in coalition
        base_penalty: Maximum penalty for smallest partner (proportion, e.g. 0.15 = 15%)
        dominant_bonus: Bonus for the dominant partner (proportion)

    Returns:
        Dict mapping party index to expected vote change (-0.15 to +0.05)

    Example:
        >>> seats = np.array([200, 50, 30])  # 3-party coalition
        >>> penalties = junior_partner_penalty(seats, [0, 1, 2])
        >>> penalties  # {0: 0.05, 1: -0.10, 2: -0.15}
    """
    if len(coalition_parties) < 2:
        return dict.fromkeys(coalition_parties, 0.0)

    coalition_seats = seats[coalition_parties]
    total_coalition = coalition_seats.sum()

    # Find dominant party (largest in coalition)
    dominant_idx = coalition_parties[np.argmax(coalition_seats)]
    min_seats = coalition_seats.min()
    max_seats = coalition_seats.max()
    seat_range = max_seats - min_seats if max_seats > min_seats else 1

    penalties = {}
    for party in coalition_parties:
        if party == dominant_idx:
            # Dominant partner gets small bonus
            penalties[party] = dominant_bonus
        else:
            # Junior partners get penalty scaled by how small they are
            seat_share = seats[party] / total_coalition
            relative_size = (seats[party] - min_seats) / seat_range
            # Smaller relative size = larger penalty
            penalties[party] = -base_penalty * (1 - relative_size * 0.5)

    return penalties


def allocate_portfolios_laver_shepsle(
    coalition_parties: list[int],
    party_seats: np.ndarray,
    party_positions: np.ndarray,
    dimensions: list[str] | None = None,
) -> dict[str, int]:
    """
    Allocate cabinet portfolios using Laver-Shepsle (1996) logic.

    Principle:
    For each policy dimension (portfolio), the party holding the
    median legislator position *within the coalition* controls that ministry.

    Args:
        coalition_parties: Indices of parties in coalition
        party_seats: Array of seats for all parties
        party_positions: Array of positions (parties x dimensions)
        dimensions: Names of dimensions/portfolios (default: "Dim 1", "Dim 2"...)

    Returns:
        Dictionary mapping Portfolio Name -> Party Index

    Example:
        If Dim 1 is "Economy", the party with the median position on economy
        within the coalition gets the "Economy" portfolio.
    """
    n_dims = party_positions.shape[1]

    if dimensions is None:
        dimensions = [f"Ministry {i+1}" for i in range(n_dims)]
    elif len(dimensions) != n_dims:
        # Fallback if dimensions don't match
        dimensions = [f"Ministry {i+1}" for i in range(n_dims)]

    allocations = {}

    # Filter coalition data
    c_seats = party_seats[coalition_parties]
    c_positions = party_positions[coalition_parties]
    total_seats = c_seats.sum()
    median_threshold = total_seats / 2

    for dim_idx, pf_name in enumerate(dimensions):
        # customized logic for 1D case handling
        if n_dims == 1:
            dim_positions = c_positions  # already 1D
        else:
            dim_positions = c_positions[:, dim_idx]

        # Sort parties by position on this dimension
        sorted_indices = np.argsort(dim_positions)

        # Find accumulated seats to locate median
        cumulative_seats = 0
        median_party_idx = -1

        for i in sorted_indices:
            cumulative_seats += c_seats[i]
            if cumulative_seats > median_threshold:
                # This party contains the median legislator
                median_party_idx = coalition_parties[i]
                break

        allocations[pf_name] = median_party_idx

    return allocations


def form_coalition_with_utility(
    seats: np.ndarray,
    positions: np.ndarray,
    office_weight: float = 0.5,
    majority_threshold: float = 0.5,
) -> tuple[list[int], float]:
    """
    Form a coalition based on Policy vs Office tradeoffs (P4).

    Utility Function:
    U = alpha * OfficeUtility + (1 - alpha) * PolicyUtility

    - OfficeUtility: majority_threshold / coalition_size (Maximizes when size is minimal)
    - PolicyUtility: 1.0 - coalition_strain (Maximizes when ideologically compact)

    Args:
        seats: Seat counts
        positions: Party positions
        office_weight: alpha (0.0 = Pure Policy, 1.0 = Pure Office)
        majority_threshold: Threshold for majority

    Returns:
        (coalition_indices, utility_score)
    """
    total_seats = seats.sum()
    majority_needed = int(np.floor(total_seats * majority_threshold)) + 1

    # 1. Get Candidate Coalitions (MWCs are usually the only rational candidates for office seekers,
    # but strictly policy-seeking might tolerate oversized if it pulls policy closer?
    # For computation, we start with MWCs.
    # To be robust, we should consider all WCs, but that's O(2^N).
    # We'll generate MWCs + valid oversized "neighbours"?)
    # For now, let's stick to MWCs as the base set, as oversized usually drops office utility significantly
    # without always improving policy utility enough to compensate unless alpha is very low.

    candidates = minimum_winning_coalitions(seats, majority_threshold)

    best_coalition = []
    best_utility = -1.0

    for parties, size in candidates:
        # Calculate Office Utility
        # Normalized: minimal possible size / actual size
        # Approximated by majority_needed / size
        office_u = majority_needed / size

        # Calculate Policy Utility
        # 1 - strain
        party_pos = positions[parties]
        if positions.ndim == 2:
            party_pos = party_pos[:, 0]  # Use primary dimension

        mean_pos = np.average(party_pos, weights=seats[parties])
        # Strain: weighted mean distance from coalition center
        strain = np.average(np.abs(party_pos - mean_pos), weights=seats[parties])

        # Normalize strain? typically 0 to 0.5.
        # Let's use simple linear
        policy_u = max(0.0, 1.0 - (strain * 2.0))  # scale up strain impact

        # Total Utility
        utility = (office_weight * office_u) + ((1.0 - office_weight) * policy_u)

        if utility > best_utility:
            best_utility = utility
            best_coalition = parties

    return best_coalition, best_utility
