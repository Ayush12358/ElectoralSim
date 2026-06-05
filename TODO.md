# ElectoralSim — Roadmap

> 454 tests. All P1/P2 complete. 59 items remain (18 P3, 41 P5).

---

## P3 — Active Work

### Module Splits

10 of 17 oversized modules under 250 LOC. 7 remain:

| Module | Lines | Difficulty |
|--------|-------|------------|
| `core/model.py` | 1000 | Core orchestrator — high regression risk |
| `engine/coalition.py` | 544 | Intertwined MWC/MCW/government stability |
| `analysis/batch_runner.py` | 429 | Tight class coupling |
| `systems/allocation.py` | 421 | Circular import with mixed systems |
| `dynamics/opinion_dynamics.py` | 403 | Numba kernels interwoven |
| `presets/india/election.py` | 383 | Monolithic state iteration |
| `engine/numba_accel.py` | 363 | JIT-compiled functions |

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

### Tooling & Test Infrastructure

#### CI Hardening

- [ ] **P3** Add `mypy` to CI lint workflow
    - Config exists in `pyproject.toml` with `warn_return_any=true`, `warn_unused_ignores=true`
    - Pre-commit hook commented out at `.pre-commit-config.yaml:27-31`
    - Currently 114 errors in 29 files — start with `mypy electoral_sim/ --ignore-missing-imports || true` (soft gate), tighten later
    - Eventually add to pre-commit hook (uncomment `mirrors-mypy` block)
    - Long-term: flip `disallow_untyped_defs=true` and make mypy a hard gate
- [ ] **P3** Add `bandit` SAST to CI
    - New job or step: `bandit -r electoral_sim/ -f json -o bandit-report.json`
    - Upload SARIF to GitHub Security tab
    - Exclude test fixtures from scan (`--exclude tests/`)
- [ ] **P3** Add `pip-audit` to CI
    - New job or step in existing workflow
    - Currently only mentioned as user advice in `SECURITY.md` — needs automation
    - Add `pip-audit` to dev deps in `pyproject.toml`
- [ ] **P3** Add `pre-commit` CI gate
    - New job: `pre-commit run --all-files --show-diff-on-failure`
    - Catches formatting/lint drift when contributors skip local pre-commit install
    - Add `pre-commit` to CI deps in workflow YAML
- [ ] **P3** Expand CI test matrix to include Python 3.11
    - Current: 3.12 + 3.13 only
    - The original migration was from py3.11→3.12; add 3.11 back for compatibility verification
    - Update `pyproject.toml` `requires-python` if 3.11 is not listed

#### Test Infrastructure

- [ ] **P3** Create `tests/conftest.py` with shared fixtures
    - `seeded_model(n_voters=1000, seed=42)` — returns configured `ElectionModel`
    - `small_config(n_parties=3)` — returns `Config` dataclass for unit tests
    - `voter_frame(n=100, seed=42)` — returns `pl.DataFrame` of synthetic voters
    - `party_frame(n=3)` — returns `pl.DataFrame` of synthetic parties with positions
    - `known_votes()` — returns standard vote arrays [100, 80, 30] used in 9 inline tests
    - Eliminates ~300 lines of repeated `ElectionModel(n_voters=..., seed=42)` boilerplate across 11 test files
- [ ] **P3** Create `tests/fixtures/elections/` with golden JSON files
    - Shape: `{"system": "irv", "candidates": [...], "ballots": [[...]...], "expected": {"winner": "...", "elimination_order": [...]}}`
    - `fptp_basic.json` — simple plurality, 3 candidates
    - `irv_basic_transfer.json` — 3-candidate IRV with single transfer
    - `irv_multi_transfer.json` — 5-candidate IRV with multiple eliminations
    - `stv_surplus_transfer.json` — STV surplus distribution (Droop quota)
    - `pr_dhondt_known.json` — D'Hondt: votes [100,80,30], 5 seats → [3,2,0]
    - `pr_sainte_lague_known.json` — Sainte-Laguë: votes [100,80,30], 5 seats → [2,2,1]
    - `pr_hare_known.json` — Hare quota with known split
    - `pr_droop_known.json` — Droop quota with known split
    - `coalition_mwc_basic.json` — minimum winning coalition with known membership
    - `coalition_mcw_basic.json` — minimum connected winning with known membership
    - Replace 9 inline hardcoded `assert seats.tolist() == [3, 2, 0]` tests with file-backed validation
    - Each fixture loaded via a `pytest.mark.parametrize` loop over all JSON files
