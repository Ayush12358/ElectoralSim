# ElectoralSim Usage Guide

## Installation

```bash
# From source
pip install -e .

# Or with dev dependencies
pip install -e ".[dev,viz]"
```

## Quick Start

```python
from electoral_sim import ElectionModel

# Create a model with 100K voters
model = ElectionModel(n_voters=100_000)

# Run an election
results = model.run_election()

# View results
print(f"Turnout: {results['turnout']:.1%}")
print(f"Gallagher Index: {results['gallagher']:.2f}")
print(f"ENP (votes): {results['enp_votes']:.2f}")
```

---

## Using Presets

Country presets come with realistic party configurations:

```python
from electoral_sim import ElectionModel

# India (543 Lok Sabha constituencies)
model = ElectionModel.from_preset("india")

# USA (435 House districts)  
model = ElectionModel.from_preset("usa")

# UK (650 House of Commons seats)
model = ElectionModel.from_preset("uk")

# Germany (MMP system with 5% threshold)
model = ElectionModel.from_preset("germany")
```

Override preset parameters:

```python
model = ElectionModel.from_preset(
    "india",
    n_voters=500_000,  # Override voter count
    seed=42,           # Set random seed
)
```

---

## Using Config

For full control, use the Config class:

```python
from electoral_sim import Config, ElectionModel, PartyConfig

# Define parties
parties = [
    PartyConfig("Left", position_x=-0.5, position_y=-0.2, valence=50),
    PartyConfig("Center", position_x=0.0, position_y=0.0, valence=55),
    PartyConfig("Right", position_x=0.5, position_y=0.3, valence=50),
]

# Create config
config = Config(
    n_voters=100_000,
    n_constituencies=10,
    parties=parties,
    electoral_system="PR",
    allocation_method="sainte_lague",
    threshold=0.05,  # 5% threshold
    temperature=0.5,
    seed=42,
)

# Create model from config
model = ElectionModel.from_config(config)
results = model.run_election()
```

---

## Chainable API

Build models fluently:

```python
from electoral_sim import ElectionModel

results = (
    ElectionModel(n_voters=100_000)
    .with_system("PR")
    .with_allocation("dhondt")
    .with_threshold(0.05)
    .with_temperature(0.3)  # More deterministic voting
    .run_election()
)
```

---

## Electoral Systems

### FPTP (First Past The Post)

```python
model = ElectionModel(
    n_voters=100_000,
    n_constituencies=10,
    electoral_system="FPTP",
)
```

### Proportional Representation

```python
from electoral_sim import ElectionModel

# D'Hondt (favors larger parties)
model = ElectionModel(
    electoral_system="PR",
    allocation_method="dhondt",
)

# Sainte-Laguë (more proportional)
model = ElectionModel(
    electoral_system="PR",
    allocation_method="sainte_lague",
)

# With electoral threshold
model = ElectionModel(
    electoral_system="PR",
    threshold=0.05,  # 5% threshold
)
```

---

## Metrics

```python
from electoral_sim import (
    gallagher_index,
    effective_number_of_parties,
    efficiency_gap,
)
import numpy as np

vote_shares = np.array([0.40, 0.35, 0.15, 0.10])
seat_shares = np.array([0.55, 0.35, 0.08, 0.02])

# Gallagher Index (disproportionality)
gallagher = gallagher_index(vote_shares, seat_shares)
print(f"Gallagher Index: {gallagher:.2f}")  # Lower = more proportional

# Effective Number of Parties
enp = effective_number_of_parties(vote_shares)
print(f"ENP: {enp:.2f}")  # Higher = more fragmented
```

---

## Coalition Formation

```python
from electoral_sim import (
    minimum_winning_coalitions,
    minimum_connected_winning,
    coalition_strain,
    form_government,
)
import numpy as np

# After an election with no majority
seats = np.array([45, 35, 15, 5])
positions = np.array([0.6, -0.2, 0.1, -0.5])
names = ["Right", "Center-Left", "Center", "Left"]

# Find minimum winning coalitions
mwcs = minimum_winning_coalitions(seats)
print(f"MWCs found: {len(mwcs)}")

# Form government (picks most stable coalition)
gov = form_government(seats, positions, names)
print(f"Government: {gov['coalition_names']}")
print(f"Stability: {gov['stability']:.2f}")
```

---

## Government Stability

```python
from electoral_sim import (
    collapse_probability,
    simulate_government_survival,
    GovernmentSimulator,
)

# Calculate collapse probability
prob = collapse_probability(
    time_in_office=30,  # months
    strain=0.3,
    stability=0.7,
    model="sigmoid",
)
print(f"Collapse probability at month 30: {prob:.1%}")

# Simulate survival
survival = simulate_government_survival(
    strain=0.3,
    stability=0.7,
    n_simulations=1000,
)
print(f"Mean survival: {survival['mean_survival']:.1f} months")
print(f"Full term probability: {survival['full_term_prob']:.1%}")

# Interactive simulation
sim = GovernmentSimulator(strain=0.3, stability=0.7, seed=42)
sim.add_event("scandal", severity=0.5)
months = sim.simulate(max_months=60)
print(f"Government lasted {months} months")
```

---

## Accessing Agent Data

```python
model = ElectionModel(n_voters=10_000, seed=42)

# Voter demographics (Polars DataFrame)
voters_df = model.voters.df
print(voters_df.columns)
# ['constituency', 'age', 'gender', 'education', 'income', 
#  'religion', 'party_id_7pt', 'ideology_x', 'ideology_y', 
#  'turnout_prob', 'unique_id']

# Party data
parties_df = model.parties.df
print(parties_df)

# Filter voters
young_voters = voters_df.filter(voters_df["age"] < 30)
print(f"Voters under 30: {len(young_voters)}")
```

---

## Running Multiple Elections

```python
model = ElectionModel.from_preset("india", n_voters=100_000, seed=42)

# Run 10 elections
for i in range(10):
    results = model.run_election()
    print(f"Election {i+1}: Gallagher={results['gallagher']:.2f}")

# Get all results
all_results = model.get_results()
```

---

## Reproducibility

Use the `seed` parameter for reproducible results:

```python
model1 = ElectionModel(n_voters=10_000, seed=42)
model2 = ElectionModel(n_voters=10_000, seed=42)

r1 = model1.run_election()
r2 = model2.run_election()

assert r1['turnout'] == r2['turnout']
```
