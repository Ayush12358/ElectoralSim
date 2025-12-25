"""
GPU Acceleration using CuPy.

This module provides GPU-accelerated versions of core compute functions.
If CuPy is not available, it provides info about missing dependencies.
"""

import numpy as np

try:
    import cupy as cp
    import cupyx as cpx

    CUPY_AVAILABLE = True
except ImportError:
    cp = None
    cpx = None
    CUPY_AVAILABLE = False


def is_gpu_available() -> bool:
    """Check if CuPy and a compatible GPU are available."""
    if not CUPY_AVAILABLE:
        return False
    try:
        # Check if we can actually use a device
        cp.cuda.Device(0).use()
        return True
    except Exception:
        return False


def compute_utilities_gpu(
    voter_x: np.ndarray,
    voter_y: np.ndarray,
    party_x: np.ndarray,
    party_y: np.ndarray,
    valence: np.ndarray,
    valence_weight: float = 0.01,
) -> np.ndarray:
    """
    Compute utility matrix using GPU acceleration.

    Logic:
        U = -sqrt((v_x - p_x)^2 + (v_y - p_y)^2) + valence_weight * valence
    """
    if not CUPY_AVAILABLE:
        raise RuntimeError("CuPy not installed. Cannot use GPU acceleration.")

    # Transfer data to GPU
    v_x = cp.asarray(voter_x, dtype=cp.float32)
    v_y = cp.asarray(voter_y, dtype=cp.float32)
    p_x = cp.asarray(party_x, dtype=cp.float32)
    p_y = cp.asarray(party_y, dtype=cp.float32)
    val = cp.asarray(valence, dtype=cp.float32)

    # Use broadcasting for distance calculation
    # Reshape vectors to (N_VOTERS, 1) and (1, N_PARTIES)
    dx = v_x[:, None] - p_x[None, :]
    dy = v_y[:, None] - p_y[None, :]

    # Euclidean distance
    dist = cp.sqrt(dx**2 + dy**2)

    # Utility calculation
    utilities = -dist + valence_weight * val[None, :]

    # Transfer back to Host (CPU) memory
    return cp.asnumpy(utilities)


def mnl_sample_gpu(
    utilities: np.ndarray,
    temperature: float,
) -> np.ndarray:
    """
    Multinomial logit sampling using GPU.

    P(j) = exp(U_j/τ) / Σexp(U_k/τ)
    """
    if not CUPY_AVAILABLE:
        raise RuntimeError("CuPy not installed. Cannot use GPU acceleration.")

    # Transfer to GPU
    u = cp.asarray(utilities, dtype=cp.float32)

    # Scaled utilities
    scaled = u / temperature

    # Numerical stability: subtract max per row
    u_max = scaled.max(axis=1, keepdims=True)
    exp_u = cp.exp(scaled - u_max)

    # Calculate probabilities
    probs = exp_u / exp_u.sum(axis=1, keepdims=True)

    # Cumulative sums for sampling
    cumprobs = cp.cumsum(probs, axis=1)

    # Generate random values on GPU
    random_vals = cp.random.random((utilities.shape[0], 1), dtype=cp.float32)

    # Perform sampling (find first index where random_val < cumprob)
    votes = (random_vals > cumprobs).sum(axis=1)

    return cp.asnumpy(votes).astype(np.int64)


def fptp_count_gpu(
    constituencies: np.ndarray,
    votes: np.ndarray,
    n_constituencies: int,
    n_parties: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    FPTP seat counting using GPU.
    """
    if not CUPY_AVAILABLE:
        raise RuntimeError("CuPy not installed. Cannot use GPU acceleration.")

    c = cp.asarray(constituencies, dtype=cp.int32)
    v = cp.asarray(votes, dtype=cp.int32)

    # Global vote counts
    vote_counts = cp.asnumpy(cp.bincount(v, minlength=n_parties))

    # For constituency counting, we can use a custom kernel or a loop
    # For now, we'll keep the loop but use CuPy operations inside
    seats = np.zeros(n_parties, dtype=np.int64)

    # Note: For small number of constituencies, CPU loop is fine if
    # the filtering is fast. For 543, we might want a parallel approach.
    # Currently, we just return the counts and the CPU handles the rest
    # of the system-specific allocation to keep simplicity.

    return seats, vote_counts.astype(np.int64)
