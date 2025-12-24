# ElectoralSim: Generic Electoral Simulation Toolkit

A modular agent-based modeling toolkit for electoral systems, voter behavior, and political dynamics using [mesa-frames](https://github.com/mesa/mesa-frames).

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Scale**: Simulate 1M+ voters with vectorized mesa-frames & Numba acceleration.
- **Electoral Systems**: FPTP, PR, STV, IRV, Approval, Condorcet.
- **Voter Behavior**: Modular engine with Proximity, Valence, Retrospective, and Strategic voting models.
- **Opinion Dynamics**: Pluggable social networks (Barabási-Albert, Watts-Strogatz) with Bounded Confidence & Noisy Voter models.
- **Metrics**: Gallagher Index, ENP, Efficiency Gap, HHI.
- **Coalition & Gov**: MWC/MCW formation models and stability/collapse simulation.
- **Presets**: High-level configurations for India, USA, UK, and Germany.

## Installation

```bash
git clone https://github.com/Ayush12358/electoral-simulation-india.git
cd electoral-simulation-india
pip install -e .
```

## Quick Start

```python
from electoral_sim import ElectionModel

# Simple usage
model = ElectionModel(n_voters=100_000)
results = model.run_election()

print(f"Turnout: {results['turnout']:.1%}")
print(f"Gallagher Index: {results['gallagher']:.2f}")
```

### Using Presets

```python
# India (543 Lok Sabha constituencies)
model = ElectionModel.from_preset("india")

# Germany (MMP with 5% threshold)
model = ElectionModel.from_preset("germany")
```

### Chainable API

```python
results = (
    ElectionModel(n_voters=100_000)
    .with_system("PR")
    .with_allocation("sainte_lague")
    .with_threshold(0.05)
    .run_election()
)
```

### CLI

```bash
# List presets
electoral-sim list-presets

# Run simulation
electoral-sim run --preset india --voters 100000 --output results.json
```

## Documentation

See [USAGE.md](USAGE.md) for full documentation.

## Project Structure

```
electoral_sim/
├── __init__.py      # Public API
├── model.py         # ElectionModel, VoterAgents, PartyAgents
├── config.py        # Config, PartyConfig, presets
├── cli.py           # Command-line interface
├── systems/         # FPTP, PR, allocation methods
├── metrics/         # Gallagher, ENP, efficiency gap
├── coalition.py     # MCW, MWC, strain
└── government.py    # Collapse models, stability
```

## Tech Stack

- **[mesa-frames](https://github.com/mesa/mesa-frames)** — Vectorized agent-based modeling
- **[Polars](https://pola.rs/)** — High-performance DataFrames
- **[Numba](https://numba.pydata.org/)** — Just-In-Time acceleration for core loops
- **[NetworkX](https://networkx.org/)** — Social networks
- **[NumPy](https://numpy.org/)** — Numerical operations

## License

MIT