- [ ] **P3** Add core invariant property tests via Hypothesis
    - `test_fptp_total_votes_preserved` — sum of votes across all parties == total votes cast
    - `test_fptp_seats_match_constituencies` — FPTP winner gets exactly 1 seat per constituency
    - `test_pr_seats_sum_to_house_size` — sum(party.seats) == n_seats across all allocators
    - `test_irv_winner_is_not_eliminated` — IRV winner never appears in elimination_order
    - `test_irv_majority_winner` — IRV winner has >50% of active votes in final round
    - `test_stv_winners_count_equals_seats` — len(winners) == n_seats
    - `test_allocation_monotonicity` — more votes never yields fewer seats (monotonicity)
    - `test_gallagher_bounded_0_100` — Gallagher index ∈ [0, 100]
    - `test_enp_bounded_1_n` — ENP ∈ [1, n_parties]
    - `test_coalition_majority` — coalition seat share > 50%
    - `test_seed_determinism` — same seed, same config → identical results (strengthen existing 2-test class)
    - `test_different_seeds_diverge` — at least 1 metric differs across 3+ seeds
- [ ] **P3** Fix test count everywhere
    - README.md: 502 → 454 (line ~55: "502 tests including")
    - tests/AGENTS.md: 401 → 454
    - pyproject.toml description: update if test count is mentioned
    - Add a conftest `pytest_configure` hook or a Make target that auto-verifies the count stays in sync

#### Performance Regression Prevention

- [ ] **P3** Add `pytest-benchmark` to dev deps and convert benchmark scripts
    - Add `pytest-benchmark>=4.0` to `[project.optional-dependencies] dev`
    - Add `[tool.pytest-benchmark]` config in `pyproject.toml` with `min-rounds=3`, `max-time=5`
    - Write benchmark tests with tight thresholds:
        - `test_voter_creation_10k(benchmark)` → < 30ms
        - `test_voter_creation_100k(benchmark)` → < 150ms
        - `test_fptp_election_100k(benchmark)` → < 50ms
        - `test_fptp_election_1M(benchmark)` → < 500ms
        - `test_pr_election_100k(benchmark)` → < 100ms
        - `test_batch_throughput_10k(benchmark)` → > 20 elections/sec
    - Add `--benchmark-only` marker to `pyproject.toml` for selective execution
    - Add `--benchmark-autosave` in CI to store baseline for regression comparison
- [ ] **P3** Wire CI `benchmark-smoke` job to assert actual timing thresholds
    - Current: `python -c "..."` runs at 500 voters, crash-only check
    - Add: run benchmark at 10K, 100K, 1M with hard thresholds
    - Fail PR if: 10K > 40ms OR 100K > 200ms OR 1M > 750ms
    - Upload benchmark results as CI artifact (`--benchmark-json=bench.json`)
    - Compare against stored baseline (`--benchmark-compare=baseline.json`) if available
    - Add `--benchmark-storage=benchmarks/.benchmarks` for local historical tracking
- [ ] **P3** Add dedicated perf regression workflow (or extend `benchmark-smoke`)
    - New job `perf-regression`: runs on PRs touching `electoral_sim/engine/`, `electoral_sim/systems/`, `electoral_sim/core/model.py`
    - Uses GitHub Actions `actions/cache` to store/restore baseline benchmark JSON
    - Posts a comment on PR if perf regresses >10%
    - Marks benchmark-only test class with `@pytest.mark.slow` for opt-in execution

#### Security & Auditing

- [ ] **P3** Enforce CodeQL findings as blocking
    - Current: CodeQL runs weekly and on push/PR but SARIF upload is advisory
    - Add `security-events: write` permission to workflow
    - Configure branch protection to block PRs with new CodeQL findings
