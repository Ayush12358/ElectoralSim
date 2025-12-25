# Country Presets

ElectoralSim includes pre-configured setups for 11 countries plus the EU Parliament.

## Available Presets

| Preset | Country | System | Seats | Parties |
|--------|---------|--------|-------|---------|
| `india` | India | FPTP | 543 | 17 |
| `usa` | USA | FPTP | 435 | 2 |
| `uk` | UK | FPTP | 650 | 6 |
| `germany` | Germany | MMP (PR) | 598 | 6 |
| `brazil` | Brazil | PR | 513 | 8 |
| `france` | France | Two-Round | 577 | 7 |
| `japan` | Japan | Mixed | 465 | 6 |
| `australia_house` | Australia | IRV | 151 | 5 |
| `australia_senate` | Australia | STV | 76 | 5 |
| `south_africa` | South Africa | PR | 400 | 6 |

## Using Presets

### Quick Start

```python
from electoral_sim import ElectionModel

model = ElectionModel.from_preset("germany", n_voters=100_000)
results = model.run_election()
```

### Override Parameters

```python
model = ElectionModel.from_preset(
    "india",
    n_voters=500_000,
    seed=42
)
```

### Access Config Directly

```python
from electoral_sim import germany_config

config = germany_config(n_voters=100_000)
print(f"System: {config.electoral_system}")
print(f"Parties: {[p.name for p in config.parties]}")
```

## Specialized Simulations

### India (Full Simulation)

For state-wise breakdown and alliance tracking:

```python
from electoral_sim import simulate_india_election

result = simulate_india_election(
    n_voters_per_constituency=1000,
    seed=42
)
```

See [India documentation](india.md) for details.

### EU Parliament

27 member states, 720 MEPs, 8 political groups:

```python
from electoral_sim import simulate_eu_election

result = simulate_eu_election(
    n_voters_per_mep=500,
    seed=42
)
```

See [Countries documentation](countries.md) for details.

## Detailed Documentation

- [India (Lok Sabha)](india.md) — 543 constituencies, state-level results
- [Other Countries](countries.md) — USA, UK, Germany, EU, and more
