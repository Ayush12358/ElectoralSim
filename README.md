# ElectoralSim

<p align="center">
  <strong>Advanced Agent-Based Electoral Simulation Toolkit</strong>
</p>

<p align="center">
  <a href="https://github.com/Ayush12358/ElectoralSim/actions/workflows/tests.yml"><img src="https://github.com/Ayush12358/ElectoralSim/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://github.com/Ayush12358/ElectoralSim/actions/workflows/lint.yml"><img src="https://github.com/Ayush12358/ElectoralSim/actions/workflows/lint.yml/badge.svg" alt="Lint"></a>
  <a href="https://codecov.io/gh/Ayush12358/ElectoralSim"><img src="https://codecov.io/gh/Ayush12358/ElectoralSim/branch/master/graph/badge.svg" alt="Coverage"></a>
  <a href="https://pypi.org/project/electoral-sim/"><img src="https://img.shields.io/pypi/v/electoral-sim.svg" alt="PyPI"></a>
  <a href="https://pypi.org/project/electoral-sim/"><img src="https://img.shields.io/pypi/pyversions/electoral-sim.svg" alt="Python"></a>
  <a href="https://pepy.tech/project/electoral-sim"><img src="https://static.pepy.tech/badge/electoral-sim" alt="Downloads"></a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0"></a>
  <a href="https://ayush12358.github.io/ElectoralSim/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue" alt="Documentation"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
</p>

<p align="center">
  <a href="https://ayush12358.github.io/ElectoralSim/">Documentation</a> •
  <a href="https://pypi.org/project/electoral-sim/">PyPI</a> •
  <a href="#quick-start">Quick Start</a>
</p>

