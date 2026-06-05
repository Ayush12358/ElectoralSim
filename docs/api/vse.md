# Voter Satisfaction Efficiency (VSE)

Voting System Efficiency analysis: measures how well an electoral outcome maximizes social welfare.

VSE is defined as:
```
VSE = (W_actual - W_random) / (W_optimal - W_random)
```

Where:
- **W_actual:** Social welfare of the actual election winner(s)
- **W_optimal:** Social welfare of the best possible winner(s)
- **W_random:** Average social welfare of a random winner

Reference: Jameson Quinn, "Voting System Efficiency"

---

## calculate_vse

Calculate Voting System Efficiency from a utility matrix and seat shares.

```python
from electoral_sim.analysis.vse import calculate_vse

vse = calculate_vse(
    utilities=utilities,
    seat_shares=seat_shares,
    random_iterations=0,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `utilities` | `np.ndarray` | `(n_voters, n_parties)` matrix of voter utilities |
| `seat_shares` | `np.ndarray` | `(n_parties,)` array of seat shares (0-1) |
| `random_iterations` | int | Unused; `w_random` is analytical (mean of all options) |

**Returns:** VSE score (typically 0.0 to 1.0). Returns 0.0 if all options have equal total utility (division by zero guard).

**Algorithm:**
1. **W_optimal** — maximum total utility across all parties (single-winner assumption)
2. **W_random** — mean total utility across all parties
3. **W_actual** — weighted average of total utility using seat shares

**Example:**
```python
import numpy as np
from electoral_sim import ElectionModel
from electoral_sim.analysis.vse import calculate_vse

model = ElectionModel(n_voters=10_000)
results = model.run_election()

# Get utility matrix and seat shares from the model
utilities = np.random.normal(50, 15, (10_000, 5))  # Example utilities
seat_shares = results["seats"] / results["seats"].sum()

vse = calculate_vse(utilities, seat_shares)
print(f"VSE: {vse:.3f}")
```

---

## calculate_welfare

Calculate Social Welfare (sum of utilities) for a given outcome.

```python
from electoral_sim.analysis.vse import calculate_welfare

welfare = calculate_welfare(utilities=np.array([0.8, 0.6, 0.3, 0.1]))
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `utilities` | `np.ndarray` | `(n_voters,)` utilities for the chosen outcome |
| `weights` | `np.ndarray \| None` | Optional `(n_voters,)` voter weights |

**Returns:** Total welfare (weighted sum if weights provided).

**Example:**
```python
# Weighted welfare (e.g., by constituency size)
weights = np.array([1.0, 1.0, 2.0, 1.0])
welfare = calculate_welfare(utilities, weights=weights)
print(f"Weighted welfare: {welfare:.2f}")
```
