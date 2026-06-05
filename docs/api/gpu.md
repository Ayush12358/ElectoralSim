# GPU Acceleration

GPU-accelerated compute kernels using CuPy for utility computation and multinomial logit sampling.

> **Requires:** CuPy (`pip install cupy` or `pip install electoral-sim[gpu]`). Falls back to informational messages when CuPy is unavailable.

---

## is_gpu_available

Check whether CuPy and a compatible GPU are available.

```python
from electoral_sim.engine.gpu_accel import is_gpu_available

if is_gpu_available():
    print("GPU acceleration ready")
else:
    print("Using CPU-only path")
```

**Returns:** `bool` — `True` if CuPy is importable and a CUDA device can be used.

**Note:** Always call this before invoking other GPU functions, which raise `RuntimeError` on failure.

---

## compute_utilities_gpu

Compute a utility matrix using GPU acceleration with CuPy broadcasting.

```python
from electoral_sim.engine.gpu_accel import compute_utilities_gpu

utilities = compute_utilities_gpu(
    voter_x=voter_x,
    voter_y=voter_y,
    party_x=party_x,
    party_y=party_y,
    valence=valence,
    valence_weight=0.01,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `voter_x` | `np.ndarray` | `(n_voters,)` economic left-right positions |
| `voter_y` | `np.ndarray` | `(n_voters,)` social positions |
| `party_x` | `np.ndarray` | `(n_parties,)` party economic positions |
| `party_y` | `np.ndarray` | `(n_parties,)` party social positions |
| `valence` | `np.ndarray` | `(n_parties,)` valence scores |
| `valence_weight` | float | Weight for valence term (default `0.01`) |

**Returns:** `(n_voters, n_parties)` utility matrix (NumPy array on CPU).

**Formula:**
```
U = -sqrt((v_x - p_x)^2 + (v_y - p_y)^2) + valence_weight * valence
```

**Performance:** For 1M voters × 10 parties, GPU achieves ~10-20x speedup over CPU path. Data is transferred to GPU, computed in float32, and results are transferred back as float64.

**Example:**
```python
import numpy as np
from electoral_sim.engine.gpu_accel import is_gpu_available, compute_utilities_gpu

if is_gpu_available():
    voter_x = np.random.uniform(-1, 1, 100_000)
    voter_y = np.random.uniform(-1, 1, 100_000)
    party_x = np.linspace(-0.8, 0.8, 5)
    party_y = np.zeros(5)
    valence = np.array([50, 45, 40, 55, 35])

    utils = compute_utilities_gpu(voter_x, voter_y, party_x, party_y, valence)
    print(f"Utility matrix shape: {utils.shape}")
```

---

## mnl_sample_gpu

Multinomial logit sampling using GPU for vote choice generation.

```python
from electoral_sim.engine.gpu_accel import mnl_sample_gpu

votes = mnl_sample_gpu(utilities=utilities, temperature=0.5)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `utilities` | `np.ndarray` | `(n_voters, n_parties)` utility matrix |
| `temperature` | float | Logit temperature τ — lower = more deterministic |

**Returns:** `(n_voters,)` integer array of chosen party indices.

**Algorithm:**
```
P(j) = exp(U_j / τ) / Σ exp(U_k / τ)
```

Numerically stabilized by subtracting row-max before exponentiation. Random sampling uses CuPy's built-in random number generator.

**Example:**
```python
import numpy as np
from electoral_sim.engine.gpu_accel import is_gpu_available, compute_utilities_gpu, mnl_sample_gpu

if is_gpu_available():
    # Generate utilities on GPU
    utils = compute_utilities_gpu(voter_x, voter_y, party_x, party_y, valence)

    # Sample votes with different temperatures
    deterministic = mnl_sample_gpu(utils, temperature=0.1)  # Almost argmax
    probabilistic = mnl_sample_gpu(utils, temperature=1.0)  # More randomness
```

---

## GPU Strategy

GPU acceleration in ElectoralSim currently targets the two largest performance bottlenecks:

1. **Utility computation** (`compute_utilities_gpu`) — the `(n_voters, n_parties)` distance matrix dominates runtime for large populations
2. **MNL sampling** (`mnl_sample_gpu`) — multinomial sampling from probability distributions row-by-row

Other operations (FPTP seat counting, PR allocation) use the CPU/Numba path.

**See also:** The CPU JIT path in `electoral_sim.engine.numba_accel` provides comparable function signatures via `compute_utilities_numba` and `mnl_sample_numba`.
