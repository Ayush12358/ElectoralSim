# presets/ — Country Configurations

## Overview

Each preset defines a real-world electoral system: party names, ideological positions, valence values, voting rules, and allocation methods. Accessed via `ElectionModel.from_preset("country_name")`, which maps to a function returning a `Config` object.

## Directory Structure

| Country | Type | Key Feature |
|---|---|---|
| `australia/` | Config | IRV for House, STV for Senate (two configs) |
| `brazil/` | Config | Open-list PR, 7 parties, D'Hondt |
| `eu/` | Script | 27 member states, 720 MEPs, 7 political groups |
| `france/` | Config | Two-round system (simulated as FPTP), 577 seats |
| `germany/` | Config | MMP with 5% threshold, Sainte-Lague |
| `india/` | Script | 543 constituencies, 17 parties, state-wise results |
| `japan/` | Config | Parallel system (FPTP + PR), 289 districts |
| `south_africa/` | Config | Pure PR, single national district |
| `uk/` | Config | Multi-party FPTP, 650 Commons seats |
| `usa/` | Config | Two-party FPTP, 435 House districts |

**Simple** (Config): config.py + `__init__.py` that re-exports the config function.
**Complex** (Script): election.py with dedicated simulation logic, custom result types.

## Pattern: Adding a New Preset

1. **Create `config.py`** — Define a function returning `Config` with party `PartyConfig(name, pos_x, pos_y, valence)` list, electoral system, allocation method, and threshold.
2. **Create `__init__.py`** — Import and re-export the config function and `*_PARTIES` dict.
3. **Register in parent `__init__.py`** — Add the import to `electoral_sim/presets/__init__.py` and include symbols in `__all__`.
4. **Add to `PRESETS` dict** — Map the country name string to the config function so `from_preset()` works.

## Special Presets

- **India** (`india/election.py`) — `simulate_india_election()` runs a full 543-constituency Lok Sabha simulation with 17 national and regional parties, state-by-state vote analysis, and alliance seat tracking. Returns `IndiaElectionResult` with `.seats`, `.votes`, `.state_results`, `.nda_seats`.
- **EU** (`eu/election.py`) — `simulate_eu_election()` models the 720-seat European Parliament across 27 member states with degressive proportionality, 7 political groups (EPP, S&D, Renew, Greens/EFA, ECR, ID, GUE/NGL), and country-level aggregation.

## Anti-Patterns

- **Never** modify a preset `__init__.py` without updating the parent `__init__.py` and the `PRESETS` dict. A missing entry silently breaks `from_preset()`.
- **Never** import directly from `presets/<country>/config` outside of the presets package — go through `electoral_sim.presets` or `ElectionModel.from_preset()`.
- **Never** add party definitions outside of `config.py` — party config is the single source of truth.
