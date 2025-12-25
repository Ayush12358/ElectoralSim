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
mwcs = minimum_winning_coalitions(seats)

print(f"Found {len(mwcs)} MWCs:")
for coalition in mwcs:
    print(f"  {coalition}")
```

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
```

---

### cox_proportional_hazard

Cox proportional hazards model for government survival.

```python
from electoral_sim import cox_proportional_hazard

hazard = cox_proportional_hazard(
    time=12,  # months
    covariates={
        "majority_margin": 0.1,  # 10% above majority
        "coalition_strain": 0.3,
        "economic_growth": 0.02,
    }
)
```

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
