# India (Lok Sabha)

Comprehensive simulation of Indian general elections.

## Overview

- **543 constituencies** (Lok Sabha seats)
- **30 states/UTs** with regional party weights
- **17 major parties** including national and regional
- **NDA/INDIA alliance** tracking
- **SC/ST reserved seats** support

## Quick Start

```python
from electoral_sim import simulate_india_election

result = simulate_india_election(
    n_voters_per_constituency=1000,
    seed=42,
    verbose=True
)

# Results
print(f"BJP: {result.seats['BJP']} seats")
print(f"INC: {result.seats['INC']} seats")
print(f"NDA Alliance: {result.nda_seats} seats")
print(f"INDIA Alliance: {result.india_seats} seats")
print(f"Turnout: {result.turnout:.1%}")
```

## Result Structure

```python
class IndiaElectionResult:
    seats: dict[str, int]           # Party -> seats won
    vote_shares: dict[str, float]   # Party -> vote share
    state_results: dict             # State-wise breakdown
    nda_seats: int                  # NDA alliance total
    india_seats: int                # INDIA alliance total
    other_seats: int                # Non-alliance seats
    turnout: float                  # Overall turnout
    gallagher: float                # Disproportionality
    enp_votes: float                # ENP by votes
    enp_seats: float                # ENP by seats
    voter_df: pl.DataFrame          # Voter data
    party_positions: dict           # Party ideology positions
    nota_contested_seats: int       # NOTA impact analysis
    nota_contested_list: list       # Constituencies where NOTA was significant
```

## Parties

### National Parties
| Party | Ideology | Alliance |
|-------|----------|----------|
| BJP | Center-Right | NDA |
| INC | Center-Left | INDIA |
| BSP | Social Justice | - |
| CPM | Left | INDIA |
| CPI | Left | INDIA |
| NCP | Center | INDIA |
| AAP | Anti-Corruption | INDIA |

### Regional Parties
| Party | State | Alliance |
|-------|-------|----------|
| TMC | West Bengal | INDIA |
| DMK | Tamil Nadu | INDIA |
| AIADMK | Tamil Nadu | NDA |
| SP | Uttar Pradesh | INDIA |
| JDU | Bihar | NDA |
| TDP | Andhra Pradesh | NDA |
| YCP | Andhra Pradesh | - |
| BJD | Odisha | - |
| SS | Maharashtra | INDIA |
| BRS | Telangana | - |

## State-wise Results

Access detailed state breakdown:

```python
result = simulate_india_election(n_voters_per_constituency=500)

# State results
for state, data in result.state_results.items():
    print(f"{state}: {data}")
```

## NOTA Analysis

Track "None of the Above" impact:

```python
result = simulate_india_election(
    n_voters_per_constituency=500,
    include_nota=True
)

print(f"NOTA contested {result.nota_contested_seats} seats")
for const in result.nota_contested_list:
    print(f"  - {const}")
```

## Reserved Constituencies

Model SC/ST reservation:

```python
from electoral_sim import ElectionModel

# Example: Reserve constituency 0 for specific parties
constraints = {0: ["BSP", "INC", "SP"]}

model = ElectionModel(
    n_voters=10_000,
    n_constituencies=5,
    constituency_constraints=constraints
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n_voters_per_constituency` | int | 1000 | Voters per seat |
| `seed` | int | None | Random seed |
| `verbose` | bool | True | Print progress |
| `include_nota` | bool | False | Enable NOTA option |
| `historical_data_path` | str | None | Path to seed with historical data |

## Historical Data Seeding

Use historical vote shares to initialize:

```python
result = simulate_india_election(
    n_voters_per_constituency=500,
    historical_data_path="electoral_sim/data/india_2024_sample.csv"
)
```