- [ ] **P3** Add Dependabot grouping for CI/workflow bumps
    - Current: individual PRs for each Action (e.g., #10-#14 were all CI bumps)
    - Add `groups:` config to `.github/dependabot.yml` to batch GitHub Actions updates into single PR

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

- [ ] **P5** Expand Hypothesis property tests from 7→50+
    - Current: 7 tests in 2 files (test_unit.py: 5 allocation + metric invariants, test_engine.py: 2 IRV/STV no-crash)
    - Target modules: behavior engine (utility composition, weight normalization), opinion dynamics (convergence, bounded opinions), coalition formation (MWC/MCW invariants, seat majority), metrics (all indices bounded, monotonic), batch runner (determinism, parallel==sequential), preset loading (all 24 presets parse without error)
    - Add `@example` edge cases alongside `@given` for known-failure scenarios
    - Use `hypothesis.extra.numpy` for array-shaped strategies
    - Add `assume()` guards for invalid inputs (zero votes, empty arrays, single party)
- [ ] **P5** Add `syrupy` for snapshot/regression testing
    - Add `syrupy>=4.0` to dev deps
    - Snap key outputs at fixed seeds: `ElectionModel(seed=42).run_election()` → `result.json.snap`
    - Snap per-preset at known seed: `india(seed=42)`, `germany(seed=42)`, etc.
    - Snap coalition structures, seat distributions, opinion distributions
    - On refactor: any output change requires explicit `--snapshot-update` approval
    - Guard against silent behavioral regressions during module splits
- [ ] **P5** Add `mutmut` mutation testing to dev deps
    - `mutmut run` on `electoral_sim/systems/` and `electoral_sim/engine/`
    - Prove tests catch: `>= quota` → `> quota`, `-= 1` removed, `and` → `or` in conditionals
    - Target: >80% mutation kill rate on allocation + coalition code
    - Add `mutmut html` report generation as Make target
    - Alternative: evaluate `cosmic-ray` for distributed mutation testing on larger modules
- [ ] **P5** Set up `asv` (Airspeed Velocity) for continuous performance tracking
    - Create `asv.conf.json` at repo root, pointing at `benchmarks/benchmark_core.py` functions
    - Benchmark matrix: Python 3.12, commit range ~10 recent, 3 repeats
    - Add `asv run` to release workflow (before PyPI publish)
    - Generate time-series dashboard: `asv publish` + `asv gh-pages`
    - Track: voter creation, FPTP election, PR election, batch throughput at 10K/100K/1M
    - Alert if any metric regresses >15% vs previous release
- [ ] **P5** Add profiling tooling to dev deps
    - `py-spy` for sampling profiler: `py-spy record -o profile.svg -- python -m electoral_sim.core.model`
    - `line_profiler` for line-by-line hot-spot analysis on `numba_accel.py`, `allocation.py`, `opinion_dynamics.py`
    - Create `make profile` target that runs 1M-voter election under profiler
    - Document profiling workflow in `docs/advanced/performance.md`
- [ ] **P5** Machine-readable benchmark output + CI artifact pipeline
    - Add `--output json` / `--output csv` to `benchmark_core.py`, `benchmark_scale.py`
    - CI: upload benchmark JSON as artifact with commit SHA in filename
    - Add `scripts/compare_benchmarks.py` to diff two benchmark JSON files
    - Add PR comment bot that posts perf delta when engine/ code changes
- [ ] **P5** Source verification for political science claims
    - Add `scholarly`, `semantic-scholar`, `crossrefapi` to docs dev deps
    - Create `scripts/verify_sources.py` that checks all references in docs/ are resolvable
    - Rule: any claim about real countries, turnout, party systems, voter behavior, or electoral rules needs a citation OR must be marked as `[ASSUMPTION]` in docstrings
    - Add source verification as a CI job on docs/ changes
    - Mark all country presets with calibration status in `PRESET_PROVENANCE`
- [ ] **P5** AGENTS.md — add coding agent guardrails
    - Add "Core Invariants" section: total seats == requested, votes don't disappear unless system allows, seed → determinism, country presets must distinguish real data from assumptions
    - Add "Testing Expectations": fixture-based tests for every voting-system change, prefer property tests over mocks, add regression tests for bugs
    - Add "Documentation Expectations": political science claims need sources, unsourced claims must be labeled `[SIMPLIFIED]` or `[ASSUMED]`
    - Add "Anti-Hallucination Rules": never add hardcoded outputs to make tests pass, never assume electoral system behavior without a reference implementation or citation
- [ ] **P5** Create specialized `.github/agents/` definitions
    - `electoral-sim-maintainer.agent.md` — architecture review, merge-readiness, API compatibility, docs-match-implementation
    - `electoral-sim-electoral-systems.agent.md` — FPTP/PR/IRV/STV correctness, golden fixtures, seat allocation invariants
    - `electoral-sim-performance.agent.md` — detect O(n²), benchmark 10K/100K/1M, suggest vectorization, Numba profiling
    - `electoral-sim-docs-audit.agent.md` — verify references exist, label unsourced assumptions, ensure examples reproducible
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
| P3 Polish (pre-audit) | 58/76 ✅ |
| P4 Features | 10/10 ✅ |
| P5 Research (completed) | 43/80 ✅ |

**Total**: 232/287 completed (81%)

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

### v0.2.0 (Current)
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
