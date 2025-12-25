# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
