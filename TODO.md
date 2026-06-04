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

- [x] **P2** Refactor India preset to use ElectionModel engine
- [ ] **P5** Distributed computing support (Dask/Ray)
- [ ] **P5** Real-time visualization dashboard
- [ ] **P5** REST API for web integration
- [ ] **P5** Docker containerization
- [ ] **P5** Jupyter notebook integration

### Data & Validation

- [x] **P2** Add validation case framework (Germany 2021 Bundestag)
- [x] **P2** Add preset calibration status metadata
- [ ] **P5** Historical election data for all countries
- [ ] **P5** Calibration against real election results
- [ ] **P5** Sensitivity analysis tools
- [ ] **P5** Uncertainty quantification

---

## Bugs & Code Quality — Found 2026-06-04

### Bugs

- [ ] **P2** Fix `DivisionByZero` warning in `coalition_strain()` when weights sum to 0 — returns NaN, should return 0.0 (line 131)
- [ ] **P3** Fix `RuntimeWarning` in `coalition_strain()` — normalize weights without divide-by-zero risk
- [ ] **P2** EU Parliament preset has no `config.py` — has `election.py` only, unlike all other presets. Add `eu_config()` for PRESETS registry.
- [ ] **P3** `PartyAgents.step()` is bare `pass` — should call `adaptive_strategy_step()` or document why not
- [ ] **P3** `VoterAgents.step()` is bare `pass` — should call opinion dynamics or document why not

### Broad Exception Handling

- [ ] **P2** `core/cli.py:338` uses bare `except Exception` in `run_simulation()` — should catch specific errors
- [ ] **P2** `core/cli.py:402` uses bare `except Exception` in `run_batch()` — should catch specific errors
- [ ] **P2** `engine/gpu_accel.py:29` uses bare `except Exception` in `is_gpu_available()` — should catch `cupy.cuda.runtime.CUDARuntimeError` explicitly

### Stale/Placeholder Code

- [ ] **P3** `systems/allocation.py:216` has bare `pass` in a fallback import block — should raise `NotImplementedError` with guidance
- [ ] **P3** `engine/government.py:287` has bare `pass` with comment about discrete media effect — implement or remove

### Code Style

- [ ] **P3** `core/model.py:114` uses `Optional[ConstituencyManager]` — replace with `ConstituencyManager | None` (PEP 604 style, Python 3.10+)
- [ ] **P5** Add `py.typed` marker to MANIFEST.in for PEP 561 compliance

### Miscellaneous

- [ ] **P2** `app.py` imports `simulate_india_election` from `presets.india.election` directly — should use `electoral_sim` top-level import for consistency
- [ ] **P3** `MANIFEST.in` doesn't include `benchmarks/`, `docs/`, or `.github/` — consider adding for source distributions
- [ ] **P3** Auxiliary test files (`stress_test.py`, `benchmark_cache.py`) are not run by CI — add to test suite or document as manual-only

---

## Test Coverage Gaps — Found 2026-06-04

### Below 80% Coverage

- [ ] **P2** `engine/numba_accel.py` (42%, 184 stmts) — Numba JIT functions not exercised in tests
    - `dhondt_numba`, `sainte_lague_numba`, `fptp_count_numba`, `compute_utilities_numba`, `mnl_sample_numba`
    - Fallback code paths (non-Numba branches) also uncovered
    - `benchmark_numba()` function partially tested
- [ ] **P2** `engine/gpu_accel.py` (27%, 48 stmts) — GPU functions skip when CuPy unavailable
    - Need GPU hardware to test `compute_utilities_gpu`, `mnl_sample_gpu`
    - CPU fallback/mock tests could exercise error paths
- [ ] **P2** `dynamics/opinion_dynamics.py` (68%, 168 stmts) — Numba import fallback paths uncovered
    - NetworkX import fallback paths uncovered (lines 19-21, 27-36, 63)
    - Numba zealot + bounded confidence Numba branches uncovered (lines 249-269, 449-472)
    - `zealot_step()` standalone function never tested (line 198)
    - `if __name__ == '__main__'` block never tested (lines 449-472)
- [ ] **P2** `systems/alternative.py` (79%, 148 stmts) — `if __name__` block uncovered (lines 318-355)
    - Condorcet cycle edge case (lines 89-94)
- [ ] **P3** `visualization/specialized.py` (96%) — lines 56-57 uncovered (animation save path)
- [ ] **P3** `data/loaders.py` (94%) — lines 56, 78 uncovered (branch of incumbents from votes without seats column)

### Integration Test Coverage

- [ ] **P2** `tests/test_integration.py` has only 12 tests across 3 classes — should have more cross-module workflows
    - No integration test for: Model + Coalition (run election then form government)
    - No integration test for: BatchRunner + Presets
    - No integration test for: EventManager → Model → step() → run_election()
    - No integration test for: OpinionDynamics → Model → run_election() → results
- [ ] **P2** No hypothesis property-based tests exist (no `@given` decorators found)
    - Add property tests for: allocation sum invariant, turnout 0-1, ENP ≥ 1, Gallagher ≥ 0

### Warning Cleanup

