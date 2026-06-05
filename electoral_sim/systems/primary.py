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
Primary Election and Candidate Selection Systems.

Supports closed primaries (only registered party members vote),
open primaries (any voter can participate), and candidate field
selection with valence-based general election handoff.
"""

import numpy as np


def closed_primary(
    voter_utilities: np.ndarray,
    party_affiliation: np.ndarray,
    party_id: int,
) -> dict:
    """
    Closed primary: only voters registered with the party can vote.

    Args:
        voter_utilities: (n_voters, n_candidates) utility matrix
        party_affiliation: (n_voters,) party ID for each voter
        party_id: Party conducting the primary

    Returns:
        Dict with 'winner' (candidate index with highest utility
        among party voters) and 'vote_counts'
    """
    mask = party_affiliation == party_id
    if not mask.any():
        return {"winner": -1, "vote_counts": np.zeros(voter_utilities.shape[1])}

    party_voters = voter_utilities[mask]
    scores = party_voters.sum(axis=0)
    winner = int(np.argmax(scores))
    return {"winner": winner, "vote_counts": scores}


def open_primary(
    voter_utilities: np.ndarray,
) -> dict:
    """
    Open primary: any voter can vote in the primary.

    Args:
        voter_utilities: (n_voters, n_candidates) utility matrix

    Returns:
        Dict with 'winner' (candidate with highest total utility)
        and 'vote_counts'
    """
    scores = voter_utilities.sum(axis=0)
    winner = int(np.argmax(scores))
    return {"winner": winner, "vote_counts": scores}


def candidate_selection(
    n_parties: int,
    n_candidates_per_party: int = 3,
    base_valence: float = 50.0,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    Generate candidate valence scores for each party's candidate field.

    Candidates within a party have valence values distributed around
    the party's base valence. The highest-valence candidate becomes
    the general election nominee.

    Args:
        n_parties: Number of parties
        n_candidates_per_party: Candidates per party primary
        base_valence: Mean candidate valence
        rng: Random generator

    Returns:
        (n_parties, n_candidates_per_party) valence matrix
    """
    if rng is None:
        rng = np.random.default_rng()

    valence = base_valence + rng.normal(0, 10, (n_parties, n_candidates_per_party))
    return np.clip(valence, 0, 100)
