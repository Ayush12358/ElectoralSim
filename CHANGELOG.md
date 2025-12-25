# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
