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

# Votes for party A in each district
party_a_votes = np.array([6000, 5500, 4000, 3000, 2500])
# Total votes in each district
total_votes = np.array([10000, 10000, 10000, 10000, 10000])

gap = efficiency_gap(party_a_votes, total_votes)
print(f"Efficiency Gap: {gap:.1%}")
```

**Interpretation:**
- Positive: Party A is disadvantaged (has more wasted votes)
- Negative: Party A is advantaged
- |Gap| > 7%: Suggests significant gerrymandering

---

## Additional Metrics

### Loosemore-Hanby Index

Alternative disproportionality measure (sum of absolute differences).

```python
def loosemore_hanby(vote_shares, seat_shares):
    return 0.5 * np.abs(vote_shares - seat_shares).sum()
```

### Herfindahl-Hirschman Index (HHI)

Concentration index (inverse of ENP).

```python
def hhi(shares):
    return np.sum(shares ** 2)
```

### Voter Satisfaction Efficiency (VSE)

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
