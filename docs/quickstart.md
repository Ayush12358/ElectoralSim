# Quick Start Guide

This guide walks you through your first election simulation with ElectoralSim.

## Your First Election

```python
from electoral_sim import ElectionModel

# Create a model with 10,000 voters across 5 constituencies
model = ElectionModel(
    n_voters=10_000,
    n_constituencies=5,
    seed=42  # For reproducibility
)

# Run an election
results = model.run_election()

# View results
print(f"Turnout: {results['turnout']:.1%}")
print(f"Gallagher Index: {results['gallagher']:.2f}")
print(f"Effective Parties (votes): {results['enp_votes']:.2f}")
print(f"Effective Parties (seats): {results['enp_seats']:.2f}")
```

**Output:**
```
Turnout: 75.4%
Gallagher Index: 12.35
Effective Parties (votes): 2.89
Effective Parties (seats): 2.45
```

## Understanding the Results

| Key | Description |
|-----|-------------|
| `turnout` | Fraction of voters who cast ballots |
| `gallagher` | Disproportionality index (0 = perfectly proportional) |
| `enp_votes` | Effective number of parties by vote share |
| `enp_seats` | Effective number of parties by seat share |
| `seats` | Array of seats won by each party |
| `vote_counts` | Array of votes received by each party |

## Using Country Presets

Presets provide realistic party configurations:

```python
# India - 543 Lok Sabha constituencies
model = ElectionModel.from_preset("india", n_voters=100_000)

# Germany - MMP with 5% threshold
model = ElectionModel.from_preset("germany", n_voters=50_000)

# USA - 435 House districts
model = ElectionModel.from_preset("usa", n_voters=50_000)
```

## Specialized India Simulation

For full India election simulation with state-wise breakdown:

```python
from electoral_sim import simulate_india_election

result = simulate_india_election(
    n_voters_per_constituency=1000,
    seed=42
)

# Access results
print(f"Total seats: {sum(result.seats.values())}")
print(f"BJP seats: {result.seats['BJP']}")
print(f"NDA alliance: {result.nda_seats} seats")
print(f"INDIA alliance: {result.india_seats} seats")
```

## Changing Electoral Systems

```python
# FPTP (default)
model = ElectionModel(n_voters=10_000, electoral_system="FPTP")

# Proportional Representation with D'Hondt
model = ElectionModel(
    n_voters=10_000,
    electoral_system="PR",
    allocation_method="dhondt"
)

# PR with 5% threshold
model = ElectionModel(
    n_voters=10_000,
    electoral_system="PR",
    allocation_method="sainte_lague",
    threshold=0.05
)
```

## Chainable API

Build models fluently:

```python
results = (
    ElectionModel(n_voters=50_000)
    .with_system("PR")
    .with_allocation("sainte_lague")
    .with_threshold(0.05)
    .with_temperature(0.3)
    .run_election()
)
```

## Multiple Elections

Run batch simulations for Monte Carlo analysis:

```python
model = ElectionModel(n_voters=10_000, seed=42)

# Run 100 elections
batch_results = model.run_elections_batch(n_elections=100)

# Get aggregate statistics
stats = model.get_aggregate_stats(batch_results)
print(f"Mean turnout: {stats['turnout_mean']:.1%} ± {stats['turnout_std']:.1%}")
print(f"Mean Gallagher: {stats['gallagher_mean']:.2f} ± {stats['gallagher_std']:.2f}")
```

## Next Steps

- [API Reference](api/README.md) — Full documentation of all classes and functions
- [Behavior Models](api/behavior_models.md) — Custom voter behavior
- [Country Presets](presets/README.md) — Available country configurations
- [Advanced Topics](advanced/README.md) — Voter psychology, performance tuning
