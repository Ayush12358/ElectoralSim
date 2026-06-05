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
Vote Counting Module

Contains functions for counting votes under different electoral systems.
"""

from typing import Literal

import numpy as np

from electoral_sim.engine.numba_accel import fptp_count_fast


def count_fptp(
    constituencies: np.ndarray,
    votes: np.ndarray,
    n_constituencies: int,
    n_parties: int,
) -> dict:
    """
    First Past The Post: winner takes all in each constituency.

    Uses Numba parallel acceleration when available.

    Args:
        constituencies: Array of constituency assignments per voter
        votes: Array of vote choices (party indices)
        n_constituencies: Total number of constituencies
        n_parties: Number of parties

    Returns:
        Dictionary with seats and vote counts
    """
    seats, vote_counts = fptp_count_fast(constituencies, votes, n_constituencies, n_parties)

    return {
        "system": "FPTP",
        "seats": seats,
        "vote_counts": vote_counts,
        "n_constituencies": n_constituencies,
    }


def count_pr(
    votes: np.ndarray,
    n_parties: int,
    n_seats: int,
    allocation_method: Literal["dhondt", "sainte_lague", "hare", "droop"] = "dhondt",
    threshold: float = 0.0,
) -> dict:
    """
    Proportional Representation with seat allocation.

    Args:
        votes: Array of vote choices (party indices)
        n_parties: Number of parties
        n_seats: Total seats to allocate
        allocation_method: Allocation algorithm
        threshold: Minimum vote share for representation

    Returns:
        Dictionary with seats and vote counts
    """
    from electoral_sim.systems.allocation import allocate_seats

    # Vectorized vote counting
    vote_counts = np.bincount(votes, minlength=n_parties).astype(np.int64)

    # Allocate seats
    seats = allocate_seats(vote_counts, n_seats, allocation_method, threshold)

    return {
        "system": "PR",
        "method": allocation_method,
        "seats": seats,
        "vote_counts": vote_counts,
        "n_seats": n_seats,
    }
