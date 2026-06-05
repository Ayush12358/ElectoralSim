# Metrics

Functions for measuring electoral outcomes and system performance.

## Gallagher Index

Measures disproportionality between votes and seats.

```python
from electoral_sim import gallagher_index
import numpy as np

vote_shares = np.array([0.40, 0.35, 0.15, 0.10])
seat_shares = np.array([0.55, 0.35, 0.08, 0.02])

gal = gallagher_index(vote_shares, seat_shares)
print(f"Gallagher Index: {gal:.2f}")
```

**Formula:** 
```
G = sqrt(0.5 × Σ(vote_share_i - seat_share_i)²)
```

**Interpretation:**
- 0-2: Very proportional (e.g., Netherlands, Germany)
- 2-5: Fairly proportional
- 5-10: Moderately disproportional
- 10+: Highly disproportional (e.g., UK, USA)

---

## Effective Number of Parties (ENP)

Laakso-Taagepera index measuring party system fragmentation.

```python
from electoral_sim import effective_number_of_parties
import numpy as np

# By vote shares
vote_shares = np.array([0.35, 0.30, 0.20, 0.15])
enp_v = effective_number_of_parties(vote_shares)

# By seat shares
seat_shares = np.array([0.45, 0.35, 0.15, 0.05])
enp_s = effective_number_of_parties(seat_shares)

print(f"ENP (votes): {enp_v:.2f}")  # ~3.3
print(f"ENP (seats): {enp_s:.2f}")  # ~2.8
```

**Formula:**
```
ENP = 1 / Σ(share_i²)
```

**Interpretation:**
- 1.0: Single dominant party
- 2.0: Two-party system
- 3-4: Moderate multiparty
- 5+: Highly fragmented

---

## Efficiency Gap

Measures partisan gerrymandering by comparing "wasted votes."

```python
from electoral_sim import efficiency_gap
import numpy as np

# Votes for party A and party B in each district
party_a_votes = np.array([60, 55, 40, 45, 50])
party_b_votes = np.array([40, 45, 60, 55, 50])
# Binary array: 1 if party A won the district
party_a_seats = np.array([1, 1, 0, 0, 1])

gap = efficiency_gap(party_a_votes, party_b_votes, party_a_seats)
print(f"Efficiency Gap: {gap:.3f}")
```

**Parameters:**
- `party_a_votes`: Votes for party A in each district
- `party_b_votes`: Votes for party B in each district  
- `party_a_seats`: Binary array (1=A won, 0=B won) per district

**Interpretation:**
- Positive: Party A is disadvantaged (has more wasted votes)
- Negative: Party A is advantaged
- |Gap| > 7%: Suggests significant gerrymandering

---

---

## Basic Metrics

### turnout_rate

Calculate turnout as fraction of eligible voters who voted.

```python
from electoral_sim import turnout_rate

rate = turnout_rate(votes_cast=75_000, eligible_voters=100_000)
print(f"Turnout: {rate:.1%}")  # 75.0%
```

**Parameters:**
- `votes_cast` — Total votes cast
- `eligible_voters` — Total eligible voters

**Returns:** Turnout rate (0-1)

---

### vote_share

Calculate a single party's vote share.

```python
from electoral_sim import vote_share

share = vote_share(party_votes=40_000, total_votes=100_000)
print(f"Vote share: {share:.1%}")  # 40.0%
```

**Parameters:**
- `party_votes` — Votes for the party
- `total_votes` — Total votes cast

**Returns:** Vote share (0-1)

---

### seat_share

Calculate a single party's seat share.

```python
from electoral_sim import seat_share

share = seat_share(party_seats=125, total_seats=250)
print(f"Seat share: {share:.1%}")  # 50.0%
```

**Parameters:**
- `party_seats` — Seats won by party
- `total_seats` — Total seats

**Returns:** Seat share (0-1)

---

### seats_votes_ratio

Calculate seats-to-votes ratio (advantage ratio). > 1 = overrepresented, < 1 = underrepresented.

```python
from electoral_sim import seats_votes_ratio

ratio = seats_votes_ratio(seat_share=0.50, vote_share=0.35)
print(f"Advantage ratio: {ratio:.2f}")  # 1.43
```

**Parameters:**
- `seat_share` — Party's seat share (0-1)
- `vote_share` — Party's vote share (0-1)

**Returns:** Ratio (seat_share / vote_share)

---

### responsiveness

How much seat share changes for a 1% vote share change. Measures seats-votes curve slope.

```python
from electoral_sim import responsiveness
import numpy as np

# District-level data
party_vote_shares = np.array([0.52, 0.48, 0.55, 0.45, 0.50])
party_seat_shares = np.array([1.0, 0.0, 1.0, 0.0, 1.0])  # binary wins

r = responsiveness(party_vote_shares, party_seat_shares)
print(f"Responsiveness: {r:.2f}")
```

**Parameters:**
- `party_vote_shares` — Party vote shares across districts
- `party_seat_shares` — Party seat shares across districts

**Returns:** Responsiveness (seats-votes slope, >1 = amplified swings)

---

### swing_ratio

Seat swing per unit vote swing between two parties.

