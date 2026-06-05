# Coalition & Government

Functions for coalition formation and government stability analysis.

## Coalition Formation

### form_government

Find the most stable coalition given election results.

```python
from electoral_sim import form_government
import numpy as np

seats = np.array([150, 120, 80, 50])
positions = np.array([0.6, -0.3, 0.1, -0.6])
names = ["Right", "Left", "Center", "Far-Left"]

gov = form_government(seats, positions, names)

print(f"Coalition: {gov['coalition_names']}")
print(f"Seats: {gov['seats']}")
print(f"Stability: {gov['stability']:.2f}")
print(f"Success: {gov['success']}")
```

**Returns:**
| Key | Description |
|-----|-------------|
| `success` | Whether a majority coalition was formed |
| `coalition` | List of party indices |
| `coalition_names` | List of party names |
| `seats` | Total coalition seats |
| `stability` | Predicted stability (0-1) |

---

### minimum_winning_coalitions

Find all coalitions with minimal seats for majority.

```python
from electoral_sim import minimum_winning_coalitions

seats = np.array([45, 35, 15, 5])
mwcs = minimum_winning_coalitions(seats, majority_threshold=0.5)

print(f"Found {len(mwcs)} MWCs:")
for coalition in mwcs:
    print(f"  {coalition}")
```

**Parameters:**
- `seats` — Array of seats per party
- `majority_threshold` — Fraction needed for majority (default 0.5)

---

### minimum_connected_winning

Find ideologically connected coalitions (no gaps in position space).

```python
from electoral_sim import minimum_connected_winning

seats = np.array([45, 35, 15, 5])
positions = np.array([0.6, -0.2, 0.1, -0.5])

mcws = minimum_connected_winning(seats, positions)
```

---

### coalition_strain

Calculate ideological tension within a coalition.

```python
from electoral_sim import coalition_strain

positions = np.array([0.6, -0.2, 0.1])  # Coalition members
seats = np.array([45, 35, 15])

strain = coalition_strain(positions, seats)
print(f"Strain: {strain:.2f}")  # Higher = more tension
```

---

### predict_coalition_stability

Predict coalition stability from strain, majority margin, and party count.

```python
from electoral_sim import predict_coalition_stability

stability = predict_coalition_stability(
    strain=0.3,
    majority_margin=0.15,  # 15% above bare majority
    n_parties=3,
    model="sigmoid"        # "sigmoid", "linear", or "exponential"
)
print(f"Predicted stability: {stability:.2f}")
```

**Parameters:**
- `strain` — Policy strain from `coalition_strain()`
- `majority_margin` — Seats above majority / total seats
- `n_parties` — Number of parties in coalition
- `model` — "sigmoid", "linear", or "exponential" (default "sigmoid")

**Returns:** Stability score 0-1 (higher = more stable)

---

### junior_partner_penalty

Calculate electoral penalty for junior coalition partners.

```python
from electoral_sim import junior_partner_penalty

seats = np.array([200, 50, 30])  # 3-party coalition
coalition = [0, 1, 2]

penalties = junior_partner_penalty(seats, coalition)
# Returns: [bonus, penalty, larger_penalty]
```

**Research basis:** Junior partners often lose votes in subsequent elections due to credit-claiming by the dominant partner.

---

### allocate_portfolios_laver_shepsle

Portfolio allocation using Laver-Shepsle model.

```python
from electoral_sim import allocate_portfolios_laver_shepsle

coalition = [0, 1, 2]
seats = np.array([200, 100, 50])
positions = np.array([
    [0.2, 0.3],  # Party 0
    [0.5, 0.5],  # Party 1
    [0.8, 0.7],  # Party 2
])

allocations = allocate_portfolios_laver_shepsle(
    coalition, seats, positions,
    dimensions=["Economy", "Social"]
)
# Returns: {"Economy": 1, "Social": 1}  # Party index for each portfolio
```

---

### form_coalition_with_utility

Form coalition via Policy vs Office tradeoff utility maximization.

```python
from electoral_sim import form_coalition_with_utility

seats = np.array([200, 100, 50])
positions = np.array([0.2, 0.5, 0.8])

coalition, utility = form_coalition_with_utility(
    seats, positions,
    office_weight=0.5,        # 0 = pure policy, 1 = pure office
    majority_threshold=0.5,   # Fraction for majority
)
print(f"Coalition: {coalition}, Utility: {utility:.2f}")
```

**Parameters:**
- `seats` — Array of seat counts
- `positions` — Party positions (1D array or 2D with primary dimension used)
- `office_weight` — α weight: 0.0 = pure policy, 1.0 = pure office-seeking (default 0.5)
- `majority_threshold` — Threshold for majority (default 0.5)

**Returns:** (coalition_indices, utility_score)

**Research basis:** Office-seeking parties maximize cabinet portfolios; policy-seeking parties minimize ideological dispersion. The α parameter blends these motivations.

---

### coalition_feedback

Vote-share adjustments for coalition parties in subsequent elections (junior partner penalty effect).

```python
from electoral_sim import coalition_feedback

party_votes = np.array([0.40, 0.30, 0.20, 0.10])  # vote shares
coalition = [0, 2]  # Party 0 (senior) + Party 2 (junior)

adjusted = coalition_feedback(
    coalition, party_votes,
    junior_penalty=0.05,  # 5pp penalty for junior partners
    senior_bonus=0.02,    # 2pp bonus for senior partner
)
```

**Parameters:**
- `coalition_parties` — List of party indices in coalition
- `party_votes` — Vote shares from previous election
- `junior_penalty` — Vote share penalty for junior partners (default 0.05)
- `senior_bonus` — Vote share bonus for senior partner (default 0.02)

