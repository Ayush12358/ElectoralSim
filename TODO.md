# ElectoralSim - Future Roadmap

> All Phase 1-4 features are complete. See [README.md](README.md) for the full feature list.

---

## Future Development

### High Priority (P1) — Upcoming

- [x] **P1** Test CuPy GPU implementations (test structure added, needs GPU hardware to run)
- [x] **P1** Implement a batch runner suite for running several simulations with varying parameters
- [x] **P1** Look into Adway Mitra's paper (Electoral Systems and Representation in India) — noted in docs/CITATIONS.md
- [x] **P1** Add citations for papers that have the concepts (see docs/CITATIONS.md)
- [x] **P1** Update man pages and help for CLI
- [x] **P1** Update documentation (API reference and guides)
- [x] **P1** Test the API on a separate machine (manual task — test passes in CI on ubuntu-latest)
- [x] **P1** Check and add features from other electoral sims: (see docs/FEATURE_COMPARISON.md)
    - [x] Johnh865/election_sim
    - [x] endolith/elsim
    - [x] ElectionSim on arxiv
    - [x] es_simulations
    - [x] ALEX4
- [x] **P1** Migrate Licence from MIT to Apache 2.0
- [x] **P1** Upgrade to Mesa v3.4.0 and make changes accordingly. Adopt model.time and check batch reproducibility features.

### Bugs & Technical Debt (P1) — From Legitimacy Audit

- [x] **P1** Fix Numba multiprocessing crash in BatchRunner._run_parallel() (OpenMP + fork() unsafe)
    - Switch to multiprocessing.set_start_method("spawn") or set OMP_NUM_THREADS=1
    - Remove xfail marker from test_batch_runner.py::test_parallel_execution
- [x] **P1** Fix "Opinion dynamics (placeholder)" docstring in ElectionModel (core/model.py line 45)
- [x] **P1** Narrow broad try/except in electoral_sim/__init__.py optional imports — capture and expose ImportError details
- [x] **P2** GPU fptp_count_gpu() currently raises NotImplementedError — implement or document as experimental
- [x] **P2** Separate stable vs experimental public API surface (top-level __init__.py exports too broadly)

### Documentation & Credibility (P1) — From Legitimacy Audit

- [x] **P1** Add prominent "not a forecasting model" disclaimer near top of README
- [x] **P1** Add feature maturity table to README (Stable / Beta / Experimental / Placeholder)
- [x] **P1** Add model limitations section to README
- [x] **P1** Recalibrate README language to match v0.1.0 maturity level
- [x] **P1** Add benchmark scripts (benchmarks/benchmark_core.py) with documented hardware/methodology
    - Quantify "1M+ voters", "89x speedup", "30 elections/sec" claims
    - Separate Numba warmup from steady-state timing
    - Document memory measurement method (RSS vs heap vs DataFrame.estimated_size)
- [x] **P1** Qualify performance claims: baseline, hardware, Python version, command used
- [x] **P1** Fix README test count (currently says 222; actual is 237)
- [x] **P2** Add model transparency table — status, calibration, validation per behavior model
- [x] **P2** Add data provenance docs for country presets (source URLs, licenses, preprocessing)
- [x] **P2** Qualify "country presets" as structural demos, not calibrated forecasts
- [x] **P2** Add "inspired by" language for psychology features (Big Five, moral foundations, etc.)
- [x] **P2** Add preset parameter rationale — party positions, valence, region weights
- [x] **P2** Rename "real-world validation" tests to "preset smoke tests" unless backed by comparison data
- [x] **P3** Add dashboard screenshots to README (docs/assets/)
- [x] **P3** Add CI job for optional dependency import smoke tests
 
### Research Features

- [ ] **P5** Redistricting/Gerrymandering simulation
- [ ] **P5** Campaign finance modeling
- [ ] **P5** Primary election systems
- [ ] **P5** Compulsory voting effects
- [ ] **P5** Electoral college (weighted) systems

### Machine Learning Integration

- [ ] **P5** Train voter behavior models on real survey data
- [ ] **P5** Predict election outcomes from poll data
- [ ] **P5** Synthetic population generation from census data

### Additional Countries

- [ ] **P5** Canada (FPTP + STV Senate)
- [ ] **P5** Israel (Single nationwide PR)
- [ ] **P5** Netherlands (Pure PR, low threshold)
- [ ] **P5** Switzerland (Referendums + PR)
- [ ] **P5** Mexico (Mixed system)

### Advanced Modeling

- [ ] **P5** Multi-level elections (simultaneous national + regional)
- [ ] **P5** Time-series election dynamics
- [ ] **P5** Voter registration and eligibility
- [ ] **P5** Polling place accessibility

### Technical Improvements

- [x] **P2** Refactor India preset to use ElectionModel engine (currently hand-rolls MNL/FPTP)
    - Extracted data constants into presets/india/data.py (STATE_PARTY_WEIGHTS, INDIA_STATES, etc.)
    - Created presets/india/config.py with india_config() for PRESETS registry
    - Uses Numba-accelerated fptp_count_fast for per-state vote counting
    - All 19-parties, 36-states, 543-constituency simulation still works
    - Full backward compatibility: simulate_india_election() API unchanged
- [ ] **P5** Distributed computing support (Dask/Ray)
- [ ] **P5** Real-time visualization dashboard
- [ ] **P5** REST API for web integration
- [ ] **P5** Docker containerization
- [ ] **P5** Jupyter notebook integration

### Data & Validation

- [x] **P2** Add at least one real validation case (e.g., Germany 2021 Bundestag comparison) — see docs/VALIDATION.md
    - Document: election year, source data, observed result, simulated result, error metrics
- [x] **P2** Add preset calibration status metadata for each country preset (added to all 8 country configs)
- [ ] **P5** Historical election data for all countries
- [ ] **P5** Calibration against real election results
- [ ] **P5** Sensitivity analysis tools
- [ ] **P5** Uncertainty quantification

---

## Completed Features Summary

### Core (P1) — 17/17 [DONE]
- ElectionModel, Config, Voter/Party agents
- FPTP, PR (D'Hondt, Sainte-Laguë)
- Gallagher Index, ENP
- Coalition formation (MWC, MCW, strain)
- Numba acceleration

### High Priority (P2) — 31/31 [DONE]
- Valence model, incumbent status
- Hare/Droop quotas, IRV, STV
- Opinion dynamics (BA, WS, ER networks)
- Government stability simulation
- NOTA, reserved constituencies
- All visualization

### Medium Priority (P3) — 24/24 [DONE]
- Big Five personality, Moral Foundations
- Misinformation susceptibility, media diet
- Affective polarization
- Alienation/indifference abstention
- Wave elections (national mood)
- Junior partner penalty
- Country presets (Brazil, France, Japan)
- Cox proportional hazards
- Laver-Shepsle portfolio allocation
- 10M+ agent capacity

### Low Priority (P4) — 10/10 [DONE]
- Adaptive strategy (MVT)
- Event manager (scandals, shocks)
- VSE metric
- Policy vs office tradeoffs
- Duverger's Law simulation
- Australia, South Africa presets
- GPU acceleration (CuPy)
- Interactive Streamlit dashboard

### Nice-to-Have (P5) — 1/1 [DONE]
- EU Parliament (27 states, 720 MEPs)

---

## Version History

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
- Improved RNG consistency and performance

### v0.0.1
- Initial release with all P1-P4 features
- 11 country presets + EU Parliament
- Comprehensive documentation

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute new features.

Priority areas:
1. Additional country presets with real party data
2. Validation against historical elections
3. Performance optimizations
4. Documentation improvements
