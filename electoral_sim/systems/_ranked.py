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

"""Ranked-choice voting systems: IRV and STV.

Extracted from alternative.py to keep each file under the 250-LOC ceiling.
"""

import numpy as np

from electoral_sim.systems.alternative import _validate_rankings


def irv_election(
    rankings: np.ndarray,
    n_candidates: int,
) -> dict:
    """Instant Runoff Voting (Ranked Choice Voting).

    Process:
    1. Count first-choice votes
    2. If a candidate has majority, they win
    3. Otherwise, eliminate last-place candidate
    4. Transfer eliminated candidate's votes to next preference
    5. Repeat until one candidate has majority

    Args:
        rankings: (n_voters, n_candidates) array of rankings (1=first choice, 2=second, etc.)
                  0 or -1 means unranked
        n_candidates: Number of candidates

    Returns:
        Dictionary with winner, round results, and elimination order
    """
    n_voters = len(rankings)
    _validate_rankings(rankings, n_candidates, "irv_election")
    eliminated = set()
    rounds = []
    elimination_order = []

    while len(eliminated) < n_candidates - 1:
        vote_counts = np.zeros(n_candidates, dtype=np.int64)

        for voter_ranks in rankings:
            for pref in range(1, n_candidates + 1):
                candidates_at_pref = np.where(voter_ranks == pref)[0]
                for c in candidates_at_pref:
                    if c not in eliminated:
                        vote_counts[c] += 1
                        break
                else:
                    continue
                break

        active_votes = vote_counts.sum()
        rounds.append(
            {
                "vote_counts": vote_counts.copy(),
                "eliminated": list(eliminated),
            }
        )

        max_votes = vote_counts.max()
        if max_votes > active_votes / 2:
            winner = int(np.argmax(vote_counts))
            return {
                "winner": winner,
                "rounds": rounds,
                "elimination_order": elimination_order,
                "final_votes": vote_counts,
            }

        min_votes = float("inf")
        to_eliminate = -1
        for c in range(n_candidates):
            if c not in eliminated and vote_counts[c] < min_votes:
                min_votes = vote_counts[c]
                to_eliminate = c

        eliminated.add(to_eliminate)
        elimination_order.append(to_eliminate)

    for c in range(n_candidates):
        if c not in eliminated:
            winner = c
            break

    final_tally = rounds[-1]["vote_counts"] if rounds else np.zeros(n_candidates)

    return {
        "winner": winner,
        "rounds": rounds,
        "elimination_order": elimination_order,
        "final_votes": final_tally,
    }


def stv_election(
    rankings: np.ndarray,
    n_candidates: int,
    n_seats: int,
) -> dict:
    """Single Transferable Vote (STV) for multi-winner elections.

    Uses Droop quota: floor(votes / (seats + 1)) + 1

    Args:
        rankings: (n_voters, n_candidates) ranking array
        n_candidates: Number of candidates
        n_seats: Number of seats to fill

    Returns:
        Dictionary with elected candidates, rounds, and transfer details
    """
    n_voters = len(rankings)
    _validate_rankings(rankings, n_candidates, "stv_election")
    quota = int(np.floor(n_voters / (n_seats + 1))) + 1

    weights = np.ones(n_voters, dtype=np.float64)
    elected = []
    eliminated = set()
    rounds = []

    while len(elected) < n_seats and len(eliminated) + len(elected) < n_candidates:
        vote_counts = np.zeros(n_candidates, dtype=np.float64)

        for i, voter_ranks in enumerate(rankings):
            for pref in range(1, n_candidates + 1):
                candidates_at_pref = np.where(voter_ranks == pref)[0]
                for c in candidates_at_pref:
                    if c not in eliminated and c not in elected:
                        vote_counts[c] += weights[i]
                        break
                else:
                    continue
                break

        rounds.append(
            {
                "vote_counts": vote_counts.copy(),
                "elected": list(elected),
                "eliminated": list(eliminated),
                "quota": quota,
            }
        )

        above_quota = [
            c
            for c in range(n_candidates)
            if c not in elected and c not in eliminated and vote_counts[c] >= quota
        ]

        if above_quota:
            best = max(above_quota, key=lambda c: vote_counts[c])
            elected.append(best)

            surplus = vote_counts[best] - quota
            if surplus > 0 and len(elected) < n_seats:
                transfer_ratio = surplus / vote_counts[best]

                for i, voter_ranks in enumerate(rankings):
                    for pref in range(1, n_candidates + 1):
                        candidates_at_pref = np.where(voter_ranks == pref)[0]
                        for c in candidates_at_pref:
                            if c == best:
                                weights[i] *= transfer_ratio
                                break
                            elif c not in eliminated and c not in elected:
                                break
                        else:
                            continue
                        break
        else:
            min_votes = float("inf")
            to_eliminate = -1
            for c in range(n_candidates):
                if c not in eliminated and c not in elected:
                    if vote_counts[c] < min_votes:
                        min_votes = vote_counts[c]
                        to_eliminate = c

            if to_eliminate >= 0:
                eliminated.add(to_eliminate)

    remaining = [
        (c, vote_counts[c]) for c in range(n_candidates) if c not in elected and c not in eliminated
    ]
    remaining.sort(key=lambda x: -x[1])
    for c, _ in remaining:
        if len(elected) >= n_seats:
            break
        elected.append(c)

    return {
        "elected": elected,
        "rounds": rounds,
        "n_seats": n_seats,
        "quota": quota,
    }
