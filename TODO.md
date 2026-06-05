# ElectoralSim — Roadmap

> 502 tests. All P1/P2 complete. 38 items remain (4 P3, 34 P5).

---

## P3 — Active Work

### Module Splits

9 of 17 oversized modules under 250 LOC. 8 remain:

| Module | Lines | Difficulty |
|--------|-------|------------|
| `core/model.py` | 1000 | Core orchestrator — high regression risk |
| `engine/coalition.py` | 544 | Intertwined MWC/MCW/government stability |
| `analysis/batch_runner.py` | 429 | Tight class coupling |
| `systems/allocation.py` | 421 | Circular import with mixed systems |
| `dynamics/opinion_dynamics.py` | 403 | Numba kernels interwoven |
| `presets/india/election.py` | 383 | Monolithic state iteration |
| `engine/numba_accel.py` | 363 | JIT-compiled functions |
| `metrics/indices.py` | 329 | Gerrandering already extracted; remainder is disproportionality |

- [ ] **P3** Split remaining modules under 250 LOC
    - Extract counting/results from `model.py`
    - Split government from coalition in `coalition.py`
    - Extract export/mixed-system modules from `allocation.py`
    - Extract state loop helpers from `india/election.py`

### Architecture

- [ ] **P3** Stable plugin/extension API for behavior models, voting systems, metrics, presets
    - Avoid edits to core registries for every extension
- [ ] **P5** `ElectionModel` aware of state regions — India sim batches manually
- [ ] **P5** Builder pattern for `ElectionModel` (20+ constructor params)

### Dashboard & Visualization

- [ ] **P3** Dashboard tabs: systems comparison, preset metadata, calibration status, uncertainty intervals
- [ ] **P3** Redistricting/geography visualizations: district maps, compactness histograms, ensemble plots, swing maps

---

## P5 — Future Research

### Electoral Systems & Dynamics

- [ ] **P5** Reinforcement-learning party strategy (median-voter, office-seeking, policy-seeking, vote-maximizing)
- [ ] **P5** Electoral college and weighted body systems
- [ ] **P5** Referendums and ballot measures
- [ ] **P5** Compulsory voting effects
- [ ] **P5** Multi-level elections (simultaneous national + regional)
- [ ] **P5** Time-series election dynamics
- [ ] **P5** Comparative electoral-system benchmark report (FPTP, PR, MMP, IRV, STV, Approval, Score, Borda, Condorcet)
- [ ] **P5** Deliberation and persuasion experiments (debate, social learning, elite cues, polarization)
- [ ] **P5** Misinformation intervention scenarios
- [ ] **P5** Turnout shocks (weather, holidays, conflict, administrative disruption)
- [ ] **P5** Overseas/absentee/mail voting channels
- [ ] **P5** Recount and audit simulation
- [ ] **P5** Malicious or accidental data-quality scenario tests

### Voter Behavior & Demographics

- [ ] **P5** Demographic synthetic population generation from census microdata (joint distributions)
- [ ] **P5** Ecological inference / small-area estimation bridge
- [ ] **P5** Voter registration and eligibility modeling
- [ ] **P5** Polling place accessibility

### Elections Administration

- [ ] **P5** International election-admin scenario dimensions (ballot access, campaign period, media access, complaints/appeals, counting/tabulation)
- [ ] **P5** Participatory budgeting / knapsack voting module

### Economic & Macro

- [ ] **P5** Macroeconomic scenario feeds (GDP, inflation, unemployment, approval proxies)

### Data, Calibration & ML

- [ ] **P5** Train voter behavior models on real survey data
- [ ] **P5** Predict election outcomes from poll data
- [ ] **P5** Historical election data for all countries
- [ ] **P5** Calibration against real election results

### Infrastructure & DX

- [ ] **P5** Distributed computing support (Dask/Ray)
- [ ] **P5** Real-time visualization dashboard
- [ ] **P5** REST API for web integration
- [ ] **P5** Docker containerization
- [ ] **P5** Jupyter notebook integration
- [ ] **P5** No tutorial/quickstart for new users beyond README code snippets

---

## Completed Summary

| Priority | Status |
|----------|--------|
| P1 Bugs & Technical Debt | 28/28 ✅ |
| P2 Features, Metrics, Presets | 93/93 ✅ |
| P3 Polish (pre-audit) | 58/62 ✅ |
| P4 Features | 10/10 ✅ |
| P5 Research (completed) | 43/77 ✅ |

**Total**: 232/270 completed (86%)

Key completions this session:
- 9 module splits (voter_behavior, batch_runner, opinion_dynamics, alternative, campaign, plots, cli, config, indices)
- ElectionResult wired into `run_election()`
- India/EU presets refactored to BehaviorEngine + vote_mnl_fast
- StateConfig extracted for India preset
- 10 stale P5 items marked complete
- 22 other P3 tasks (docs, CI, refactoring, presets)
- 1 critical bug fix (plot_india_state_map)

---

## Version History

### v0.1.1 (Current)
- Legitimacy audit: 6 bug fixes, honest README rewrite, benchmarks, CI, data provenance
- Fixed Numba multiprocessing crash, GPU stub, placeholder docstrings, import errors
- Added benchmark scripts, dashboard screenshots, API maturity labeling
- All 17 audit credibility items resolved

### v0.0.2
- Migrated from `mesa-frames` to `Mesa 3.0+` + `Polars`
- Comprehensive test suite (225 tests, ~70% coverage)
- Fixed Mesa 3.0 API compatibility

### v0.0.1
- Initial release with all P1-P4 features
- 11 country presets + EU Parliament

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute new features.

Priority areas:
1. Additional country presets with real party data
2. Validation against historical elections
3. Performance optimizations
4. Documentation improvements
