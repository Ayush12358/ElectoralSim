# Electoral Systems

Seat allocation methods and alternative voting systems.

## Seat Allocation (PR)

### allocate_seats

Universal allocation function supporting all methods.

```python
from electoral_sim import allocate_seats

seats = allocate_seats(
    votes=np.array([4000, 3000, 2000, 1000]),
    n_seats=10,
    method="dhondt",  # or "sainte_lague", "hare", "droop"
    threshold=0.05
)
```

---

### D'Hondt

Favors larger parties. Used in: Spain, Portugal, Poland, Israel.

```python
from electoral_sim import dhondt_allocation

votes = np.array([4000, 3000, 2000, 1000])
seats = dhondt_allocation(votes, n_seats=10)
# Result: [4, 3, 2, 1]
```

**Formula:** Divide votes by 1, 2, 3, ... and allocate seats to highest quotients.

---

### Sainte-Laguë

More proportional than D'Hondt. Used in: Germany, New Zealand, Norway.

```python
from electoral_sim import sainte_lague_allocation

seats = sainte_lague_allocation(votes, n_seats=10)
```

**Formula:** Divide votes by 1, 3, 5, 7, ...

---

### Hare Quota (LR-Hare)

Largest remainder with Hare quota. Very proportional.

```python
from electoral_sim import hare_quota_allocation

seats = hare_quota_allocation(votes, n_seats=10)
```

**Quota:** `total_votes / n_seats`

---

### Droop Quota

Largest remainder with Droop quota. Used in: Ireland (STV).

```python
from electoral_sim import droop_quota_allocation

seats = droop_quota_allocation(votes, n_seats=10)
```

**Quota:** `(total_votes / (n_seats + 1)) + 1`

---

## Alternative Voting Systems

### IRV (Instant Runoff Voting)

Also known as Ranked Choice Voting. Used in: Australia (House), USA (some cities).

```python
from electoral_sim import irv_election, generate_rankings

# Generate preference rankings from utilities
utilities = np.random.randn(1000, 5)
rankings = generate_rankings(utilities)

result = irv_election(rankings, n_candidates=5)
print(f"Winner: Candidate {result['winner']}")
print(f"Rounds: {len(result['rounds'])}")
```

**Parameters:**
- `rankings` — (n_voters, n_candidates) array of rankings (1=first choice, 0=unranked)
- `n_candidates` — Number of candidates

**Returns:** Dict with `winner`, `rounds`, `elimination_order`, `final_votes`

---

### STV (Single Transferable Vote)

Multi-winner ranked choice. Used in: Ireland, Australia (Senate), Malta.

```python
from electoral_sim import stv_election, generate_rankings

utilities = np.random.randn(1000, 10)
rankings = generate_rankings(utilities)

result = stv_election(rankings, n_candidates=10, n_seats=3)
print(f"Elected: {result['elected']}")
print(f"Quota: {result['quota']}")
```

**Parameters:**
- `rankings` — (n_voters, n_candidates) array
- `n_candidates` — Number of candidates
- `n_seats` — Number of seats to fill

**Returns:** Dict with `elected`, `rounds`, `n_seats`, `quota`

---

### Approval Voting

Voters can approve multiple candidates.

```python
from electoral_sim import approval_voting
import numpy as np

approvals = np.array([
    [1, 1, 0, 0],  # Voter 1 approves A and B
    [0, 1, 1, 0],  # Voter 2 approves B and C
    [1, 0, 0, 1],  # Voter 3 approves A and D
])

result = approval_voting(approvals, n_candidates=4)
print(f"Winner: Candidate {result['winner']}")
print(f"Approval counts: {result['approval_counts']}")
```

**Parameters:**
- `approvals` — (n_voters, n_candidates) boolean array
- `n_candidates` — Number of candidates

**Returns:** Dict with `winner`, `approval_counts`, `approval_shares`

---

### Condorcet Winner

Finds the candidate who beats all others in pairwise comparisons (if one exists).

```python
from electoral_sim import condorcet_winner, generate_rankings

utilities = np.random.randn(1000, 4)
rankings = generate_rankings(utilities)

result = condorcet_winner(rankings, n_candidates=4)
if result['has_condorcet']:
    print(f"Condorcet winner: Candidate {result['condorcet_winner']}")
else:
    print("No Condorcet winner (cycle exists)")
```

**Parameters:**
- `rankings` — (n_voters, n_candidates) array
- `n_candidates` — Number of candidates

**Returns:** Dict with `has_condorcet`, `condorcet_winner`, `pairwise`

---

### Borda Count

Candidates receive points based on rank position (n-1 for 1st, n-2 for 2nd, etc.).

```python
from electoral_sim import borda_count, generate_rankings

utilities = np.random.randn(1000, 5)
rankings = generate_rankings(utilities)

result = borda_count(rankings, n_candidates=5)
print(f"Winner: Candidate {result['winner']}")
print(f"Scores: {result['scores']}")
```

**Returns:** Dict with `winner`, `scores`

---

### Score (Range) Voting

Voters assign scores (0 to max_score) based on utility scaling.

```python
from electoral_sim import score_voting

utilities = np.array([[1.0, 0.5, 0.0], [0.0, 1.0, 0.5], [0.5, 0.0, 1.0]])

result = score_voting(utilities, n_candidates=3, max_score=10)
print(f"Winner: Candidate {result['winner']}")
```

**Returns:** Dict with `winner`, `scores`

---

### PAV (Proportional Approval Voting)

Multi-winner approval-based committee voting with sequential selection.

```python
from electoral_sim import pav_committee

approvals = np.array([
    [1, 1, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 1],
])

result = pav_committee(approvals, n_candidates=4, committee_size=2)
print(f"Committee: {result['committee']}")
```

**Returns:** Dict with `committee`, `scores`

---

### generate_rankings

Converts utility matrix to ranked preference ballots.

```python
from electoral_sim import generate_rankings

utilities = np.random.randn(1000, 5)
rankings = generate_rankings(utilities, n_ranked=3)
# rankings shape: (1000, 5), 1=first choice, 2=second, 0=unranked
```

**Parameters:**
- `utilities` — (n_voters, n_candidates) utility matrix
- `n_ranked` — Optional, number of candidates to rank (default: all)

---

## Using Systems in ElectionModel

### FPTP

```python
model = ElectionModel(
    n_voters=10_000,
    n_constituencies=10,
    electoral_system="FPTP"
)
```

### PR with D'Hondt

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="PR",
    allocation_method="dhondt"
)
```

### PR with Threshold

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="PR",
    allocation_method="sainte_lague",
    threshold=0.05  # 5% threshold
)
```