```python
from electoral_sim import swing_ratio

sr = swing_ratio(
    party_votes_a=np.array([60, 55, 40]),
    party_votes_b=np.array([40, 45, 60]),
    party_seats_a=np.array([1, 1, 0]),
)
print(f"Swing ratio: {sr:.2f}")
```

**Parameters:**
- `party_votes_a` — Party A district vote totals
- `party_votes_b` — Party B district vote totals
- `party_seats_a` — Binary (1=A won, 0=B won) per district

**Returns:** Swing ratio. Typical range: 1.5 (PR) to 5+ (majoritarian)

---

## Concentration & Disproportionality

### Loosemore-Hanby Index

Alternative disproportionality measure — sum of absolute differences between vote and seat shares.

```python
from electoral_sim import loosemore_hanby_index
import numpy as np

vote_shares = np.array([0.40, 0.35, 0.15, 0.10])
seat_shares = np.array([0.55, 0.35, 0.08, 0.02])

lh = loosemore_hanby_index(vote_shares, seat_shares)
print(f"Loosemore-Hanby: {lh:.3f}")
```

**Formula:** `D = 0.5 * Σ|vote_share_i - seat_share_i|`

**Interpretation:**
- 0-5: Proportional
- 5-10: Moderate disproportionality
- 10+: Highly disproportional

---

### Herfindahl-Hirschman Index (HHI)

Concentration index — sum of squared shares. Inverse of ENP.

```python
from electoral_sim import herfindahl_hirschman_index

shares = np.array([0.35, 0.30, 0.20, 0.15])
hhi = herfindahl_hirschman_index(shares)
print(f"HHI: {hhi:.4f}")  # ~0.275
print(f"Equivalent ENP: {1/hhi:.1f}")  # ~3.6
```

**Formula:** `HHI = Σ(share_i²)`

**Interpretation:**
- 1.0: Monopoly (single party)
- 0.5: Duopoly (~2-party system)
- 0.25: Competitive (~4-party system)

---

## Gerrymandering Metrics

### partisan_bias

Measures how much one party is systematically advantaged in translating votes to seats.

```python
from electoral_sim import partisan_bias

# District-level data
party_a_votes = np.array([55, 60, 45, 40, 52])
party_b_votes = np.array([45, 40, 55, 60, 48])

bias = partisan_bias(party_a_votes, party_b_votes)
print(f"Partisan bias: {bias:.3f}")
```

**Parameters:**
- `party_a_votes` — Party A votes per district
- `party_b_votes` — Party B votes per district

**Returns:** Partisan bias value (positive = Party A advantaged)

---

### mean_median_gap

Difference between mean and median district vote share. Reveals gerrymandering via distribution skew.

```python
from electoral_sim import mean_median_gap

district_shares = np.array([0.52, 0.48, 0.60, 0.40, 0.51])
gap = mean_median_gap(district_shares)
print(f"Mean-median gap: {gap:.3f}")
```

**Parameters:**
- `district_shares` — Party vote shares across districts

**Returns:** Mean minus median gap (positive bias = advantage)

---

### partisan_gini

Inequality measure applied to seat distribution relative to votes. Captures electoral system disproportionality at the district level.

```python
from electoral_sim import partisan_gini

vote_shares = np.array([0.52, 0.48, 0.55, 0.45, 0.50])
seat_shares = np.array([1.0, 0.0, 1.0, 0.0, 1.0])

gini = partisan_gini(vote_shares, seat_shares)
print(f"Partisan Gini: {gini:.3f}")
```

**Parameters:**
- `vote_shares` — Party vote shares across districts
- `seat_shares` — Party seat shares across districts

**Returns:** Gini coefficient (0 = perfect equality, 1 = maximum inequality)

---

## District Geometry

### polsby_popper

Compactness measure: ratio of area to square of perimeter. 1.0 = perfect circle.

```python
from electoral_sim import polsby_popper

score = polsby_popper(area=100.0, perimeter=40.0)
print(f"Polsby-Popper: {score:.3f}")
```

**Formula:** `PP = (4π × area) / perimeter²`

**Interpretation:** 1.0 = perfect circle, lower values = more convoluted (potentially gerrymandered)

---

### convex_hull_compactness

Ratio of polygon area to its convex hull area.

```python
from electoral_sim import convex_hull_compactness

score = convex_hull_compactness(area=85.0, convex_hull_area=100.0)
print(f"Convex hull compactness: {score:.3f}")
```

**Formula:** `CHC = area / convex_hull_area`

**Interpretation:** 1.0 = perfectly convex, lower values = indented/irregular boundaries

---

## Voter Satisfaction Efficiency (VSE)

Measures how well election results match aggregate voter preferences.

```python
# VSE is automatically calculated in ElectionModel results
results = model.run_election()
print(f"VSE: {results['vse']:.3f}")
```

**Formula:** Compares actual outcome utility to optimal and random baselines.

**Interpretation:**
- 1.0: Optimal outcome (matches theoretical best)
- 0.0: Random outcome
- Negative: Worse than random

> **Note:** The standalone `calculate_vse()` function lives in `electoral_sim.analysis.vse`, not the `metrics` module. It accepts a `(n_voters, n_parties)` utility matrix and a `(n_parties,)` seat share array.
