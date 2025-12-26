# ElectoralSim Documentation

Welcome to the ElectoralSim documentation. This toolkit provides a comprehensive framework for simulating electoral systems, voter behavior, and political dynamics.

## Quick Links

- [Installation](installation.md)
- [Quick Start](quickstart.md)
- [CLI Usage](cli.md)
- [API Reference](api/README.md)
- [Batch Runner API](api/batch_runner.md)
- [Country Presets](presets/README.md)
- [Advanced Topics](advanced/README.md)

---

## What is ElectoralSim?

ElectoralSim is an agent-based modeling toolkit for electoral simulations, built on top of [Mesa](https://mesa.readthedocs.io/) with Polars DataFrames. It enables researchers and developers to:

- **Simulate elections** at scale (1M+ voters) with multiple electoral systems
- **Model voter behavior** using established political science theories
- **Analyze electoral outcomes** with standard metrics (Gallagher, ENP, VSE)
- **Run parameter sweeps** for sensitivity analysis with the batch runner
- **Study coalition dynamics** and government stability
- **Explore opinion dynamics** through social network models
- **Use CLI tools** for batch simulations and analysis

## Core Concepts

### ElectionModel
The central class that orchestrates simulations. It manages voter agents, party agents, electoral rules, and behavior models.

### BehaviorEngine
A pluggable system for combining multiple voter utility models (proximity, valence, retrospective, strategic voting).

### OpinionDynamics
Social network-based opinion evolution using models like Bounded Confidence and Noisy Voter.

### Country Presets
Pre-configured setups for 11 countries including India, USA, UK, Germany, and the EU Parliament.

---

## Getting Started

```python
from electoral_sim import ElectionModel

model = ElectionModel(n_voters=100_000, seed=42)
results = model.run_election()
print(f"Turnout: {results['turnout']:.1%}")
```

See the [Quick Start Guide](quickstart.md) for more examples.

---

## Table of Contents

### Guides
1. [Installation](installation.md)
2. [Quick Start](quickstart.md)

### API Reference
- [ElectionModel](api/election_model.md)
- [Behavior Models](api/behavior_models.md)
- [Electoral Systems](api/electoral_systems.md)
- [Metrics](api/metrics.md)
- [Coalition & Government](api/coalition.md)
- [Opinion Dynamics](api/opinion_dynamics.md)

### Country Presets
- [Overview](presets/README.md)
- [India (Lok Sabha)](presets/india.md)
- [Other Countries](presets/countries.md)

### Advanced Topics
- [Voter Psychology](advanced/voter_psychology.md)
- [Performance Optimization](advanced/performance.md)
