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

### Closed-List PR

Parties receive seats proportional to votes; candidates elected in party-defined list order.

```python
from electoral_sim import closed_list_allocation

votes = np.array([4000, 3000, 2000, 1000])
candidate_list = [
    ["Alice", "Bob", "Carol"],
    ["Dave", "Eve"],
    ["Frank", "Grace"],
    ["Helen"],
]

result = closed_list_allocation(votes, n_seats=10, candidate_list=candidate_list, threshold=0.05)
print(f"Seats per party: {result['seats']}")
print(f"Elected: {result['elected']}")
```

**Parameters:**
- `votes` — Vote counts per party
- `n_seats` — Total seats to allocate
- `candidate_list` — Per-party ordered list of candidate names
- `threshold` — Minimum vote share to qualify (0-1)

**Returns:** Dict with `seats` (per-party array) and `elected` (list of candidate names)

---

### Open-List PR

Parties receive seats proportional to votes; candidates elected by preference vote order within each party.

```python
from electoral_sim import open_list_allocation

votes = np.array([4000, 3000, 2000, 1000])
candidate_list = [["Alice", "Bob"], ["Dave", "Eve"], ["Frank", "Grace"], ["Helen"]]
preference_votes = [
    np.array([2500, 1500]),  # Alice 2500, Bob 1500
    np.array([1800, 1200]),
    np.array([1200, 800]),
    np.array([1000]),
]

result = open_list_allocation(votes, n_seats=10, candidate_list=candidate_list,
                              preference_votes=preference_votes, threshold=0.05)
```

**Parameters:**
- `votes` — Vote counts per party
- `n_seats` — Total seats
- `candidate_list` — Per-party candidate names
- `preference_votes` — Per-party array of preference votes per candidate
- `threshold` — Minimum vote share

**Returns:** Dict with `seats` (per-party) and `elected` (candidate names)

---

### FPTP Allocation (Standalone)

First Past The Post: winner takes all in each constituency.

```python
from electoral_sim import fptp_allocation
import polars as pl

# votes_by_constituency must have columns: constituency, party, votes
votes_df = pl.DataFrame({
    "constituency": [0, 0, 0, 1, 1, 1],
    "party": [0, 1, 2, 0, 1, 2],
    "votes": [5200, 4800, 1000, 3000, 6000, 1000],
})

seats = fptp_allocation(votes_df, n_constituencies=2)
# Winner in constituency 0: party 0, in constituency 1: party 1
# Result: [1, 1, 0]
```

**Parameters:**
- `votes_by_constituency` — Polars DataFrame with columns `[constituency, party, votes]`
- `n_constituencies` — Total number of constituencies

**Returns:** Array of total seats per party

---

### MMP Allocation (Germany-Style)

Mixed-Member Proportional with overhang and leveling seats.

```python
from electoral_sim import mmp_allocation

district_votes = np.array([200, 180, 120])   # FPTP tier votes
list_votes = np.array([220, 170, 110])       # PR list votes

result = mmp_allocation(
    district_votes, list_votes,
    n_district_seats=150, n_total_seats=300,
    threshold=0.05
)
print(f"District seats: {result['district_seats']}")
print(f"List seats: {result['list_seats']}")
print(f"Overhang: {result['overhang']}")
print(f"Total: {result['total_seats']}")
```

**Parameters:**
- `district_votes` — Per-party vote totals for FPTP tier
- `list_votes` — Per-party vote totals for PR tier
- `n_district_seats` — Number of FPTP district seats
- `n_total_seats` — Target total seats in parliament
- `threshold` — Minimum vote share for list seat qualification (default 0.0)

**Returns:** Dict with `district_seats`, `list_seats`, `overhang`, `total_seats`

---

### Parallel Mixed Allocation (Japan-Style)

FPTP district seats + PR list seats allocated independently, without compensatory leveling.

