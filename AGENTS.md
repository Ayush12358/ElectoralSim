# ElectoralSim Knowledge Base

**Updated:** 2026-06-05
**Version:** v0.2.0
**Branch:** master

## Overview

Agent-based electoral simulation toolkit (Python 3.12+). Models voting behavior, electoral systems (FPTP, PR, IRV, STV, Borda, Score, PAV, MMP), opinion dynamics, coalition formation, and government stability across 23 country presets + EU Parliament. Uses Mesa for agent orchestration, Polars for vectorized data, Numba for JIT acceleration. 454 tests, ~85% coverage.

## Feature Implementation Workflow

See `docs/WORKFLOW.md` for the full step-by-step workflow for implementing features, fixes, and enhancements.

## Continuous Iteration Workflow

See `docs/ITERATION.md` for the meta-workflow that continuously picks tasks from TODO.md, implements them via WORKFLOW.md, and regenerates TODO.md when empty.

## Structure

```
./
├── electoral_sim/        # Main package (12 modules, 100+ .py files)
│   ├── core/             # ElectionModel, Config, CLI, Voter Generation
│   ├── agents/           # VoterAgents, PartyAgents, adaptive strategy
│   ├── behavior/         # Proximity, Valence, Strategic, Campaign models
│   ├── dynamics/         # Opinion dynamics (network-based, noisy voter, zealots)
│   ├── engine/           # Numba/GPU, Coalition, Government, Hazards
│   ├── systems/          # Allocation (D'Hondt, MMP, mixed), IRV, STV, Borda, Score, PAV
│   ├── metrics/          # Gallagher, ENP, VSE, Efficiency Gap, gerrymandering, compactness
│   ├── analysis/         # BatchRunner, Duverger, VSE, sensitivity, calibration, redistricting
│   ├── visualization/    # Plotly/Matplotlib plots, streamlit
│   ├── events/           # Event manager (scandals, shocks, election timeline, polls)
│   ├── presets/            # 23 country presets (including EU Parliament)
│   └── data/             # Historical election data files
├── app.py                # Streamlit dashboard (23 countries)
├── tests/                # 11 test files (454 tests, ~85% coverage)
├── benchmarks/           # Performance benchmark scripts
├── docs/                 # mkdocs-material documentation + WORKFLOW.md
└── scripts/              # Release scripts (bump_version, do_release)
```

## Where to Look

| Task | Path | Notes |
|------|------|-------|
| Run simulation | `electoral_sim/core/model.py` | `ElectionModel` - main entry point |
| Configure election | `electoral_sim/core/config.py` | `Config`/`PartyConfig` dataclasses |
| CLI entry point | `electoral_sim/core/cli.py` | `main()` function |
| Add voting system | `electoral_sim/systems/allocation.py` | Seat allocation algorithms |
| Add country preset | `electoral_sim/presets/<country>/config.py` | Follow existing pattern |
| Modify behavior | `electoral_sim/behavior/voter_behavior.py` | Behavior engine classes |
| Coalition logic | `electoral_sim/engine/coalition.py` | MWC/MCW/Laver-Shepsle |
| Government survival | `electoral_sim/engine/government.py` | Stability/survival models |
| Opinion dynamics | `electoral_sim/dynamics/opinion_dynamics.py` | Network topologies |
| Metrics | `electoral_sim/metrics/indices.py` | All electoral metrics |
| Add test | `tests/` | pytest, hypothesis property tests |
| Streamlit app | `app.py` | Interactive dashboard |
| Benchmarks | `benchmarks/benchmark_core.py` | Reproducible perf scripts |
| Release | `scripts/do_release.py` | PyPI release workflow |
| Feature workflow | `docs/WORKFLOW.md` | Step-by-step implementation guide |

## Conventions

### Code Style
- Black formatter, 100-char line length
- Ruff linting: E+F rules only, ignores E501/F401/F841/E402/F821
- Type hints throughout (`from __future__ import annotations` in modules)
- NumPy-style docstrings for all public functions/classes
- `@dataclass` for configuration objects
- Apache 2.0 license header on all source files

### Architecture
- **Mesa Model** pattern: `ElectionModel(Model)` with `step()` and `run_election()`
- **Polars DataFrames** for agent storage (not Mesa's built-in agent list)
- Chainable API: `.with_system("PR") .with_allocation("sainte_lague") .run_election()`
- `Config` dataclass drives model creation; `PartyConfig` for party definitions
- Behavior models registered via `BehaviorEngine` with weighted composition
- Numba fallback: graceful degradation with pure NumPy if Numba unavailable
- Module `__init__.py` re-exports public API (facade pattern)

### Imports
- First-party: `from electoral_sim.<module>.<submodule> import <Symbol>`
- Conditional imports for optional deps (matplotlib, cupy)
- `TYPE_CHECKING` guards for type-only imports

## Anti-Patterns

- **Never** use `mesa-frames` (deprecated, replaced by Polars directly)
- **Never** use `pd.DataFrame` (Polars only for agent data)
- **Never** suppress type errors with `# type: ignore` unless unavoidable
- **Never** modify `__init__.py` in presets without updating config module

## Commands

```bash
pip install -e ".[dev]"    # Install with dev deps
pytest tests/ -v            # Run tests
pytest tests/ --cov         # Coverage
black .                     # Format
ruff check .                # Lint
mkdocs serve                # Local docs
streamlit run app.py        # Dashboard
electoral-sim run --help    # CLI
```

## Notes

- Global `__version__` in `electoral_sim/__init__.py` (currently 0.2.0)
- Hypothesis property-based tests in test suite
- Presets follow strict pattern: `config.py` with party definitions + `__init__.py` exports
- `from_preset("country_name")` on `ElectionModel` is the preset entry point