A modular, high-performance simulation toolkit for electoral systems, voter behavior, and political dynamics. Built on [Mesa](https://mesa.readthedocs.io/) with Polars DataFrames for vectorized agent-based modeling at scale.

---

## Key Features

### Performance
- **1M+ voters** with vectorized Polars DataFrames & Numba JIT acceleration (89x speedup)
- **30 elections/second** batch simulation capability
- **Batch parameter sweeps** for systematic exploration
- **Parallel execution** with multiprocessing
- **Optional GPU support** via CuPy for massive-scale simulations

### Electoral Systems
| System | Methods |
|--------|---------|
| **Plurality** | First Past The Post (FPTP) |
| **Proportional** | D'Hondt, Sainte-Laguë, Hare Quota, Droop Quota |
| **Ranked Choice** | IRV/RCV, STV (Single Transferable Vote) |
| **Other** | Approval Voting, Condorcet Winner |

### Voter Behavior Models
- **Proximity Model** — Spatial voting based on ideological distance
- **Valence Model** — Non-policy candidate appeal (charisma, competence)
- **Retrospective Model** — Economic voting (reward/punish incumbents)
- **Strategic Voting** — Duverger's Law, wasted vote model
- **Sociotropic/Pocketbook** — National vs personal economic evaluation

### Voter Psychology
- **Big Five (OCEAN)** — Personality traits influencing ideology
- **Moral Foundations** — Haidt's Care, Fairness, Loyalty, Authority, Sanctity
- **Media Diet** — Voter-specific media bias and misinformation susceptibility
- **Affective Polarization** — In-group/out-group sentiment

### Opinion Dynamics
- **Network Topologies** — Barabási-Albert, Watts-Strogatz, Erdős-Rényi
- **Models** — Bounded Confidence, Noisy Voter, Zealots
- **Media Effects** — Mass media bias with Raducha susceptibility model

### Coalition & Government
- **Formation** — MWC, MCW, Laver-Shepsle portfolio allocation
- **Stability** — Sigmoid/Linear/Exponential collapse models
- **Analysis** — Coalition strain, junior partner penalty, Cox hazard

### Metrics
- Gallagher Index (disproportionality)
- Effective Number of Parties (Laakso-Taagepera)
- Efficiency Gap, Loosemore-Hanby, Herfindahl-Hirschman Index
- Voter Satisfaction Efficiency (VSE)

### Country Presets (11 Countries)
| Region | Countries |
|--------|-----------|
| **Asia** | 🇮🇳 India (543 Lok Sabha), 🇯🇵 Japan |
| **Europe** | 🇬🇧 UK, 🇩🇪 Germany, 🇫🇷 France, 🇪🇺 EU Parliament (720 MEPs) |
| **Americas** | 🇺🇸 USA, 🇧🇷 Brazil |
| **Oceania/Africa** | 🇦🇺 Australia, 🇿🇦 South Africa |

---

## Installation

```bash
pip install electoral-sim
```

**From source:**
```bash
git clone https://github.com/Ayush12358/ElectoralSim.git
cd ElectoralSim
pip install -e .
```

**Optional dependencies:**
```bash
pip install electoral-sim[viz]   # Visualization (matplotlib, plotly)
pip install electoral-sim[gpu]   # GPU acceleration (cupy)
pip install electoral-sim[all]   # Everything
```

---

## Command-Line Interface

Run simulations directly from the command line:

```bash
# Basic simulation
electoral-sim run --voters 50000 --constituencies 10

# Use country preset
electoral-sim run --preset india --output results.json

# Batch parameter sweeps
electoral-sim batch --config batch_config.json --output results.csv

# List available presets
electoral-sim list-presets
```

See the [CLI Guide](https://ayush12358.github.io/ElectoralSim/cli/) for comprehensive usage.

---

## Quick Start

### Basic Election

```python
from electoral_sim import ElectionModel

# Create model with 100K voters
model = ElectionModel(n_voters=100_000, seed=42)
results = model.run_election()

print(f"Turnout: {results['turnout']:.1%}")
print(f"Gallagher Index: {results['gallagher']:.2f}")
print(f"ENP (votes): {results['enp_votes']:.2f}")
```

### Country Presets

```python
# India - Full Lok Sabha simulation
from electoral_sim import simulate_india_election

result = simulate_india_election(n_voters_per_constituency=1000)
print(f"BJP: {result.seats['BJP']} seats")
print(f"NDA Alliance: {result.nda_seats} seats")

# Other countries
model = ElectionModel.from_preset("germany")  # MMP with 5% threshold
model = ElectionModel.from_preset("usa")       # 435 House districts
model = ElectionModel.from_preset("uk")        # 650 Commons seats
```

### Chainable API

```python
results = (
    ElectionModel(n_voters=100_000)
    .with_system("PR")
    .with_allocation("sainte_lague")
    .with_threshold(0.05)
    .with_temperature(0.3)  # More deterministic voting
    .run_election()
)
```

### Batch Runner - Parameter Sweeps

Systematic parameter exploration for sensitivity analysis:

```python
from electoral_sim.analysis import BatchRunner, ParameterSweep

# Define parameter sweep
sweep = ParameterSweep({
    'n_voters': [10_000, 50_000, 100_000],
    'temperature': [0.3, 0.5, 0.7],
    'economic_growth': [-0.02, 0.0, 0.02]
})

# Run batch with parallel execution  
runner = BatchRunner(
    model_class=ElectionModel,
    parameter_sweep=sweep,
    n_runs_per_config=5,
    n_jobs=4
)

results_df = runner.run()
runner.export_results('results.csv')
```

### Custom Behavior Engine

```python
from electoral_sim import (
    ElectionModel, BehaviorEngine, 
    ProximityModel, ValenceModel, StrategicVotingModel
)

# Build custom voter behavior
engine = BehaviorEngine()
engine.add_model(ProximityModel(weight=1.0))
engine.add_model(ValenceModel(weight=0.5))
engine.add_model(StrategicVotingModel(sensitivity=2.0))

model = ElectionModel(n_voters=50_000, behavior_engine=engine)
results = model.run_election()
```

### Opinion Dynamics

```python
from electoral_sim import ElectionModel, OpinionDynamics

# Create social network
od = OpinionDynamics(n_agents=10_000, topology="barabasi_albert", m=3)

# Simulate with opinion evolution
model = ElectionModel(n_voters=10_000, opinion_dynamics=od)
for _ in range(100):
    model.step()  # Opinions evolve
result = model.run_election()
```

### Coalition Formation

```python
from electoral_sim import form_government, coalition_strain
import numpy as np

seats = np.array([150, 120, 80, 50])
positions = np.array([0.6, -0.3, 0.1, -0.6])
names = ["Right", "Left", "Center", "Far-Left"]

gov = form_government(seats, positions, names)
print(f"Coalition: {gov['coalition_names']}")
print(f"Majority: {gov['seats']} seats")
print(f"Stability: {gov['stability']:.2f}")
```

---

## Streamlit Dashboard

Launch the interactive election explorer:

```bash
streamlit run app.py
```

Features:
- Multi-country simulation (India, USA, UK, Germany, etc.)
- Dynamic parameters (economic growth, national mood, anti-incumbency)
- Real-time seat distribution and vote share charts
- Swing analysis and ideological landscape visualization

---

## 🏗️ Project Structure

```
electoral_sim/
├── core/               # ElectionModel, Config, Voter Generation
├── agents/             # Voter, Party, Adaptive Strategy
├── behavior/           # Behavior models (Proximity, Valence, Strategic, etc.)
├── dynamics/           # Opinion dynamics (networks, bounded confidence)
├── engine/             # Numba/GPU acceleration, Coalition, Government
├── events/             # Event manager (scandals, economic shocks)
├── metrics/            # Gallagher, ENP, VSE, Efficiency Gap
├── presets/            # Country configs (11 countries + EU)
│   ├── india/          # 543 constituencies, 17 parties
│   ├── eu/             # 27 member states, 720 MEPs
│   └── ...
├── systems/            # Electoral systems (allocation, IRV, STV)
├── visualization/      # Plots, maps, animations
└── data/               # Historical election data
```

---

## Performance Benchmarks

| Scale | Create Time | Election Time | Memory |
|-------|-------------|---------------|--------|
| 10K voters | 18ms | 5ms | 52 MB |
| 100K voters | 109ms | 35ms | 15 MB |
| 500K voters | 608ms | 176ms | 95 MB |
| 1M voters | 1.2s | 316ms | 148 MB |
| 2M voters | 2.4s | 672ms | 181 MB |

**Batch elections:** ~200ms/election at 500K voters (5 elections/sec)

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run integration tests only
pytest tests/test_integration.py -v

# Run stress tests
python tests/stress_test.py
```

**Test coverage:** 222 tests with ~70% code coverage, including:
- **Property-based tests** (Hypothesis) - random input generation
- **Parameterized tests** - all systems, presets, allocation methods
- **Performance benchmarks** - 1K, 10K voters timing
- **Error handling** - invalid inputs, edge cases
- **Real-world validation** - UK, US, Germany metrics

---

## Documentation

- [Usage Guide](USAGE.md) — Detailed API usage examples
- [docs/](docs/) — Full documentation
  - [API Reference](docs/api/) — Complete function/class documentation
  - [Country Presets](docs/presets/) — India, EU, and other country guides
  - [Advanced Topics](docs/advanced/) — Voter psychology, performance tuning

---

## Tech Stack

| Component | Library |
|-----------|---------|
| Agent-Based Modeling | [Mesa](https://mesa.readthedocs.io/) |
| DataFrames | [Polars](https://pola.rs/) |
| JIT Acceleration | [Numba](https://numba.pydata.org/) |
| GPU Support | [CuPy](https://cupy.dev/) |
| Social Networks | [NetworkX](https://networkx.org/) |
| Visualization | [Plotly](https://plotly.com/), [Matplotlib](https://matplotlib.org/) |
| Dashboard | [Streamlit](https://streamlit.io/) |

---

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Mesa](https://mesa.readthedocs.io/) for the agent-based modeling framework
- Political science research on spatial voting, opinion dynamics, and coalition theory
- Electoral data from various national election commissions

---

<p align="center">
  <sub>Built with love for computational political science</sub>
</p>