```python
from electoral_sim import parallel_mixed_allocation

district_votes = np.array([200, 180, 120])
pr_votes = np.array([220, 170, 110])

result = parallel_mixed_allocation(
    district_votes, pr_votes,
    n_district_seats=150, n_pr_seats=150,
    threshold=0.05
)
print(f"District: {result['district_seats']}")
print(f"PR: {result['pr_seats']}")
print(f"Total: {result['total_seats']}")
```

**Parameters:**
- `district_votes` — Per-party vote totals for FPTP tier
- `pr_votes` — Per-party vote totals for PR list tier
- `n_district_seats` — Total FPTP district seats
- `n_pr_seats` — Total PR list seats
- `threshold` — Minimum vote share for PR tier

**Returns:** Dict with `district_seats`, `pr_seats`, `total_seats`

---

### ALLOCATION_METHODS Registry

Dictionary mapping method names to allocator functions. Used by `allocate_seats()` for dispatch.

```python
from electoral_sim.systems.allocation import ALLOCATION_METHODS

print(ALLOCATION_METHODS)
# {'dhondt': <function dhondt_allocation>, 'sainte_lague': <function sainte_lague_allocation>,
#  'hare': <function hare_quota_allocation>, 'droop': <function droop_quota_allocation>}
```

---

### Numba Acceleration

`allocate_seats()` automatically uses Numba JIT-accelerated versions (`dhondt_fast`, `sainte_lague_fast` from `electoral_sim.engine.numba_accel`) for D'Hondt and Sainte-Laguë when Numba is available. Falls back gracefully to pure Python implementations if Numba is not installed.

---

## Primary Elections & Candidate Selection

### closed_primary

Closed primary: only voters registered with the party can vote.

```python
from electoral_sim import closed_primary

voter_utilities = np.random.randn(1000, 5)    # (n_voters, n_candidates)
party_affiliation = np.random.randint(0, 3, 1000)  # (n_voters,)

result = closed_primary(voter_utilities, party_affiliation, party_id=0)
print(f"Winner: Candidate {result['winner']}")
print(f"Vote counts: {result['vote_counts']}")
```

**Parameters:**
- `voter_utilities` — (n_voters, n_candidates) utility matrix
- `party_affiliation` — (n_voters,) party ID for each voter
- `party_id` — Party conducting the primary

**Returns:** Dict with `winner` (candidate index) and `vote_counts`

---

### open_primary

Open primary: any voter can participate regardless of party registration.

```python
from electoral_sim import open_primary

voter_utilities = np.random.randn(1000, 5)

result = open_primary(voter_utilities)
print(f"Winner: Candidate {result['winner']}")
```

**Parameters:**
- `voter_utilities` — (n_voters, n_candidates) utility matrix

**Returns:** Dict with `winner` (candidate with highest total utility) and `vote_counts`

---

### candidate_selection

Generate candidate valence scores for each party's primary field.

```python
from electoral_sim import candidate_selection

valence_matrix = candidate_selection(
    n_parties=4,
    n_candidates_per_party=3,
    base_valence=50.0,
    rng=np.random.default_rng(42)
)
# Returns (n_parties, n_candidates_per_party) valence matrix
```

**Parameters:**
- `n_parties` — Number of parties
- `n_candidates_per_party` — Candidates per party primary (default 3)
- `base_valence` — Mean candidate valence (default 50.0)
- `rng` — Optional random generator

**Returns:** (n_parties, n_candidates_per_party) valence matrix, clipped to [0, 100]

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

### MMP (Mixed-Member Proportional)

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="PR",
    allocation_method="mmp",
    threshold=0.05
)
```

### Parallel Mixed

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="PR",
    allocation_method="parallel"
)
```

### IRV (Instant Runoff Voting)

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="IRV"
)
```

### STV (Single Transferable Vote)

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="STV",
    n_seats=3
)
```

### Borda Count

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="Borda"
)
```

### Score Voting

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="Score"
)
```

### PAV (Proportional Approval Voting)

```python
model = ElectionModel(
    n_voters=10_000,
    electoral_system="PAV",
    committee_size=5
)
```
