"""
Alternative Voting Systems

Implements:
- Approval Voting
- Condorcet methods
- Borda Count
- Score (Range) Voting
- PAV (Proportional Approval Voting)

IRV and STV → systems/_ranked.py (extracted to keep files under 250 LOC).
"""

import numpy as np


def _validate_rankings(rankings: np.ndarray, n_candidates: int, name: str = "") -> None:
    """Validate ranked ballot array for common issues.

    Raises ValueError for: invalid shape, duplicate ranks, out-of-range ranks,
    non-positive n_candidates.
    """
    label = f" in {name}" if name else ""

    if n_candidates <= 0:
        raise ValueError(f"n_candidates must be positive, got {n_candidates}{label}")

    if not isinstance(rankings, np.ndarray) or rankings.ndim != 2:
        raise ValueError(
            f"rankings must be 2D array (n_voters, n_candidates), "
            f"got shape {getattr(rankings, 'shape', 'scalar')}{label}"
        )

    n_voters, n_cols = rankings.shape
    if n_cols != n_candidates:
        raise ValueError(
            f"rankings shape[1] ({n_cols}) must equal n_candidates ({n_candidates}){label}"
        )

    for i in range(n_voters):
        row = rankings[i]
        nonzero_ranks = row[row > 0]
        if len(set(nonzero_ranks)) != len(nonzero_ranks):
            raise ValueError(f"Duplicate ranks in voter {i}: {row.tolist()}{label}")
        if np.any((row < 0) | (row > n_candidates)):
            raise ValueError(f"Out-of-range ranks in voter {i}: {row.tolist()}{label}")


def borda_count(
    rankings: np.ndarray,
    n_candidates: int,
) -> dict:
    """
    Borda Count: candidates receive points based on rank position.

    For n candidates, 1st choice gets n-1 points, 2nd gets n-2 points,
    ..., last choice gets 0 points. Winner is the candidate with the
    highest total score.

    Args:
        rankings: (n_voters, n_candidates) array of rankings (1=first choice)
        n_candidates: Number of candidates

    Returns:
        Dictionary with winner and per-candidate scores
    """
    _validate_rankings(rankings, n_candidates, "borda_count")
    scores = np.zeros(n_candidates, dtype=np.float64)
    n_voters = len(rankings)

    for voter_ranks in rankings:
        for c in range(n_candidates):
            rank = voter_ranks[c]
            if rank > 0:  # 0 = unranked
                scores[c] += n_candidates - rank

    winner = int(np.argmax(scores)) if n_voters > 0 else -1
    return {
        "winner": winner,
        "scores": scores,
    }


def score_voting(
    utilities: np.ndarray,
    n_candidates: int,
    max_score: int = 10,
) -> dict:
    """
    Score (Range) Voting: voters assign scores to candidates.

    Winner is the candidate with the highest total score. Utilities
    are scaled to the range [0, max_score] based on min-max per voter.

    Args:
        utilities: (n_voters, n_candidates) utility matrix
        n_candidates: Number of candidates
        max_score: Maximum score per voter (default 10)

    Returns:
        Dictionary with winner and per-candidate total scores
    """
    n_voters = len(utilities)
    scores = np.zeros(n_candidates, dtype=np.float64)

    for i in range(n_voters):
        u = utilities[i]
        u_min, u_max = u.min(), u.max()
        if u_max > u_min:
            scaled = max_score * (u - u_min) / (u_max - u_min)
        else:
            scaled = np.zeros(n_candidates)
        scores += scaled

    winner = int(np.argmax(scores)) if n_voters > 0 else -1
    return {
        "winner": winner,
        "scores": scores,
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
    winner = int(np.argmax(approval_counts)) if len(approvals) > 0 else -1
    approval_shares = (
        approval_counts / len(approvals) if len(approvals) > 0 else np.zeros(n_candidates)
    )

    return {
        "winner": winner,
        "approval_counts": approval_counts,
        "approval_shares": approval_shares,
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
    _validate_rankings(rankings, n_candidates, "condorcet_winner")
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


def pav_committee(
    approvals: np.ndarray,
    n_candidates: int,
    committee_size: int,
) -> dict:
    """
    Proportional Approval Voting (PAV) for multi-winner committees.

    Sequentially selects the candidate who adds the most marginal
    voter satisfaction. Each voter's satisfaction for a committee
    with k of their approved candidates is: 1 + 1/2 + ... + 1/k.

    Args:
        approvals: (n_voters, n_candidates) boolean array
        n_candidates: Number of candidates
        committee_size: Number of seats to fill

    Returns:
        Dictionary with committee list and per-candidate scores
    """
    n_voters = len(approvals)
    if n_voters == 0 or committee_size <= 0:
        return {"committee": [], "scores": np.zeros(n_candidates)}

    committee = []
    voter_counts = np.ones(n_voters, dtype=np.float64)  # 1/(1 + approved_in_committee)

    for _ in range(min(committee_size, n_candidates)):
        best_score = -1.0
        best_candidate = -1
        for c in range(n_candidates):
            if c in committee:
                continue
            marginal = 0.0
            for v in range(n_voters):
                if approvals[v, c]:
                    marginal += 1.0 / voter_counts[v]
            if marginal > best_score:
                best_score = marginal
                best_candidate = c
        if best_candidate >= 0:
            committee.append(best_candidate)
            for v in range(n_voters):
                if approvals[v, best_candidate]:
                    voter_counts[v] += 1.0

    scores = np.zeros(n_candidates)
    for c in committee:
        for v in range(n_voters):
            if approvals[v, c]:
                scores[c] += 1.0 / (voter_counts[v] - 0.5)  # approximate per-voter score

    return {"committee": committee, "scores": scores}


# =============================================================================
# QUICK TEST
# =============================================================================

if __name__ == "__main__":
    from electoral_sim.systems._ranked import irv_election, stv_election

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
