# ElectoralSim

Agent-based electoral simulation for India using [mesa-frames](https://github.com/mesa/mesa-frames).

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Scale**: Simulate 100K+ voters with mesa-frames vectorization
- **Electoral Systems**: FPTP, PR (D'Hondt, Sainte-Laguë)
- **Voting Models**: Proximity, Multinomial Logit
- **Metrics**: Gallagher Index, ENP, Efficiency Gap
- **Coalition**: MCW/MWC formation, strain analysis
- **Government**: Stability models (sigmoid, linear, exponential)
- **Presets**: India, USA, UK, Germany

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
- **[NetworkX](https://networkx.org/)** — Social networks (planned)
- **[NumPy](https://numpy.org/)** — Numerical operations

## License

MIT
