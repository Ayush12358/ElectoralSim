# Vote Counting

Vote counting functions for FPTP and PR electoral systems. Both delegates to Numba-accelerated backends for performance.

---

## count_fptp

First Past The Post: winner takes all in each constituency. Uses Numba parallel acceleration when available.

```python
from electoral_sim.core.counting import count_fptp

result = count_fptp(
    constituencies=constituency_array,
    votes=vote_array,
    n_constituencies=10,
    n_parties=5,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `constituencies` | `np.ndarray` | `(n_voters,)` constituency assignments per voter |
| `votes` | `np.ndarray` | `(n_voters,)` vote choices (party indices) |
| `n_constituencies` | int | Total number of constituencies |
| `n_parties` | int | Number of parties |

**Returns:** Dict with keys:
| Key | Type | Description |
|-----|------|-------------|
| `system` | str | Always `"FPTP"` |
| `seats` | `np.ndarray` | `(n_parties,)` seat counts per party |
| `vote_counts` | `np.ndarray` | `(n_parties,)` raw vote counts per party |
| `n_constituencies` | int | Number of constituencies |

**Under the hood:** Calls `fptp_count_fast()` from `electoral_sim.engine.numba_accel`, which uses Numba parallel JIT when available, falling back to vectorized NumPy.

**Example:**
```python
import numpy as np
from electoral_sim.core.counting import count_fptp

# 1000 voters across 10 constituencies, 5 parties
constituencies = np.random.randint(0, 10, 1000)
votes = np.random.randint(0, 5, 1000)

result = count_fptp(constituencies, votes, 10, 5)
print(f"Winning party: {np.argmax(result['seats'])}")
print(f"Seats: {result['seats']}")
print(f"Votes: {result['vote_counts']}")
```

---

## count_pr

Proportional Representation with seat allocation. Counts votes vectorized and delegates seat allocation to the systems module.

```python
from electoral_sim.core.counting import count_pr

result = count_pr(
    votes=vote_array,
    n_parties=5,
    n_seats=100,
    allocation_method="dhondt",
    threshold=0.05,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `votes` | `np.ndarray` | *required* | `(n_voters,)` vote choices (party indices) |
| `n_parties` | int | *required* | Number of parties |
| `n_seats` | int | *required* | Total seats to allocate |
| `allocation_method` | `Literal["dhondt", "sainte_lague", "hare", "droop"]` | `"dhondt"` | Allocation algorithm |
| `threshold` | float | `0.0` | Minimum vote share for representation (0-1) |

**Returns:** Dict with keys:
| Key | Type | Description |
|-----|------|-------------|
| `system` | str | Always `"PR"` |
| `method` | str | Allocation method used |
| `seats` | `np.ndarray` | `(n_parties,)` allocated seats |
| `vote_counts` | `np.ndarray` | `(n_parties,)` raw vote counts |
| `n_seats` | int | Total seats |

**Under the hood:**
1. Vote counting via `np.bincount` (vectorized)
2. Seat allocation via `allocate_seats()` from `electoral_sim.systems.allocation`

**Example:**
```python
import numpy as np
from electoral_sim.core.counting import count_pr

votes = np.random.randint(0, 5, 10_000)

# D'Hondt with 5% threshold
result_dhondt = count_pr(votes, n_parties=5, n_seats=120, allocation_method="dhondt", threshold=0.05)

# Sainte-Laguë (more proportional for small parties)
result_sl = count_pr(votes, n_parties=5, n_seats=120, allocation_method="sainte_lague")

print("D'Hondt seats:", result_dhondt["seats"])
print("Sainte-Laguë seats:", result_sl["seats"])
```

> **Note:** With a threshold > 0, the allocation function internally zeroes-out parties below the threshold _before_ running the allocation algorithm.