**Returns:** Adjusted vote share array (renormalized to sum to 1)

---

### party_evolution

Simulate party system evolution: entry of new parties, exit of non-viable ones.

```python
from electoral_sim import party_evolution

votes = np.array([0.40, 0.30, 0.20, 0.08, 0.02])
positions = np.array([-0.5, -0.2, 0.1, 0.4, 0.7])

result = party_evolution(
    votes, positions,
    viability_threshold=0.03,   # Parties below 3% may exit
    ideology_closeness=0.2,     # New parties fill gaps
    rng=np.random.default_rng(42),
)
```

**Parameters:**
- `party_votes` — Current vote shares
- `party_positions` — Current party positions
- `viability_threshold` — Minimum vote share to survive (default 0.03)
- `ideology_closeness` — Gap threshold for new party entry (default 0.2)
- `rng` — Optional random generator

**Returns:** Dict with updated votes, positions, and entry/exit indicators

---

## Government Stability

### collapse_probability

Calculate probability of government collapse at time T.

```python
from electoral_sim import collapse_probability

prob = collapse_probability(
    time=30,  # months in office
    strain=0.3,
    stability=0.7,
    model="sigmoid"  # or "linear", "exponential"
)
```

**Models:**
- `sigmoid`: S-curve (slow start, rapid mid-term risk, plateau)
- `linear`: Constant hazard rate
- `exponential`: Rapidly increasing risk

---

### simulate_government_survival

Monte Carlo simulation of government duration.

```python
from electoral_sim import simulate_government_survival

survival = simulate_government_survival(
    strain=0.3,
    stability=0.7,
    n_simulations=1000,
    max_months=60,
    seed=42
)

print(f"Mean survival: {survival['mean_survival']:.1f} months")
print(f"Median survival: {survival['median_survival']:.1f} months")
print(f"Full term probability: {survival['full_term_prob']:.1%}")
print(f"Std dev: {survival['std_survival']:.1f} months")
print(f"Early collapse prob: {survival['early_collapse_prob']:.1%}")
print(f"Min/Max: {survival['min_survival']} / {survival['max_survival']} months")
```

**Returns:**

| Key | Description |
|-----|-------------|
| `mean_survival` | Mean months survived |
| `median_survival` | Median months survived |
| `std_survival` | Standard deviation of survival times |
| `full_term_prob` | Probability of surviving full term |
| `early_collapse_prob` | Probability of collapse before mid-term |
| `min_survival` | Minimum survival (months) |
| `max_survival` | Maximum survival (months) |

---

---

### hazard_rate

Calculate instantaneous hazard rate with bathtub curve (higher at start and end of term).

```python
from electoral_sim import hazard_rate

events = [
    {"type": "scandal", "severity": 0.7, "month": 18},
    {"type": "economic_crisis", "severity": 0.9, "month": 30},
]

rate = hazard_rate(
    time_in_office=24,  # months
    events=events,
    base_hazard=0.02,
)
print(f"Hazard rate at month 24: {rate:.4f}")
```

**Parameters:**
- `time_in_office` — Months in office
- `events` — List of events with `{"type": str, "severity": float}` (optional)
- `base_hazard` — Base hazard rate (default 0.02)

**Returns:** Hazard rate (probability per unit time)

**Event types:** scandal (weight 0.3), economic_crisis (0.4), defection (0.5), vote_of_no_confidence (0.8), leadership_challenge (0.3)

---

### cox_proportional_hazard

Cox proportional hazards model for government survival.

```python
from electoral_sim import cox_proportional_hazard

hazard = cox_proportional_hazard(
    time_in_office=12,  # months
    covariates={
        "majority_margin": 0.1,  # 10% above majority
        "coalition_strain": 0.3,
        "economic_growth": 0.02,
    },
    base_hazard=0.01,
    coefficients={
        "majority_margin": -0.5,    # Wider margin reduces hazard
        "coalition_strain": 0.8,    # Higher strain increases hazard
        "economic_growth": -0.3,    # Growth reduces hazard
    },
)
```

**Parameters:**
- `time_in_office` — Months elapsed
- `covariates` — Dict of covariate names → values
- `base_hazard` — Baseline hazard rate (default 0.01)
- `coefficients` — Dict of covariate names → coefficients (defaults based on Warwick 1994)

---

### GovernmentSimulator

Interactive government simulation with events.

```python
from electoral_sim import GovernmentSimulator

sim = GovernmentSimulator(strain=0.3, stability=0.7, seed=42)

# Add events
sim.add_event("scandal", severity=0.5, month=12)
sim.add_event("economic_shock", severity=0.3, month=24)

# Run simulation
months = sim.simulate(max_months=60)
print(f"Government lasted {months} months")
```

### GovernmentSimulator Methods

#### step

Advance one month. Returns True if government survives.

```python
survived = sim.step()
if not survived:
    print(f"Collapsed at month {sim.months_in_office}")
    print(f"Reason: {sim.collapse_reason}")
```

**Returns:** bool — True if survived, False if collapsed

#### summary

Get simulation summary as a dict.

```python
info = sim.summary()
print(f"Coalition: {info['coalition']}")
print(f"Duration: {info['months_in_office']} months")
print(f"Collapsed: {info['collapsed']}")
print(f"Reason: {info['collapse_reason']}")
print(f"Events: {info['n_events']}")
```

**Returns:**

| Key | Description |
|-----|-------------|
| `coalition` | Party names |
| `months_in_office` | Duration survived |
| `collapsed` | Whether government fell |
| `collapse_reason` | "policy_strain" or "time_in_office" if collapsed |
| `strain` | Coalition strain value |
| `stability` | Stability score |
| `n_events` | Number of destabilizing events recorded |
