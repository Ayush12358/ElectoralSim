# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-06-04

### Fixed
- **South Africa export typo**: `SOUTH_AF_RICA_PARTIES` → `SOUTH_AFRICA_PARTIES` in `__all__`.
- **India preset `__init__.py`**: was empty; now exports `simulate_india_election`, `IndiaElectionResult`, etc.
- **Visualization import**: `visualization.charts` → `visualization` (silent `ImportError` now caught explicitly).
- **GPU FPTP stub**: `fptp_count_gpu()` returned zero seats silently; now raises `NotImplementedError`.
- **Numba multiprocessing crash**: `BatchRunner._run_parallel()` uses `spawn` context + sets `OMP_NUM_THREADS=1` in workers.
- **Party placeholders**: `PartyAgents.step()` docstring now references actual `adaptive_strategy_step()`.

### Changed
- **README rewrite**: Honest recalibration — "Advanced Toolkit" → "Early-stage · Functional". Added disclaimer, feature maturity table, limitations section, and parallel execution caveat.
- **Performance claims qualified**: Benchmark table now includes hardware/environment details. 2M voter row removed.
- **Test count updated**: 222 → 237 in README.
- **API maturity labeling**: `__init__.py` split into `STABLE` and `BETA` sections with clear comments.
- **Preset documentation**: All 8 country presets now have data provenance source notes and parameter rationale docstrings.

### Added
- **`benchmarks/benchmark_core.py`**: Reproducible performance script with env reporting, warmup, and voter/FPTP/PR/batch benchmarks.
- **`benchmarks/README.md`**: Methodology documentation.
- **CI job**: Optional dependency import smoke tests (viz, streamlit).
- **Dashboard screenshots**: `docs/assets/` with inline image in README.

## [0.1.0] - 2025-12-26

### Added
- **BatchRunner Suite**: A powerful tool for running parallel Monte Carlo simulations and parameter sweeps.
  - Parallel execution using `ProcessPoolExecutor`.
  - Result aggregation into Polars DataFrames.
  - Progress tracking with `tqdm`.
  - Flattened CSV/Parquet export for downstream analysis.
- **CLI Enhanced**: New `batch` command for running sweeps from the terminal.
- **Mesa v3.4.0 Support**: Full adoption of Mesa 3.4.0 features, including universal time (`model.time`).
- **Python 3.12/3.13 Compatibility**: Modernized codebase for the latest Python versions.

### Changed
- **Breaking**: Dropped support for Python 3.11. Minimum requirement is now Python 3.12.
- **Breaking**: Migrated project license from MIT to **Apache License 2.0**.
- **Mesa Upgrade**: Standardized on Mesa v3.4.0+.

### Fixed
- **Reproducibility**: Guaranteed deterministic results in `BatchRunner` through hierarchical seeding.
- **CI Stability**: Resolved version conflicts between `numba`, `numpy`, and `scipy` in GitHub Actions.
- **Linting**: Cleaned up codebase to comply with modern `ruff` and `black` standards.

## [0.0.2] - 2024-12-25

### Changed
- **Breaking**: Migrated from `mesa-frames` to `Mesa 3.0+` with `Polars` DataFrames
- Updated minimum Python version to 3.11

### Added
- **Comprehensive Test Suite** - 225 tests with ~70% coverage
  - Property-based tests using Hypothesis
  - Parameterized tests for all systems and presets
  - Performance benchmarks
  - Real-world validation tests (UK, US, Germany metrics)
- Added `hypothesis` to dev dependencies

### Fixed
- Mesa 3.0 API compatibility (Model.__init__ signature changes)
- RNG consistency using `self.rng` (NumPy Generator) throughout
- Removed all legacy `mesa-frames` references from code and docs

### Removed
- `mesa-frames` dependency (replaced with pure Mesa + Polars)

---

## [0.0.1] - 2024-12-25

### Added

#### Core Features
- `ElectionModel` - Main simulation class with chainable API
- `Config` and `PartyConfig` - Configuration dataclasses
- FPTP and PR electoral systems
- D'Hondt, Sainte-Laguë, Hare, and Droop allocation methods
- IRV, STV, Approval Voting, and Condorcet systems

#### Voter Behavior
- `BehaviorEngine` - Modular utility computation
- `ProximityModel`, `ValenceModel`, `RetrospectiveModel`
- `StrategicVotingModel`, `WastedVoteModel`, `SociotropicPocketbookModel`

#### Voter Psychology
- Big Five (OCEAN) personality traits
- Moral Foundations (Haidt)
- Media diet and misinformation susceptibility
- Affective polarization

#### Opinion Dynamics
- `OpinionDynamics` - Social network-based opinion evolution
- Barabási-Albert, Watts-Strogatz, Erdős-Rényi topologies
- Bounded Confidence and Noisy Voter models

#### Coalition & Government
- MWC and MCW coalition formation
- Government stability simulation
- Laver-Shepsle portfolio allocation

#### Metrics
- Gallagher Index, ENP, Efficiency Gap, VSE

#### Country Presets
- India (543 constituencies, 17 parties)
- USA, UK, Germany, Brazil, France, Japan
- Australia (House + Senate), South Africa
- EU Parliament (27 states, 720 MEPs)

#### Performance
- Numba JIT acceleration
- Optional GPU support (CuPy)
- 1M+ voter capacity
