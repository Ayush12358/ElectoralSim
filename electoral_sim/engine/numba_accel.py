"""
Numba-accelerated functions for electoral simulation.

These JIT-compiled functions provide 10-50x speedup for hot loops.
Falls back to pure NumPy if Numba is not available.
"""

import numpy as np

try:
    from numba import jit, prange

    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False

    # Create no-op decorator
    def jit(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    prange = range


# =============================================================================
# SEAT ALLOCATION (Numba-accelerated)
# =============================================================================


@jit(nopython=True, cache=True)
def dhondt_numba(votes: np.ndarray, n_seats: int) -> np.ndarray:
    """
    D'Hondt allocation - Numba accelerated.

    ~10-20x faster than pure Python for large n_seats.
    """
    n_parties = len(votes)
    seats = np.zeros(n_parties, dtype=np.int64)
    votes_float = votes.astype(np.float64)

    for _ in range(n_seats):
        # Find party with highest quotient
        max_quotient = -1.0
        winner = 0
        for p in range(n_parties):
            quotient = votes_float[p] / (seats[p] + 1)
            if quotient > max_quotient:
                max_quotient = quotient
                winner = p
        seats[winner] += 1

    return seats


@jit(nopython=True, cache=True)
def sainte_lague_numba(votes: np.ndarray, n_seats: int) -> np.ndarray:
    """
    Sainte-Laguë allocation - Numba accelerated.

    Uses divisors 1, 3, 5, 7, ...
    """
    n_parties = len(votes)
    seats = np.zeros(n_parties, dtype=np.int64)
    votes_float = votes.astype(np.float64)

    for _ in range(n_seats):
        max_quotient = -1.0
        winner = 0
        for p in range(n_parties):
            divisor = 2 * seats[p] + 1
            quotient = votes_float[p] / divisor
            if quotient > max_quotient:
                max_quotient = quotient
                winner = p
        seats[winner] += 1

    return seats


@jit(nopython=True, cache=True, parallel=True)
def fptp_count_numba(
    constituencies: np.ndarray,
    votes: np.ndarray,
    n_constituencies: int,
    n_parties: int,
) -> np.ndarray:
    """
    Count FPTP seats - Numba parallel accelerated.

    Uses parallel processing across constituencies.
    """
    seats = np.zeros(n_parties, dtype=np.int64)

    # Process each constituency in parallel
    for c in prange(n_constituencies):
        # Count votes per party in this constituency
        party_votes = np.zeros(n_parties, dtype=np.int64)

        for i in range(len(constituencies)):
            if constituencies[i] == c:
                party_votes[votes[i]] += 1

        # Find winner
        max_votes = 0
        winner = 0
        for p in range(n_parties):
            if party_votes[p] > max_votes:
                max_votes = party_votes[p]
                winner = p

        if max_votes > 0:
            seats[winner] += 1

    return seats


@jit(nopython=True, cache=True, parallel=True)
def compute_utilities_numba(
    voter_x: np.ndarray,
    voter_y: np.ndarray,
    party_x: np.ndarray,
    party_y: np.ndarray,
    valence: np.ndarray,
    valence_weight: float = 0.01,
) -> np.ndarray:
    """
    Compute utility matrix using proximity model - Numba parallel.

    Utility = -distance + valence_weight * valence
    """
    n_voters = len(voter_x)
    n_parties = len(party_x)
    utilities = np.zeros((n_voters, n_parties), dtype=np.float64)

    for i in prange(n_voters):
        for p in range(n_parties):
            dist_x = voter_x[i] - party_x[p]
            dist_y = voter_y[i] - party_y[p]
            distance = np.sqrt(dist_x * dist_x + dist_y * dist_y)
            utilities[i, p] = -distance + valence_weight * valence[p]

    return utilities


def fptp_count_fast(
    constituencies: np.ndarray,
    votes: np.ndarray,
    n_constituencies: int,
    n_parties: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Fast FPTP counting - returns (seats, vote_counts).

    Uses Numba when available, else vectorized NumPy with bincount.
    """
    # Vote counts is always fast with bincount
    vote_counts = np.bincount(votes, minlength=n_parties).astype(np.int64)

    if NUMBA_AVAILABLE:
        seats = fptp_count_numba(
            constituencies.astype(np.int64),
            votes.astype(np.int64),
            n_constituencies,
            n_parties,
        )
    else:
        # Fallback: use vectorized operations
        seats = np.zeros(n_parties, dtype=np.int64)
        for c in range(n_constituencies):
            mask = constituencies == c
            if mask.sum() == 0:
                continue
            c_votes = votes[mask]
            party_votes = np.bincount(c_votes, minlength=n_parties)
            winner = np.argmax(party_votes)
            seats[winner] += 1

    return seats, vote_counts


# =============================================================================
# MNL VOTING (Numba-accelerated sampling)
# =============================================================================


@jit(nopython=True, cache=True, parallel=True)
def mnl_sample_numba(
    utilities: np.ndarray,
    temperature: float,
    random_vals: np.ndarray,
) -> np.ndarray:
    """
    Multinomial logit sampling - Numba parallel.

    P(j) = exp(U_j/τ) / Σexp(U_k/τ)
    """
    n_voters, n_parties = utilities.shape
    votes = np.zeros(n_voters, dtype=np.int64)

    for i in prange(n_voters):
        # Compute softmax (numerically stable)
        max_u = utilities[i, 0]
        for p in range(1, n_parties):
            if utilities[i, p] > max_u:
                max_u = utilities[i, p]

        exp_sum = 0.0
        for p in range(n_parties):
            exp_sum += np.exp((utilities[i, p] - max_u) / temperature)

        # Compute cumulative probabilities and sample
        cumprob = 0.0
        for p in range(n_parties):
            prob = np.exp((utilities[i, p] - max_u) / temperature) / exp_sum
            cumprob += prob
            if random_vals[i] < cumprob:
                votes[i] = p
                break

    return votes


# =============================================================================
# WRAPPER FUNCTIONS (with threshold support)
# =============================================================================


def dhondt_fast(votes: np.ndarray, n_seats: int, threshold: float = 0.0) -> np.ndarray:
    """D'Hondt with threshold - uses Numba if available."""
    votes = votes.astype(np.float64)

    if threshold > 0:
        total = votes.sum()
        votes = np.where(votes / total >= threshold, votes, 0)

    if NUMBA_AVAILABLE:
        return dhondt_numba(votes.astype(np.int64), n_seats)
    else:
        # Fallback to pure NumPy
        n_parties = len(votes)
        seats = np.zeros(n_parties, dtype=np.int64)
        for _ in range(n_seats):
            quotients = votes / (seats + 1)
            winner = np.argmax(quotients)
            seats[winner] += 1
        return seats


def sainte_lague_fast(votes: np.ndarray, n_seats: int, threshold: float = 0.0) -> np.ndarray:
    """Sainte-Laguë with threshold - uses Numba if available."""
    votes = votes.astype(np.float64)

    if threshold > 0:
        total = votes.sum()
        votes = np.where(votes / total >= threshold, votes, 0)

    if NUMBA_AVAILABLE:
        return sainte_lague_numba(votes.astype(np.int64), n_seats)
    else:
        n_parties = len(votes)
        seats = np.zeros(n_parties, dtype=np.int64)
        for _ in range(n_seats):
            quotients = votes / (2 * seats + 1)
            winner = np.argmax(quotients)
            seats[winner] += 1
        return seats


def vote_mnl_fast(utilities: np.ndarray, temperature: float, rng) -> np.ndarray:
    """MNL voting with Numba acceleration."""
    random_vals = rng.random(len(utilities))

    if NUMBA_AVAILABLE:
        return mnl_sample_numba(utilities, temperature, random_vals)
    else:
        # Fallback to vectorized NumPy
        scaled = utilities / temperature
        scaled -= scaled.max(axis=1, keepdims=True)
        exp_utils = np.exp(scaled)
        probs = exp_utils / exp_utils.sum(axis=1, keepdims=True)
        cumprobs = np.cumsum(probs, axis=1)
        return (random_vals[:, np.newaxis] > cumprobs).sum(axis=1)


# =============================================================================
# BENCHMARK UTILITY
# =============================================================================


def benchmark_numba():
    """Run benchmark comparing Numba vs pure Python."""
    import time

    print("=" * 50)
    print("Numba Acceleration Benchmark")
    print("=" * 50)
    print(f"Numba available: {NUMBA_AVAILABLE}")

    # Test data
    votes = np.array([10000, 8000, 5000, 3000, 2000, 1000, 500], dtype=np.int64)
    n_seats = 100

    # Warm up JIT
    if NUMBA_AVAILABLE:
        _ = dhondt_numba(votes, 10)
        _ = sainte_lague_numba(votes, 10)

    # D'Hondt benchmark
    start = time.perf_counter()
    for _ in range(100):
        _ = dhondt_fast(votes, n_seats)
    numba_time = time.perf_counter() - start

    # Pure Python comparison
    start = time.perf_counter()
    for _ in range(100):
        n_parties = len(votes)
        seats = np.zeros(n_parties, dtype=np.int64)
        for _ in range(n_seats):
            quotients = votes / (seats + 1)
            seats[np.argmax(quotients)] += 1
    python_time = time.perf_counter() - start

    print(f"\nD'Hondt ({n_seats} seats, 100 iterations):")
    print(f"  Numba:  {numba_time*1000:.2f} ms")
    print(f"  Python: {python_time*1000:.2f} ms")
    print(f"  Speedup: {python_time/numba_time:.1f}x")

    # MNL benchmark
    n_voters = 100_000
    n_parties = 7
    utilities = np.random.randn(n_voters, n_parties)
    rng = np.random.default_rng(42)

    # Warm up
    if NUMBA_AVAILABLE:
        _ = vote_mnl_fast(utilities[:1000], 0.5, rng)

    start = time.perf_counter()
    _ = vote_mnl_fast(utilities, 0.5, rng)
    mnl_time = time.perf_counter() - start

    print(f"\nMNL Voting ({n_voters:,} voters, {n_parties} parties):")
    print(f"  Time: {mnl_time*1000:.2f} ms")

    print("=" * 50)


if __name__ == "__main__":
    benchmark_numba()
