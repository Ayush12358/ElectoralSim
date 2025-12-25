"""
Alternative Voting Systems

Implements:
- IRV/RCV (Instant Runoff Voting / Ranked Choice Voting)
- STV (Single Transferable Vote)
- Approval Voting
- Condorcet methods
"""

import numpy as np


def irv_election(
    rankings: np.ndarray,
    n_candidates: int,
) -> dict:
    """
    Instant Runoff Voting (Ranked Choice Voting).

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
    eliminated = set()
    rounds = []
    elimination_order = []

    while len(eliminated) < n_candidates - 1:
        # Count first-choice votes among non-eliminated candidates
        vote_counts = np.zeros(n_candidates, dtype=np.int64)

        for voter_ranks in rankings:
            # Find highest-ranked non-eliminated candidate
            for pref in range(1, n_candidates + 1):
                candidates_at_pref = np.where(voter_ranks == pref)[0]
                for c in candidates_at_pref:
                    if c not in eliminated:
                        vote_counts[c] += 1
                        break
                else:
                    continue
                break

        # Record round
        active_votes = vote_counts.sum()
        rounds.append(
            {
                "vote_counts": vote_counts.copy(),
                "eliminated": list(eliminated),
            }
        )

        # Check for majority
        max_votes = vote_counts.max()
        if max_votes > active_votes / 2:
            winner = int(np.argmax(vote_counts))
            return {
                "winner": winner,
                "rounds": rounds,
                "elimination_order": elimination_order,
                "final_votes": vote_counts,
            }

        # Eliminate candidate with fewest votes (among non-eliminated)
        min_votes = float("inf")
        to_eliminate = -1
        for c in range(n_candidates):
            if c not in eliminated and vote_counts[c] < min_votes:
                min_votes = vote_counts[c]
                to_eliminate = c

        eliminated.add(to_eliminate)
        elimination_order.append(to_eliminate)

    # Last remaining candidate wins
    for c in range(n_candidates):
        if c not in eliminated:
            winner = c
            break

    return {
        "winner": winner,
        "rounds": rounds,
        "elimination_order": elimination_order,
        "final_votes": np.zeros(n_candidates),
    }


def stv_election(
    rankings: np.ndarray,
    n_candidates: int,
    n_seats: int,
) -> dict:
    """
    Single Transferable Vote (STV) for multi-winner elections.

    Uses Droop quota: floor(votes / (seats + 1)) + 1

    Args:
        rankings: (n_voters, n_candidates) ranking array
        n_candidates: Number of candidates
        n_seats: Number of seats to fill

    Returns:
        Dictionary with elected candidates, rounds, and transfer details
    """
    n_voters = len(rankings)

    # Droop quota
    quota = int(np.floor(n_voters / (n_seats + 1))) + 1

    # Track vote weights (for surplus transfers)
    weights = np.ones(n_voters, dtype=np.float64)

    elected = []
    eliminated = set()
    rounds = []

    while len(elected) < n_seats and len(eliminated) + len(elected) < n_candidates:
        # Count weighted first-preference votes
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

        # Check for candidates reaching quota
        above_quota = [
            c
            for c in range(n_candidates)
            if c not in elected and c not in eliminated and vote_counts[c] >= quota
        ]

        if above_quota:
            # Elect candidate with most votes
            best = max(above_quota, key=lambda c: vote_counts[c])
            elected.append(best)

            # Transfer surplus votes
            surplus = vote_counts[best] - quota
            if surplus > 0 and len(elected) < n_seats:
                transfer_ratio = surplus / vote_counts[best]

                # Reduce weights for voters who had this candidate as first preference
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
            # No one reached quota - eliminate lowest
            min_votes = float("inf")
            to_eliminate = -1
            for c in range(n_candidates):
                if c not in eliminated and c not in elected:
                    if vote_counts[c] < min_votes:
                        min_votes = vote_counts[c]
                        to_eliminate = c

            if to_eliminate >= 0:
                eliminated.add(to_eliminate)

    return {
        "elected": elected,
        "rounds": rounds,
        "n_seats": n_seats,
        "quota": quota,
    }


def approval_voting(
    approvals: np.ndarray,
    n_candidates: int,
) -> dict:
    """
    Approval voting: voters can approve any number of candidates.
    Winner is candidate with most approvals.

    Args:
        approvals: (n_voters, n_candidates) boolean array (True = approved)
        n_candidates: Number of candidates

    Returns:
        Dictionary with winner and approval counts
    """
    approval_counts = approvals.sum(axis=0)
    winner = int(np.argmax(approval_counts))

    return {
        "winner": winner,
        "approval_counts": approval_counts,
        "approval_shares": approval_counts / len(approvals),
    }


def condorcet_winner(
    rankings: np.ndarray,
    n_candidates: int,
) -> dict:
    """
    Find Condorcet winner (if exists): candidate who beats all others head-to-head.

    Args:
        rankings: (n_voters, n_candidates) ranking array
        n_candidates: Number of candidates

    Returns:
        Dictionary with winner (or None if no Condorcet winner) and pairwise matrix
    """
    n_voters = len(rankings)

    # Build pairwise comparison matrix
    # pairwise[i,j] = how many voters prefer i over j
    pairwise = np.zeros((n_candidates, n_candidates), dtype=np.int64)

    for voter_ranks in rankings:
        for i in range(n_candidates):
            for j in range(n_candidates):
                if i == j:
                    continue
                rank_i = voter_ranks[i] if voter_ranks[i] > 0 else 999
                rank_j = voter_ranks[j] if voter_ranks[j] > 0 else 999
                if rank_i < rank_j:  # Lower rank = better
                    pairwise[i, j] += 1

    # Find Condorcet winner: beats all others
    condorcet = None
    for c in range(n_candidates):
        beats_all = True
        for other in range(n_candidates):
            if c != other and pairwise[c, other] <= pairwise[other, c]:
                beats_all = False
                break
        if beats_all:
            condorcet = c
            break

    return {
        "condorcet_winner": condorcet,
        "pairwise_matrix": pairwise,
        "has_condorcet": condorcet is not None,
    }


def generate_rankings(
    utilities: np.ndarray,
    n_ranked: int | None = None,
) -> np.ndarray:
    """
    Generate ranked ballots from utility scores.

    Args:
        utilities: (n_voters, n_candidates) utility scores
        n_ranked: Max candidates to rank (None = rank all)

    Returns:
        (n_voters, n_candidates) ranking array
    """
    n_voters, n_candidates = utilities.shape

    if n_ranked is None:
        n_ranked = n_candidates

    # Sort by utility (descending)
    order = np.argsort(-utilities, axis=1)

    # Convert to rankings
    rankings = np.zeros_like(utilities, dtype=np.int64)
    for i in range(n_voters):
        for rank, candidate in enumerate(order[i]):
            if rank < n_ranked:
                rankings[i, candidate] = rank + 1

    return rankings


# =============================================================================
# QUICK TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Alternative Voting Systems Test")
    print("=" * 50)

    np.random.seed(42)
    n_voters = 1000
    n_candidates = 5

    # Generate random rankings
    utilities = np.random.randn(n_voters, n_candidates)
    rankings = generate_rankings(utilities)

    # IRV
    print("\n1. IRV/RCV:")
    result = irv_election(rankings, n_candidates)
    print(f"   Winner: Candidate {result['winner']}")
    print(f"   Rounds: {len(result['rounds'])}")
    print(f"   Elimination order: {result['elimination_order']}")

    # STV
    print("\n2. STV (3 seats):")
    result = stv_election(rankings, n_candidates, n_seats=3)
    print(f"   Elected: {result['elected']}")
    print(f"   Quota: {result['quota']}")

    # Condorcet
    print("\n3. Condorcet:")
    result = condorcet_winner(rankings, n_candidates)
    print(f"   Condorcet winner: {result['condorcet_winner']}")

    # Approval
    approvals = utilities > 0  # Approve if positive utility
    print("\n4. Approval Voting:")
    result = approval_voting(approvals, n_candidates)
    print(f"   Winner: Candidate {result['winner']}")
    print(f"   Approval counts: {result['approval_counts']}")

    print("=" * 50)
