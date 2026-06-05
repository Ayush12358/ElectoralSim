# Primary Elections

Primary election and candidate selection systems. Supports closed and open primaries, plus valence-based candidate field generation.

## closed_primary

Closed primary: only voters registered with a given party may vote.

```python
from electoral_sim.systems.primary import closed_primary

result = closed_primary(
    voter_utilities=utilities,
    party_affiliation=affiliations,
    party_id=0,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `voter_utilities` | `np.ndarray` | `(n_voters, n_candidates)` utility matrix |
| `party_affiliation` | `np.ndarray` | `(n_voters,)` party ID for each voter |
| `party_id` | int | Party conducting the primary |

**Returns:** Dict with keys:
| Key | Type | Description |
|-----|------|-------------|
| `winner` | int | Candidate index with highest total utility among party voters (-1 if none) |
| `vote_counts` | `np.ndarray` | Total utility scores per candidate |

**Example:**
```python
import numpy as np

# 100 voters, 4 candidates in Party 0's primary
utilities = np.random.normal(50, 10, (100, 4))
party_affiliation = np.random.choice([0, 1], 100)

result = closed_primary(utilities, party_affiliation, party_id=0)
winner = result["winner"]
print(f"Winner: Candidate {winner}")
```

---

## open_primary

Open primary: any voter can participate regardless of party affiliation.

```python
from electoral_sim.systems.primary import open_primary

result = open_primary(voter_utilities=utilities)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `voter_utilities` | `np.ndarray` | `(n_voters, n_candidates)` utility matrix |

**Returns:** Dict with keys:
| Key | Type | Description |
|-----|------|-------------|
| `winner` | int | Candidate with highest total utility across all voters |
| `vote_counts` | `np.ndarray` | Total utility scores per candidate |

**Example:**
```python
utilities = np.random.normal(50, 10, (1000, 3))
result = open_primary(utilities)
print(f"Candidate {result['winner']} wins the open primary")
```

---

## candidate_selection

Generate candidate valence scores for each party's candidate field. The highest-valence candidate becomes the general election nominee.

```python
from electoral_sim.systems.primary import candidate_selection

valence_matrix = candidate_selection(
    n_parties=5,
    n_candidates_per_party=3,
    base_valence=50.0,
    rng=np.random.default_rng(42),
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n_parties` | int | *required* | Number of parties |
| `n_candidates_per_party` | int | `3` | Candidates per party primary |
| `base_valence` | float | `50.0` | Mean candidate valence (clipped 0-100) |
| `rng` | `np.random.Generator \| None` | `None` | Random generator |

**Returns:** `(n_parties, n_candidates_per_party)` valence matrix, clipped to [0, 100].

**Example:**
```python
import numpy as np

# Generate candidate fields for 5 parties
valence = candidate_selection(5, n_candidates_per_party=4)

# Each party's general-election nominee is its highest-valence candidate
nominees = valence.max(axis=1)
for i, v in enumerate(nominees):
    print(f"Party {i} nominee valence: {v:.1f}")
```
