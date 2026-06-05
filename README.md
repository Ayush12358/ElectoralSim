# ElectoralSim

<p align="center">
  <strong>High-Performance Electoral Simulation Toolkit</strong>
  <br><sub>Early-stage • Functional • Under active development</sub>
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

> **Disclaimer:** ElectoralSim is a simulation and electoral-system comparison toolkit, **not an election forecasting model**. Default country presets are structural demonstrations unless explicitly marked as calibrated against real election data. See [Limitations](#limitations) for more.

A modular simulation toolkit for electoral systems, voter behavior, and political dynamics. Uses a hybrid approach: voter populations are stored as vectorized Polars DataFrames (not individual Python objects) for million-scale performance, with [Mesa](https://mesa.readthedocs.io/) for model orchestration, Numba for JIT acceleration, and NetworkX for opinion dynamics.

---

## Feature Status

| Area | Status | Notes |
|------|--------|-------|
| **FPTP, PR allocation** (D'Hondt, Sainte-Laguë, Hare, Droop, MMP, parallel) | ✅ Stable | Numba-accelerated, tested |
| **IRV/RCV, STV, Approval, Condorcet, Borda, Score, PAV** | ✅ Stable | Full alternative system coverage |
| **Voter generation** (demographics, ideology, Big Five, Moral Foundations) | ✅ Stable | Rich synthetic voter profiles |
| **Behavior models** (Proximity, Valence, Retrospective, Strategic, WastedVote, Sociotropic) | ✅ Stable | Weighted composition via BehaviorEngine |
| **Metrics** (Gallagher, ENP, HHI, VSE, Efficiency Gap, partisan bias, compactness) | ✅ Stable | Validated against known values |
| **BatchRunner** (parameter sweeps, sensitivity, calibration, uncertainty) | ✅ Stable | Sequential & parallel; CI, quantiles, MCSE |
| **Country presets** (23 countries + EU Parliament) | 🟡 Beta | Structural presets; 13 calibrated-status metadata |
| **India simulator** (543 Lok Sabha) | ✅ Stable | BehaviorEngine, vote_mnl_fast, StateConfig |
| **EU Parliament** (720 MEPs, 27 states) | ✅ Stable | D'Hondt per-country, BehaviorEngine refactored |
| **Opinion dynamics** (BA, WS, ER networks, noisy voter, bounded confidence, zealots) | 🟡 Beta | Core algorithms tested; needs empirical validation |
| **Coalition & government** (MWC, MCW, Laver-Shepsle, collapse, hazard, strain) | ✅ Stable | Full formation + survival + hazard models |
| **Streamlit dashboard** | 🟡 Beta | 23 countries, scenario save/load, warning banners |
| **Redistricting/gerrymandering** (PrecinctGraph, ReCom, ensemble) | 🟡 Beta | Optional geometry dependencies |
| **Campaign models** (finance, media, registration, targeting, mobilization, polling) | 🟡 Beta | Full campaign-ecosystem modeling |
| **Primary elections** (open/closed, candidate selection) | 🟡 Beta | US-style intra-party competition |
| **Event manager** (scandals, shocks, election timeline, polls) | 🔶 Experimental | Activated when explicitly configured |
| **GPU acceleration** (CuPy) | 🔶 Experimental | Utility computation & MNL sampling only |

---

## Key Features

### Electoral Systems
| System | Methods | Status |
|--------|---------|--------|
| **Plurality** | First Past The Post (FPTP) | Stable |
| **Proportional** | D'Hondt, Sainte-Laguë, Hare Quota, Droop Quota, Open-list, Closed-list | Stable |
| **Mixed** | MMP (Mixed-Member Proportional), Parallel Mixed | Stable |
| **Ranked Choice** | IRV/RCV, STV (Single Transferable Vote), Borda Count | Stable |
| **Scoring** | Score (Range) Voting, Approval Voting, Condorcet Winner | Stable |
| **Committee** | PAV (Proportional Approval Voting) | Stable |

### Voter Behavior Models
- **Proximity Model** — Spatial voting based on ideological distance (Stable)
- **Valence Model** — Non-policy candidate appeal (Stable)
- **Retrospective Model** — Economic voting (reward/punish incumbents) (Stable)
- **Strategic Voting** — Wasted vote model with district-level viability (Stable)
- **Sociotropic/Pocketbook** — National vs personal economic evaluation (Beta)

### Opinion Dynamics (Beta)
- **Network Topologies** — Barabási-Albert, Watts-Strogatz, Erdős-Rényi, Random Regular
- **Models** — Bounded Confidence, Noisy Voter, Zealots (with Numba acceleration)

### Coalition & Government (Stable)
- **Formation** — MWC, MCW, Laver-Shepsle portfolio allocation
- **Stability** — Sigmoid/Linear/Exponential collapse, hazard models
- **Analysis** — Coalition strain, junior partner penalty, Cox hazard

### Metrics
- Gallagher Index, Loosemore-Hanby (disproportionality)
- Effective Number of Parties (Laakso-Taagepera), Herfindahl-Hirschman Index
- Efficiency Gap, Partisan Bias, Mean-Median Gap, Partisan Gini (gerrymandering)
- Polsby-Popper, Convex-Hull Compactness (district geometry)
- Voter Satisfaction Efficiency (VSE), Responsiveness, Swing Ratio

### Country Presets (23 Countries + EU)

> These are **structural presets** — they encode electoral-system rules, approximate party positions, and default parameters for demonstration and comparative simulation. They are not calibrated election forecasts. 13 have calibration-status metadata.

| Region | Countries |
|--------|-----------|
| **Asia** | 🇮🇳 India (543 Lok Sabha), 🇯🇵 Japan |
| **Europe** | 🇬🇧 UK, 🇩🇪 Germany, 🇫🇷 France, 🇪🇺 EU Parliament (720 MEPs), 🇮🇪 Ireland, 🇳🇱 Netherlands, 🇨🇭 Switzerland, 🇳🇴 Norway, 🇸🇪 Sweden, 🇪🇸 Spain, 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland, 🏴󠁧󠁢󠁷󠁬󠁳󠁿 Wales |
| **Americas** | 🇺🇸 USA, 🇧🇷 Brazil, 🇨🇦 Canada, 🇲🇽 Mexico, 🇨🇱 Chile |
| **Oceania/Africa** | 🇦🇺 Australia (House + Senate), 🇳🇿 New Zealand, 🇿🇦 South Africa |
| **Middle East** | 🇮🇱 Israel |

### Performance
- **Vectorized Polars DataFrames** for voter storage (not individual Python objects)
- **Numba JIT acceleration** for vote counting and MNL sampling (~10-50x over pure Python)
- **Batch parameter sweeps** for systematic exploration
- **Parallel execution** with multiprocessing (see [parallel caveat](#parallel-execution))

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

<p align="center">
  <img src="docs/assets/screenshot 1.png" alt="ElectoralSim Dashboard" width="800">
</p>

Features:
- Multi-country simulation (India, USA, UK, Germany, etc.)
- Dynamic parameters (economic growth, national mood, anti-incumbency)
- Real-time seat distribution and vote share charts
- Swing analysis and ideological landscape visualization

<p align="center">
  <img src="docs/assets/screenshot 2.png" alt="ElectoralSim Dashboard" width="800">
</p>
<p align="center">
  <img src="docs/assets/screenshot 3.png" alt="ElectoralSim Dashboard" width="800">
</p>

More screenshots: [`docs/assets/`](docs/assets/)

---

## Project Structure

```
electoral_sim/
├── core/               # ElectionModel, Config, CLI, Voter Generation, Provenance
├── agents/             # Voter, Party, Adaptive Strategy
├── behavior/           # Behavior models + Campaign models (6 campaign classes)
├── dynamics/           # Opinion dynamics (networks, noisy voter, bounded confidence)
├── engine/             # Numba acceleration, GPU, Coalition, Government, Hazards
├── events/             # Event manager, election timeline, poll generator
├── metrics/            # Indices (Gallagher, ENP, VSE), Gerrymandering metrics
├── presets/            # 23 countries + EU (config.py + election.py per preset)
│   ├── india/          # 543 constituencies, 17 parties, StateConfig
│   └── eu/             # 27 member states, 720 MEPs, per-country BehaviorEngine
├── systems/            # Allocation (PR, MMP, mixed), Alternative (IRV, STV, Borda, Score, PAV)
├── analysis/           # BatchRunner, Duverger, VSE, Sensitivity, Calibration, Redistricting
├── visualization/      # Plots (seats, votes, summary, ideological), Specialized
└── data/               # Historical election data, ingestion pipeline
```

---

## Performance Benchmarks

> Benchmarks below were run on an Intel i5-1135G7 (4C/8T, 16 GB RAM, Ubuntu 22.04, Python 3.12, Numba 0.65). Timings exclude Numba JIT warmup. Memory is RSS delta measured via `psutil`. See `benchmarks/` for reproducible scripts.

| Scale | Create Time | Election Time | Memory (RSS delta) |
|-------|-------------|---------------|---------------------|
| 10K voters | ~18ms | ~5ms | ~52 MB |
| 100K voters | ~109ms | ~35ms | ~15 MB |
| 500K voters | ~608ms | ~176ms | ~95 MB |
| 1M voters | ~1.2s | ~316ms | ~148 MB |

**Batch throughput:** ~5 elections/sec at 500K voters; up to ~30 elections/sec at smaller 10K-50K configurations (FPTP, default behavior, after JIT warmup).

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run integration tests only
pytest tests/test_integration.py -v

# Run stress tests
python benchmarks/stress_test.py
```

**Test suite:** 502 tests including:
- **Property-based tests** (Hypothesis) — random input generation
- **Parameterized tests** — all systems, presets, allocation methods
- **Performance smoke tests** — 1K, 10K voters timing
- **Error handling** — invalid inputs, edge cases
- **Preset smoke tests** — UK, US, Germany, India, etc.
- **Invariant tests** — seats non-negative, vote shares sum to 1, determinism with seeds

---

## Documentation

- [Usage Guide](USAGE.md) — Detailed API usage examples
- [docs/](docs/) — Full documentation
  - [API Reference](docs/api/) — Complete function/class documentation
  - [Country Presets](docs/presets/) — India, EU, and other country guides
  - [Advanced Topics](docs/advanced/) — Voter psychology, performance tuning
- [CITATIONS.md](docs/CITATIONS.md) — Academic references and citations
- [CITATION.cff](CITATION.cff) — Software citation metadata
- [FEATURE_COMPARISON.md](docs/FEATURE_COMPARISON.md) — How ElectoralSim compares to other tools

---

## Limitations

### What ElectoralSim Is
- A simulation and electoral-system **comparison toolkit**
- A **teaching and research prototyping** tool
- A way to explore how different electoral systems and voter assumptions interact

### What ElectoralSim Is Not
- ❌ An election **forecasting** model
- ❌ A **calibrated** public-opinion model (by default)
- ❌ A substitute for survey data or polling
- ❌ A validated behavioral model for all included countries

### Known Limitations
- **Country presets** use synthetic party positions and valence values — they are structural demos, not calibrated to real election data.
- **Voter psychology features** (Big Five, Moral Foundations, affective polarization) are synthetically generated and not derived from survey instruments.
- **2D ideological space** is a deliberate simplification; complex political systems (India, Brazil, EU) have dimensions (caste, region, language, religion) not captured.
- **India simulator** currently uses a specialized high-performance path separate from the generic `ElectionModel`; improvements to the core engine do not automatically benefit India.
- **GPU acceleration** is experimental and limited to utility computation and MNL sampling kernels; it has not been correctness-tested against CPU outputs.

### Parallel Execution Caveat
On Linux, Numba's OpenMP threading layer conflicts with Python's default `fork()`-based multiprocessing. If using `BatchRunner` with `n_jobs > 1`, you may encounter `BrokenProcessPool`. Workarounds:
```python
import multiprocessing
multiprocessing.set_start_method("spawn")
# or
import os; os.environ["OMP_NUM_THREADS"] = "1"
```

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
