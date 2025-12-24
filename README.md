# ElectoralSim - India Electoral Simulation

Agent-based electoral simulation for India using mesa-frames.

## Features (in progress)

- 543 Lok Sabha constituencies
- Multi-party system with PR and FPTP
- Opinion dynamics on social networks
- India-specific: NOTA, reserved constituencies, EVM

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from electoral_sim import ElectionModel

# Create model with 100K voters across 10 constituencies
model = ElectionModel(n_voters=100_000, n_constituencies=10)

# Run simulation
model.run(n_steps=100)

# Get results
results = model.get_election_results()
```

## Project Structure

```
electoral_sim/
├── agents/           # Voter, Candidate agents (mesa-frames)
├── models/           # Election model, voting behavior
├── systems/          # Electoral systems (PR, FPTP, MMP)
├── networks/         # Opinion dynamics, social networks
├── india/            # India-specific features
└── metrics/          # Indices (Gallagher, ENP)
```

## Tech Stack

- **mesa-frames** - Agent-based modeling with Polars
- **Polars** - High-performance DataFrames
- **NetworkX** - Social network topologies
- **NumPy** - Numerical operations

## License

MIT
