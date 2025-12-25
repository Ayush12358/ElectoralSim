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

# Generate preference rankings for 1000 voters, 5 candidates
rankings = generate_rankings(n_voters=1000, n_candidates=5, seed=42)

winner, rounds = irv_election(rankings)
print(f"Winner: Candidate {winner}")
print(f"Rounds: {len(rounds)}")
```

**Returns:**
- `winner` — Index of winning candidate
- `rounds` — List of round results (votes per candidate each round)

---

### STV (Single Transferable Vote)

Multi-winner ranked choice. Used in: Ireland, Australia (Senate), Malta.

```python
from electoral_sim import stv_election, generate_rankings

rankings = generate_rankings(n_voters=1000, n_candidates=10, seed=42)

winners = stv_election(rankings, n_seats=3)
print(f"Winners: {winners}")  # e.g., [2, 5, 7]
```

**Parameters:**
- `rankings` — (n_voters, n_candidates) array of preferences
- `n_seats` — Number of seats to fill

---

### Approval Voting

Voters can approve multiple candidates.

```python
from electoral_sim import approval_voting
import numpy as np

# Approval matrix: 1 = approve, 0 = don't approve
approvals = np.array([
    [1, 1, 0, 0],  # Voter 1 approves A and B
    [0, 1, 1, 0],  # Voter 2 approves B and C
    [1, 0, 0, 1],  # Voter 3 approves A and D
])

winner = approval_voting(approvals)
print(f"Winner: Candidate {winner}")
```

---

### Condorcet Winner

Finds the candidate who beats all others in pairwise comparisons (if one exists).

```python
from electoral_sim import condorcet_winner, generate_rankings

rankings = generate_rankings(n_voters=1000, n_candidates=4, seed=42)

winner = condorcet_winner(rankings)
if winner is not None:
    print(f"Condorcet winner: Candidate {winner}")
else:
    print("No Condorcet winner (cycle exists)")
```

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
