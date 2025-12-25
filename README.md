# ElectoralSim

<p align="center">
  <strong>🗳️ Advanced Agent-Based Electoral Simulation Toolkit</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="#"><img src="https://img.shields.io/badge/tests-63%20passed-brightgreen.svg" alt="Tests"></a>
  <a href="#"><img src="https://img.shields.io/badge/coverage-P1--P4%20complete-success.svg" alt="Coverage"></a>
</p>

A modular, high-performance simulation toolkit for electoral systems, voter behavior, and political dynamics. Built on [mesa-frames](https://github.com/mesa/mesa-frames) for vectorized agent-based modeling at scale.

---

## ✨ Key Features

### 🚀 Performance
- **1M+ voters** with vectorized mesa-frames & Numba JIT acceleration (89x speedup)
- **30 elections/second** batch simulation capability
- **Optional GPU support** via CuPy for massive-scale simulations

### 🗳️ Electoral Systems
| System | Methods |
|--------|---------|
| **Plurality** | First Past The Post (FPTP) |
| **Proportional** | D'Hondt, Sainte-Laguë, Hare Quota, Droop Quota |
| **Ranked Choice** | IRV/RCV, STV (Single Transferable Vote) |
| **Other** | Approval Voting, Condorcet Winner |

### 🧠 Voter Behavior Models
- **Proximity Model** — Spatial voting based on ideological distance
- **Valence Model** — Non-policy candidate appeal (charisma, competence)
- **Retrospective Model** — Economic voting (reward/punish incumbents)
- **Strategic Voting** — Duverger's Law, wasted vote model
- **Sociotropic/Pocketbook** — National vs personal economic evaluation

### 🧬 Voter Psychology
- **Big Five (OCEAN)** — Personality traits influencing ideology
- **Moral Foundations** — Haidt's Care, Fairness, Loyalty, Authority, Sanctity
- **Media Diet** — Voter-specific media bias and misinformation susceptibility
- **Affective Polarization** — In-group/out-group sentiment

### 🌐 Opinion Dynamics
- **Network Topologies** — Barabási-Albert, Watts-Strogatz, Erdős-Rényi
- **Models** — Bounded Confidence, Noisy Voter, Zealots
- **Media Effects** — Mass media bias with Raducha susceptibility model

### 🤝 Coalition & Government
- **Formation** — MWC, MCW, Laver-Shepsle portfolio allocation
- **Stability** — Sigmoid/Linear/Exponential collapse models
- **Analysis** — Coalition strain, junior partner penalty, Cox hazard

### 📊 Metrics
- Gallagher Index (disproportionality)
- Effective Number of Parties (Laakso-Taagepera)
- Efficiency Gap, Loosemore-Hanby, Herfindahl-Hirschman Index
- Voter Satisfaction Efficiency (VSE)

### 🌍 Country Presets (11 Countries)
| Region | Countries |
|--------|-----------|
| **Asia** | 🇮🇳 India (543 Lok Sabha), 🇯🇵 Japan |
| **Europe** | 🇬🇧 UK, 🇩🇪 Germany, 🇫🇷 France, 🇪🇺 EU Parliament (720 MEPs) |
| **Americas** | 🇺🇸 USA, 🇧🇷 Brazil |
| **Oceania/Africa** | 🇦🇺 Australia, 🇿🇦 South Africa |

---

## 📦 Installation

```bash
git clone https://github.com/Ayush12358/electoral-simulation-india.git
cd electoral-simulation-india
pip install -e .
```

**Optional dependencies:**
```bash
pip install -e ".[viz]"      # Visualization (matplotlib, plotly)
pip install -e ".[gpu]"      # GPU acceleration (cupy)
pip install -e ".[dev]"      # Development tools (pytest, etc.)
```

---

## 🚀 Quick Start

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

## 📊 Streamlit Dashboard

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

## ⚡ Performance Benchmarks

| Scale | Create Time | Election Time | Memory |
|-------|-------------|---------------|--------|
| 10K voters | 18ms | 5ms | 52 MB |
| 100K voters | 109ms | 35ms | 15 MB |
| 500K voters | 608ms | 176ms | 95 MB |
| 1M voters | 1.2s | 316ms | 148 MB |
| 2M voters | 2.4s | 672ms | 181 MB |

**Batch elections:** ~200ms/election at 500K voters (5 elections/sec)

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run integration tests only
pytest tests/test_integration.py -v

# Run stress tests
python tests/stress_test.py
```

**Test coverage:** 63 tests covering all P1-P4 features

---

## 📚 Documentation

- [Usage Guide](USAGE.md) — Detailed API usage examples
- [docs/](docs/) — Full documentation
  - [API Reference](docs/api/) — Complete function/class documentation
  - [Country Presets](docs/presets/) — India, EU, and other country guides
  - [Advanced Topics](docs/advanced/) — Voter psychology, performance tuning

---

## 🛠️ Tech Stack

| Component | Library |
|-----------|---------|
| Agent-Based Modeling | [mesa-frames](https://github.com/mesa/mesa-frames) |
| DataFrames | [Polars](https://pola.rs/) |
| JIT Acceleration | [Numba](https://numba.pydata.org/) |
| GPU Support | [CuPy](https://cupy.dev/) |
| Social Networks | [NetworkX](https://networkx.org/) |
| Visualization | [Plotly](https://plotly.com/), [Matplotlib](https://matplotlib.org/) |
| Dashboard | [Streamlit](https://streamlit.io/) |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [mesa-frames](https://github.com/mesa/mesa-frames) for the vectorized ABM framework
- Political science research on spatial voting, opinion dynamics, and coalition theory
- Electoral data from various national election commissions

---

<p align="center">
  <sub>Built with ❤️ for computational political science</sub>
</p>
