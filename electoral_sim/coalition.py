"""
Coalition Formation Models

Implements:
- MCW (Minimum Connected Winning) coalitions
- MWC (Minimum Winning Coalition)
- Coalition strain calculation
"""

import numpy as np
from itertools import combinations
from typing import Optional


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
    weights: Optional[np.ndarray] = None,
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
    party_names: Optional[list[str]] = None,
    majority_threshold: float = 0.5,
) -> dict:
    """
    Form a government by selecting the most stable MCW coalition.
    
    Args:
        seats: Seat counts per party
        positions: Policy positions
        party_names: Optional party names for output
        majority_threshold: Fraction needed for majority
        
    Returns:
        Dictionary with coalition details
    """
    total_seats = seats.sum()
    majority = int(np.floor(total_seats * majority_threshold)) + 1
    
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
        coalition_positions if coalition_positions.ndim == 2 else coalition_positions.reshape(-1, 1),
        seats[coalition_parties]
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