- [ ] **P3** Fix `RuntimeWarning: invalid value encountered in divide` in `coalition_strain()` when weights sum to 0
    - This is the only warning in the test suite — fix it for a clean `-W error` run
- [ ] **P3** Register `pytest.mark.slow` in `pyproject.toml` to eliminate `PytestUnknownMarkWarning`
    - Add to `[tool.pytest.ini_options] markers = ["slow: marks tests as slow"]`

### Test File Organization

- [x] **P1** Reorganize tests from 5 chaotic files into 11 disciplined files
- [ ] **P3** Move `stress_test.py` and `benchmark_cache.py` into proper test files or `benchmarks/`

---

## Architecture & Design Debt — Found 2026-06-04

### India Preset (Ongoing)
- [x] **P2** Extract data constants from `election.py` → `data.py`
- [x] **P2** Create `config.py` with `india_config()` for PRESETS registry
- [x] **P2** Use `fptp_count_fast` for per-state counting
- [ ] **P3** Make India preset use BehaviorEngine instead of hand-rolled `compute_state_party_utilities()`
- [ ] **P3** Make India preset use `vote_mnl_fast()` instead of hand-rolled MNL sampling
- [ ] **P3** Make India preset use `_decide_turnout()` instead of hand-rolled turnout logic
- [ ] **P3** Extract `STATE_PARTY_WEIGHTS` and `STATE_IDEOLOGY_SHIFTS` into per-constituency Config
- [ ] **P5** Make `ElectionModel` aware of state regions so India sim doesn't need to batch manually

### EU Preset
- [ ] **P2** Create `presets/eu/config.py` with `eu_config()` function for PRESETS registry
- [ ] **P2** Extract `EU_POLITICAL_GROUPS` and `COUNTRY_GROUP_WEIGHTS` from `election.py` into `data.py`
- [ ] **P3** Split `simulate_eu_election()` to use `ElectionModel` per country (mirror India refactor)
- [ ] **P3** EU preset currently has no `config.py` — inconsistent with all other presets

### Engine
- [ ] **P2** `voter_behavior.py` uses `if isinstance(model, X)` dispatch — replace with registry pattern or method dispatch
- [ ] **P3** `numba_accel.py` Numba fallback functions duplicate logic from `systems/allocation.py` — consolidate
- [ ] **P2** `coalition_strain()` has inconsistent behavior with zero-weight input — guard division

### API Design
- [ ] **P3** `electoral_sim/__init__.py` doesn't export `agents/` or `events/` subpackages — only individual symbols
- [ ] **P3** No public API for `VoterAgents` or `PartyAgents` from top-level — users can't manipulate agents directly
- [ ] **P5** `ElectionModel` constructor has 20+ parameters — consider builder pattern or validate-only config input

---

## Documentation Gaps — Found 2026-06-04

- [ ] **P2** No API reference for `PartyAgents` and `VoterAgents` class methods (`get_positions()`, `get_valence()`, etc.)
- [ ] **P2** No documentation for `adaptive_strategy_step()` or `EventManager` in user-facing docs
- [ ] **P3** `CITATION.cff` exists but `docs/CITATIONS.md` not linked from README
- [ ] **P3** `VALIDATION.md` has template but no populated data — needs a real calibration pass
- [ ] **P3** `FEATURE_COMPARISON.md` is research-only, not user-facing — add "How We Compare" to README
- [ ] **P3** `docs/` mkdocs structure doesn't include new files (`WORKFLOW.md`, `ITERATION.md`, `CITATIONS.md`, etc.)
- [ ] **P3** `examples/` directory has only 2 scripts — add examples for coalition, government, duverger, opinion dynamics
- [ ] **P3** No `CHANGELOG.md` entry for v0.1.1 changes beyond version bump
- [ ] **P5** No tutorial/quickstart for new users beyond README code snippets

---

## CI/CD & Infrastructure — Found 2026-06-04

- [ ] **P3** Add `pytest -W error` to CI lint/test jobs to catch warnings as errors
- [ ] **P3** Register `pytest.mark.slow` in `pyproject.toml` to fix `PytestUnknownMarkWarning`
- [ ] **P3** Run `benchmarks/benchmark_core.py` as a CI smoke test (small voter counts, verify no crash)
- [ ] **P3** Add `app.py` Streamlit import verification in `test-optional-deps` CI job
- [ ] **P3** `scripts/` directory has 7 files, many likely unused — audit and clean up
    - `release.py`, `do_release.py`, `bump_version.py` — consolidate into one release workflow
    - `benchmark_gpu.py`, `benchmark_scale.py` — move to `benchmarks/` directory
- [ ] **P5** Add `.pre-commit-config.yaml` for pre-commit hooks (Black, Ruff, mypy)

---

## auto Branch — Items to Merge to master

The following changes are currently on the `auto` branch and not in `master`:
- [ ] **P2** Merge India preset refactor into `master` (config.py, data.py, election.py rewrite)
- [ ] **P2** Merge calibration status metadata into `master` (all 8 country configs)
- [ ] **P2** Merge validation framework into `master` (docs/VALIDATION.md)
- [ ] **P1** Merge citations into `master` (docs/CITATIONS.md)
- [ ] **P1** Merge feature comparison into `master` (docs/FEATURE_COMPARISON.md)

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
