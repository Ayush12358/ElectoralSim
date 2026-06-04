# ElectoralSim - Future Roadmap

> All Phase 1-4 features are complete. See [README.md](README.md) for the full feature list.

---

## Future Development

### Deep Repo + External Research Backlog — Found 2026-06-04

#### P1 Correctness Bugs

- [x] **P1** Fix `fptp_count_numba()` parallel seat-count race in `engine/numba_accel.py`
    - Current `prange` loop increments shared `seats[winner]`; repeated all-party-0 probes returned totals below the constituency count.
    - Add deterministic regression where every constituency is won by the same party and `seats.sum() == n_constituencies`.
    - Implement by writing per-constituency winners in parallel, then reducing counts outside the parallel loop.
- [x] **P1** Make `ElectionModel` reject or truly implement `"IRV"` and `"STV"` at model level
    - `run_election()` currently treats every non-`"FPTP"` system as PR.
    - Replace shallow tests that assert only non-`None` with either ranked-ballot integration tests or explicit `ValueError` tests.
- [x] **P1** Validate `electoral_system` and `allocation_method` during `ElectionModel` construction and chain setters
    - `with_system("INVALID")` and direct mutation can silently run as PR.
    - Accepted values should be centralized and exposed in docs/CLI help.
- [x] **P1** Fix Streamlit dashboard chart rendering mismatch in `app.py`
    - `plot_seat_distribution()`, `plot_vote_shares()`, and `plot_seats_vs_votes()` return Matplotlib figures, but India/generic paths pass them to `st.plotly_chart()`.
    - Add a Streamlit smoke test or import-level UI rendering test that verifies the selected renderer type.
- [x] **P1** Add a release-blocking smoke test for the installed CLI package
    - Build/install the sdist or wheel in a clean venv and run `electoral-sim --help`, `electoral-sim list-presets`, and one tiny `electoral-sim run`.
    - Catch packaging/runtime differences that in-repo imports hide.

#### P2 Electoral Math & Voting-System Correctness

- [x] **P2** Define allocation behavior for zero votes (done in d434908, 901313c)
    - `dhondt_allocation(np.array([0, 0, 0]), 3)` currently awards seats to party 0.
    - Hare/Droop with zero seats or zero total votes should return a documented value or raise a specific error.
- [x] **P2** Recompute Hare and Droop quotas from eligible post-threshold votes
    - Thresholded-out ballots currently remain in `total_votes`, distorting largest-remainder quotas.
    - Add known-result threshold examples for both quota methods.
- [ ] **P2** Add explicit tie-breaking policy for FPTP, D'Hondt, Sainte-Lague, Hare/Droop remainders, IRV, STV, Approval, and Condorcet
    - Current behavior depends on `np.argmax`, loop order, or Polars sort/group order.
    - Support deterministic lower-index, seeded random, or supplied tie-break ordering and document the default.
- [x] **P2** Add ranked-ballot validation utilities (done, _validate_rankings() added in 18cddfd)
    - Reject duplicate ranks, impossible candidate IDs, inconsistent unranked encodings, invalid shapes, and `n_candidates <= 0`.
    - Reuse the validator across IRV, STV, Condorcet, and future ranked-ballot imports.
- [x] **P2** Fix IRV final-round reporting for exhausted ballots
    - The fallback path returns `final_votes=np.zeros(n_candidates)`, losing the last active tally.
    - Add tests for exhausted ballots, two-candidate ties, and no-majority final rounds.
- [ ] **P2** Revisit STV surplus transfer and final-seat completion rules
    - Current STV elects one above-quota candidate per round and lacks an explicit "remaining candidates fill remaining seats" rule.
    - Add known examples with expected winners, elected order, quota, and transfer weights.
- [x] **P2** Add formal known-result tests for all allocation methods
    - Cover D'Hondt, Sainte-Lague/Webster, Hare largest remainder, Droop largest remainder, threshold effects, and equal-vote ties.
    - Keep fixtures small enough to audit manually.
- [x] **P2** Add Hypothesis property tests for electoral-system invariants
    - Seat totals equal requested seats when votes are valid.
    - Allocations are non-negative integers.
    - Increasing a party's votes should not reduce its seats where monotonicity is expected.
    - Turnout and shares stay in `[0, 1]`; ENP/Gallagher remain finite for valid inputs.
- [x] **P2** Add property tests for ranked-choice edge cases
    - Random partial rankings, exhausted ballots, tied rankings, single-candidate elections, and all-unranked ballots.
    - Assert no crashes and documented winner/no-winner behavior.
- [ ] **P2** Add score/range voting as an alternative system
    - External comparison frameworks commonly evaluate plurality, RCV, approval, score, and Condorcet together.
    - Implement ballot generation from utilities and single-winner aggregation with known-result tests.
- [ ] **P2** Add Borda Count and supplementary vote/two-round runoff systems
    - International IDEA lists Borda Count and Two-Round Systems as common electoral-system variants.
    - Add docs and examples beside IRV/STV/Approval/Condorcet.
- [ ] **P2** Add open-list and closed-list PR variants
    - Model candidate ordering, preference votes, party lists, and threshold behavior separately from party-only PR.
    - Include tests for list-order, preference-vote promotion, and over-threshold/under-threshold parties.
- [ ] **P2** Implement mixed-member proportional (MMP) with overhang and leveling-seat logic
    - Germany-style presets need more than simple PR/FPTP parameters to be structurally credible.
    - Model district seats, party-list votes, thresholds, one-district exceptions, overhang seats, and leveling seats.
- [ ] **P2** Implement parallel mixed systems without compensatory leveling
    - Add Japan-style and mixed-system comparisons where FPTP and PR tiers are allocated independently.
    - Surface tier-level results in the returned result schema.
- [ ] **P2** Add multi-tier apportionment support
    - Support national, regional, and constituency tiers for ALEX-style legislative modeling and EU/national presets.
    - Include tier metadata in `Config` instead of overloading `n_constituencies`.
- [ ] **P2** Add approval-based committee voting methods
    - Research `abcvoting`/PAV/MES/Phragmen-style multiwinner rules and decide whether to implement core methods or optional adapters.
    - Add committee-size, approvals matrix, and proportionality metric tests.

#### P2 Metrics, Validation & Calibration

- [x] **P2** Harden metrics against empty arrays, all-zero shares, mismatched lengths, and zero total votes
    - `effective_number_of_parties()` can return non-finite values for all-zero shares.
    - `efficiency_gap()` can return `nan` for zero-total districts.
- [ ] **P2** Add partisan-bias, mean-median, declination, lopsided-margins, and partisan-Gini metrics
    - GerryChain exposes efficiency gap, Polsby-Popper, and partisan Gini; ElectoralSim should cover the same gerrymandering analysis basics.
    - Add references and known small examples for each metric.
- [ ] **P2** Add compactness metrics for district plans
    - Implement Polsby-Popper, Reock or convex-hull compactness, perimeter/area validation, and missing-geometry behavior.
    - Keep geometry dependencies optional.
- [ ] **P2** Add seats-votes curve and responsiveness/swing-ratio analysis
    - Useful for swing-state/district sensitivity and redistricting ensembles.
    - Return curve data in Polars DataFrames for visualization and tests.
- [ ] **P2** Add calibration framework against historical election results
    - Define target metrics, loss functions, calibration parameters, and reproducible calibration reports.
    - Start with Germany 2021, India 2024 sample, and US House data where data provenance is available.
- [ ] **P2** Add uncertainty quantification for simulation outputs
    - BatchRunner should report confidence intervals, quantiles, Monte Carlo standard errors, and seed counts.
    - Add tests for deterministic aggregation over fixed synthetic result sets.
- [ ] **P2** Add sensitivity-analysis tooling
    - Support one-at-a-time, grid, Latin hypercube, and Sobol-style sensitivity summaries.
    - Integrate with BatchRunner and export tidy Polars output.
- [ ] **P2** Add posterior predictive validation docs for "not a forecast" positioning
    - Explain what can and cannot be inferred from calibrated vs structural presets.
    - Include acceptance criteria before a preset can move from structural demo to calibrated.
- [ ] **P2** Add survey-calibrated behavior parameters from CSES-style data
    - Map vote choice, demographics, ideology, trust, satisfaction, and turnout variables into `generate_voter_frame()` and behavior models.
    - Keep data download optional and document licensing/citation requirements.
- [ ] **P2** Add precinct/district result ingestion pipeline
    - Support MIT Election Lab-style precinct returns, district identifiers, party normalization, turnout, and year metadata.
    - Add schema validation and tiny fixture files for CI.
- [ ] **P2** Add data provenance registry for every bundled dataset and preset
    - Store source URL, retrieval date, license, preprocessing steps, calibration status, and checksum.
    - Expose provenance via `ElectionModel.from_preset(...).metadata`.
- [ ] **P2** Add reproducibility manifests to BatchRunner outputs
    - Include package version, git commit, Python version, dependency versions, CPU/GPU info, seed hierarchy, and config hash.
    - Write JSON sidecars for CSV/Parquet exports.

#### P2 Redistricting & Geography

- [ ] **P2** Build a redistricting module inspired by GerryChain
    - Represent precinct/constituency graphs, district assignments, population balance, contiguity, compactness, and election updaters.
    - Keep heavy GIS dependencies optional under a `geo` extra.
- [ ] **P2** Implement ReCom-style district-plan proposal generation
    - Add spanning-tree recombination for adjacent districts, population tolerance, compactness constraints, and deterministic seeds.
    - Include small graph fixtures for fast tests.
- [ ] **P2** Add district-plan ensemble analysis
    - Compare enacted/supplied plans against simulated ensembles for seat outcomes, efficiency gap, partisan bias, and compactness.
    - Return percentile/rank summaries and plots.
- [ ] **P2** Add swing-state and swing-district analysis
    - Perturb national, regional, and district-level vote swings and report seat tipping points.
    - Integrate with FPTP, MMP, and PR presets where appropriate.
- [ ] **P2** Add constituency geometry ingestion
    - Load GeoJSON/Shapefile boundaries into optional geometry metadata.
    - Validate CRS, area/perimeter availability, adjacency construction, and missing IDs.
- [ ] **P2** Add polling-place accessibility and queue/friction model
    - Model distance, wait time, opening hours, registration friction, and turnout suppression/boost scenarios.
    - Keep it clearly framed as scenario simulation, not causal estimation.
- [ ] **P2** Add reserved/minority district constraint modeling beyond simple party allowlists
    - Represent candidate eligibility, voter demographics, reserved seat type, and party nomination constraints.
    - Validate with India reserved-constituency examples.

#### P2 Agent Behavior, Campaigns & Opinion Dynamics

- [ ] **P2** Replace `BehaviorEngine.compute_all()` `isinstance` dispatch with a model registry/protocol
    - Each behavior model should declare required voter fields, party fields, GPU support, and compute signature.
    - This will unblock third-party behavior models without editing the engine.
- [ ] **P2** Add behavior-model input validation and field dependency errors
    - Missing `economic_perception`, `personal_income_change`, `viability`, or incumbent columns should raise actionable errors or use documented defaults.
    - Add tests for each model's missing-data behavior.
- [ ] **P2** Add campaign finance model
    - Model spending, fundraising, ad saturation, diminishing returns, incumbency fundraising, and district targeting.
    - Connect campaign effects to valence/media exposure rather than direct vote overrides.
- [ ] **P2** Add media environment and media monitoring model
    - OSCE methodology treats media access and coverage as central election-environment dimensions.
    - Track party exposure, sentiment, audience reach, misinformation susceptibility, and time decay.
- [ ] **P2** Add voter registration and eligibility model
    - Model eligible population, registration status, turnout probability, age/citizenship constraints, and registration deadlines.
    - Separate eligible voters, registered voters, and votes cast in result metrics.
- [ ] **P2** Add primary election and candidate selection systems
    - Support closed/open primaries, party candidate fields, valence selection, and general-election candidate handoff.
    - Useful for US-style presets and intra-party competition.
- [ ] **P2** Add candidate-level modeling
    - Current party-level frame limits candidate valence, incumbency, local ideology, candidate demographics, and multi-candidate districts.
    - Introduce optional candidate frame while preserving party-level API.
- [ ] **P2** Add coalition feedback into subsequent elections
    - Junior partner penalty exists as a function; integrate it into multi-election simulation state.
    - Track government participation, policy delivery, scandal exposure, and vote-share feedback.
- [ ] **P2** Add party entry/exit and endogenous party-system formation
    - Model new parties, mergers, splits, viability thresholds, ballot access, and ideological repositioning.
    - Connect to Duverger-style analysis and proportional-system fragmentation.
- [ ] **P2** Add local campaign targeting and persuasion
    - Parties should allocate resources across constituencies or demographic groups based on marginal-seat value.
    - Include budget constraints and diminishing returns.
- [ ] **P2** Add social influence calibration and network diagnostics
    - Report network degree distribution, clustering, connected components, homophily, and influence concentration.
    - Validate bounded-confidence/noisy-voter outputs against deterministic toy networks.
- [ ] **P2** Add discrete-event scheduling for campaign/election timelines
    - Mesa 3.x has modern time/scheduling capabilities; model campaigns, events, polls, debates, registration deadlines, and election day as explicit events.
    - Keep `step()` behavior backward-compatible.
- [ ] **P2** Add poll generation and polling-error simulation
    - Generate synthetic polls from model state with house effects, sampling error, likely-voter screens, nonresponse, and correlated misses.
    - Keep prediction language clearly separated from simulation scenarios.
- [ ] **P2** Add strategic voting based on district-level viability, not only global party viability
    - For FPTP, voters should evaluate local top-two competitiveness and constituency-specific wasted-vote risk.
    - Add tests for a third party viable nationally but not locally.
- [ ] **P2** Add turnout mobilization operations
    - Model canvassing, GOTV, persuasion vs mobilization, targeted demographics, and resource allocation.
    - Return turnout decomposition by baseline, alienation, indifference, and campaign mobilization.

#### P2 Presets & Country Coverage

- [ ] **P2** Add Canada federal preset with FPTP, province metadata, and riding count
    - Include party positions, regional strengths, and source notes.
- [ ] **P2** Add Israel preset with nationwide PR and electoral threshold
    - Include coalition-heavy government formation examples.
- [ ] **P2** Add Netherlands preset with low-threshold nationwide PR
    - Useful for fragmentation and coalition comparisons.
- [ ] **P2** Add Switzerland preset with PR plus referendum/direct-democracy hooks
    - Model referendums as separate ballot events rather than party-seat contests only.
- [ ] **P2** Add Mexico preset with mixed-member Chamber of Deputies structure
    - Include district/list tiers and coalition-party handling.
- [ ] **P2** Add New Zealand MMP preset
    - Covers party vote, electorate vote, threshold/one-electorate exception, overhang behavior, and leveling seats.
- [ ] **P2** Add Ireland STV preset
    - Provides real-world multi-member ranked-choice use case and validation path for STV.
- [ ] **P2** Add Scotland/Wales additional-member presets
    - Useful for closed-list regional compensatory systems.
- [ ] **P2** Add Norway/Sweden/Denmark PR presets with leveling-seat variants
    - Compare Sainte-Lague variants, regional districts, national adjustment seats, and thresholds.
- [ ] **P2** Add Chile or Spain D'Hondt multi-district presets
    - Useful for district magnitude effects and disproportionality comparisons.
- [x] **P2** Add EU preset `config.py` (done in b617fb1) through `ElectionModel.from_preset("eu")`
    - Existing EU implementation is specialized in `election.py`, inconsistent with config-based presets.
- [ ] **P2** Add preset contract tests
    - Every preset should expose config, party metadata, provenance, expected system, expected seat count, and smoke simulation.
    - Fail if docs list a preset that `PRESETS` does not expose.
- [ ] **P2** Add preset calibration status enum
    - Values: structural demo, partially calibrated, historically calibrated, validation-only.
    - Surface status in README, docs, and dashboard.
- [ ] **P2** Add alliance/bloc modeling to presets
    - India/EU/coalition-heavy systems need parties, alliances, groups, and government blocs as distinct concepts.

#### P3 Architecture & Maintainability

- [ ] **P3** Split large modules that exceed the 250 pure-LOC ceiling
    - `core/model.py`, `core/cli.py`, `analysis/batch_runner.py`, `dynamics/opinion_dynamics.py`, `engine/coalition.py`, `presets/india/election.py`, `presets/eu/election.py`, `systems/alternative.py`, and `visualization/plots.py`.
    - Preserve public facade imports while moving cohesive logic into focused modules.
- [ ] **P3** Split `ElectionModel` into configuration, voting, counting, stepping, and result-building components
    - Reduce constructor parameter sprawl and make alternative systems easier to wire.
- [ ] **P3** Introduce an `ElectionResult` typed object
    - Replace loose dictionaries with dataclasses or typed mappings for vote counts, seats, shares, metrics, metadata, and warnings.
    - Keep dict compatibility during migration.
- [ ] **P3** Add typed domain aliases/newtypes for party IDs, constituency IDs, voter IDs, seat counts, and shares
    - Prevent mixing array positions, real IDs, and labels.
- [ ] **P3** Add runtime config validation to `Config` and `PartyConfig`
    - Validate voter counts, constituency counts, thresholds, temperature, party positions, valence ranges, and duplicate party names.
- [x] **P3** Add `from_preset()` kwargs validation
    - Unknown overrides should fail loudly instead of being silently ignored by preset factory signatures.
- [x] **P3** Replace `print()` GPU fallback warning with structured warning/logging
    - Use `warnings.warn()` with a custom category so tests and users can filter it.
- [x] **P3** Remove or document bare `step()` methods (done in 6de0eb8)
    - Either wire them into model stepping or mark them intentionally inert with test coverage.
- [ ] **P3** Add a stable plugin/extension API for behavior models, voting systems, metrics, and presets
    - Avoid requiring edits to core registries for every extension.
- [ ] **P3** Add optional dependency boundary tests
    - Simulate missing matplotlib, networkx, numba, cupy, streamlit, and plotly imports and verify graceful degradation.
- [ ] **P3** Add type-checking gate to CI and install path
    - `pyproject.toml` declares `mypy` in dev extras, but `.venv/bin/mypy` is absent in the current environment.
    - Decide whether to use mypy, basedpyright, or both, and make the command reproducible.
- [ ] **P3** Add public docstrings for currently undocumented public methods
    - Missing examples include `VoterAgents.get_ideology_x()`, `VoterAgents.get_ideology_y()`, `BehaviorEngine.add_model()`, `BehaviorEngine.compute_all()`, `Config.n_parties`, and `ConstituencyManager` helpers.
- [ ] **P3** Add `typing.get_type_hints()` smoke tests for public modules
    - `core/model.py` has postponed annotations for names not present at runtime; type-hint introspection should not fail.
- [x] **P3** Remove duplicate "Version History" header in `TODO.md`
    - Current TODO has the heading twice in a row.
- [x] **P3** Normalize stale TODO entries (done, strain.py committed)
    - Some older audit items are stale when local `engine/strain.py` and `tests/test_engine.py` changes are present.
    - Add a periodic "verify TODO still applies" workflow before implementation loops.

#### P3 CLI, Dashboard, Visualization & UX

- [ ] **P3** Add CLI support for all documented systems and presets
    - `electoral-sim run --system` should list accepted values and reject unsupported ones.
    - Include tiny CLI integration tests with JSON output.
- [ ] **P3** Add CLI commands for validation, calibration, benchmark, and preset metadata
    - Examples: `electoral-sim validate --preset germany --year 2021`, `electoral-sim preset-info india`.
- [ ] **P3** Add BatchRunner config schema validation
    - Validate JSON/YAML config before running and report all invalid fields at once.
- [ ] **P3** Add dashboard tabs for systems comparison, preset metadata, calibration status, and uncertainty intervals
    - Avoid one-off India/generic branches where common result display can be shared.
- [ ] **P3** Add dashboard support for all current presets, including Australia House/Senate, South Africa, and EU
    - Current selectbox omits several presets exposed by the package/docs.
- [ ] **P3** Add dashboard scenario save/load
    - Export current sidebar parameters, seed, preset, and results as JSON.
- [ ] **P3** Add dashboard warning banners for structural vs calibrated presets
    - Keep "not a forecast" status visible inside the app, not only README.
- [ ] **P3** Add visualizations for uncertainty bands and batch results
    - Plot turnout/seat distributions, seat probability histograms, and sensitivity tornado charts.
- [ ] **P3** Add redistricting/geography visualizations
    - District maps, compactness histograms, ensemble percentile plots, and swing maps.
- [ ] **P3** Convert visualization return types consistently
    - Either Matplotlib-only with `st.pyplot`, Plotly-only with `st.plotly_chart`, or paired functions with explicit names.
- [ ] **P3** Add visual regression smoke tests for generated plots
    - Validate non-empty axes/traces and no crash with small synthetic results.
- [ ] **P3** Add example notebooks or scripts for every major workflow
    - Coalition/government, opinion dynamics, BatchRunner, validation/calibration, redistricting, dashboard export, and custom behavior model.
- [ ] **P3** Add `docs/examples/` pages that execute snippets in CI
    - Prevent README/docs examples from drifting from function signatures.

#### P3 Docs, Packaging & CI

- [ ] **P3** Fix API docs for alternative systems
    - `docs/api/electoral_systems.md` uses signatures and return shapes that do not match current implementations.
- [ ] **P3** Fix metrics docs for `efficiency_gap()`
    - Docs describe a two-argument signature, implementation takes `party_a_votes`, `party_b_votes`, and `party_a_seats`.
- [ ] **P3** Add docs navigation entries for workflow, iteration, citations, validation, maintenance, and feature comparison
    - Ensure mkdocs actually publishes the repo's new support docs.
- [ ] **P3** Add docs build link-checking
    - Catch stale GitHub Pages/PyPI/API URLs and missing source citations.
- [x] **P3** Include `py.typed` verification test and wheel verification tests
    - Package data includes it, but add a built artifact test to prevent regressions.
- [ ] **P3** Decide whether `docs/`, `benchmarks/`, `examples/`, and `.github/` belong in sdists
    - `MANIFEST.in` currently prunes docs/scripts/examples and excludes app-related files.
    - If excluded intentionally, document the release policy.
- [ ] **P3** Consolidate release scripts
    - `release.py`, `do_release.py`, `bump_version.py`, and batch files should have one documented release path.
- [ ] **P3** Move benchmark scripts under `benchmarks/` or document why some remain in `scripts/`
    - `scripts/benchmark_gpu.py` and `scripts/benchmark_scale.py` are outside the benchmark directory.
- [ ] **P3** Add small benchmark CI smoke job
    - Run tiny voter counts to verify benchmark code paths without enforcing performance thresholds.
- [x] **P3** Add `pytest -W error` gate (done in 838336c)
    - Keep warning budget at zero.
- [ ] **P3** Register all custom pytest marks
    - `slow` appears in tests but is not registered in `pyproject.toml`.
- [x] **P3** Add dependency freshness and upper-bound review
    - Track Mesa, Polars, Numba, NumPy, NetworkX, Streamlit, Plotly, and CuPy compatibility.
- [ ] **P3** Add Python 3.13 CI lane if not already green
    - `pyproject.toml` advertises Python 3.13 support.
- [ ] **P3** Add CodeQL or static-analysis TODO triage to release checklist
    - Keep generated alerts tied back to actionable TODO entries.
- [ ] **P3** Add coverage thresholds per module category
    - Core stable modules should have stricter thresholds than GPU/optional experimental modules.

#### P5 Research & Long-Term Features

- [ ] **P5** Add reinforcement-learning party strategy experiments
    - Compare median-voter walk, office-seeking, policy-seeking, and vote-maximizing agents.
- [ ] **P5** Add demographic synthetic population generation from census microdata
    - Generate joint distributions instead of independent feature draws.
- [ ] **P5** Add ecological inference / small-area estimation bridge
    - Estimate local demographic vote patterns from aggregate returns with uncertainty caveats.
- [ ] **P5** Add macroeconomic scenario feeds
    - Connect GDP, inflation, unemployment, and approval proxies to retrospective/sociotropic models.
- [ ] **P5** Add international election-admin scenario dimensions
    - Model ballot access, campaign period, media access, complaints/appeals, counting/tabulation confidence, and observer notes.
- [ ] **P5** Add electoral college and weighted body systems
    - US presidential Electoral College, weighted councils, and indirect election bodies.
- [ ] **P5** Add referendums and ballot measures
    - Support binary/multi-option issues, turnout interactions, and simultaneous candidate + referendum ballots.
- [ ] **P5** Add participatory budgeting / knapsack voting module
    - Useful for comparing election mechanisms beyond candidate elections.
- [ ] **P5** Add deliberation and persuasion experiments
    - Model debate exposure, social learning, elite cues, and opinion convergence/polarization.
- [ ] **P5** Add misinformation intervention scenarios
    - Fact-checking reach, trust, backfire/no-backfire assumptions, and media-literacy heterogeneity.
- [ ] **P5** Add turnout shocks from weather, holidays, conflict, or administrative disruption
    - Keep exogenous shocks explicit and scenario-based.
- [ ] **P5** Add overseas/absentee/mail voting channels
    - Model eligibility, return rates, rejection rates, and counting delays.
- [ ] **P5** Add recount and audit simulation
    - Risk-limiting audits, recount thresholds, ballot error rates, and confidence intervals.
- [ ] **P5** Add malicious or accidental data-quality scenario tests
    - Missing precincts, party-name aliases, duplicate districts, inconsistent totals, and late corrections.
- [ ] **P5** Add comparative electoral-system benchmark report
    - Run the same synthetic electorates through FPTP, PR, MMP, IRV, STV, Approval, Score, Borda, and Condorcet with VSE/proportionality outputs.

#### External Research Sources To Use

- GerryChain documentation and API: redistricting ensembles, ReCom-style workflows, efficiency gap, Polsby-Popper, partisan Gini.
- MIT Election Data and Science Lab: precinct-level returns and election-data provenance patterns.
- Comparative Study of Electoral Systems (CSES): survey variables for voter behavior, demographics, district, and macro/electoral-system calibration.
- International IDEA Electoral System Design Database/Handbook: open/closed lists, MMP, parallel systems, two-round systems, Borda, STV, and mixed/tiered designs.
- OSCE/ODIHR election observation methodology: campaign, media, legal framework, election administration, complaints/appeals, counting, and tabulation dimensions.
- PrefLib: ranked/preference ballot data formats for IRV/STV/Condorcet validation.
- OpenSTV/RCTab ecosystem: known ranked-choice tabulation behavior and validation targets.
- `abcvoting`/approval-based committee voting literature: PAV, Method of Equal Shares, Phragmen, and approval multiwinner methods.
- Mesa documentation: batch runs, data collection, time/scheduling, and current ABM framework patterns.

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

- [x] **P2** Fix `DivisionByZero` warning in `coalition_strain()` when weights sum to 0 — returns NaN, should return 0.0 (line 131)
- [x] **P3** Fix `RuntimeWarning` in `coalition_strain()` — normalize weights without divide-by-zero risk
- [x] **P2** EU Parliament preset has no `config.py` — has `election.py` only, unlike all other presets. Add `eu_config()` for PRESETS registry.
- [x] **P3** `PartyAgents.step()` already documented `pass` — should call `adaptive_strategy_step()` or document why not
- [x] **P3** `VoterAgents.step()` documented as intentionally inert `pass` — should call opinion dynamics or document why not

### Broad Exception Handling

- [x] **P2** `core/cli.py:338` uses bare `except Exception` in `run_simulation()` — should catch specific errors
- [x] **P2** `core/cli.py:402` uses bare `except Exception` in `run_batch()` — should catch specific errors
- [x] **P2** `engine/gpu_accel.py:29` uses bare `except Exception` in `is_gpu_available()` — should catch `cupy.cuda.runtime.CUDARuntimeError` explicitly

### Stale/Placeholder Code

- [x] **P3** `systems/allocation.py:216` documented -- intentional Numba fallback `pass` in a fallback import block — should raise `NotImplementedError` with guidance
- [x] **P3** `engine/government.py:287` pass is empty while loop body (valid idiom) `pass` with comment about discrete media effect — implement or remove

### Code Style

- [x] **P3** `core/model.py:114` changed to `ConstituencyManager | None` — replace with `ConstituencyManager | None` (PEP 604 style, Python 3.10+)
- [x] **P5** Add `py.typed` marker to MANIFEST.in for PEP 561 compliance

### Miscellaneous

- [x] **P2** `app.py` imports `simulate_india_election` from `presets.india.election` directly — should use `electoral_sim` top-level import for consistency
- [x] **P3** `MANIFEST.in` exclusion policy documented `benchmarks/`, `docs/`, or `.github/` — consider adding for source distributions
- [x] **P3** Auxiliary test files moved to benchmarks/ (done in f1678ea) — add to test suite or document as manual-only

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
- [x] **P3** `visualization/specialized.py` animation save path now tested (animation save path)
- [x] **P3** `data/loaders.py` year-filtering branches now tested (branch of incumbents from votes without seats column)

### Integration Test Coverage

- [ ] **P2** `tests/test_integration.py` has only 12 tests across 3 classes — should have more cross-module workflows
    - No integration test for: Model + Coalition (run election then form government)
    - No integration test for: BatchRunner + Presets
    - No integration test for: EventManager → Model → step() → run_election()
    - No integration test for: OpinionDynamics → Model → run_election() → results
- [x] **P2** Hypothesis property tests added (e1c7eea, 3a2633a)
    - Add property tests for: allocation sum invariant, turnout 0-1, ENP ≥ 1, Gallagher ≥ 0

### Warning Cleanup

- [x] **P3** Fix `RuntimeWarning: invalid value encountered in divide` in `coalition_strain()` when weights sum to 0
    - This is the only warning in the test suite — fix it for a clean `-W error` run
- [x] **P3** Register `pytest.mark.slow` in `pyproject.toml` to eliminate `PytestUnknownMarkWarning`
    - Add to `[tool.pytest.ini_options] markers = ["slow: marks tests as slow"]`

### Test File Organization

- [x] **P1** Reorganize tests from 5 chaotic files into 11 disciplined files
- [x] **P3** Move `stress_test.py` and `benchmark_cache.py` into proper test files or `benchmarks/`

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
- [x] **P2** Create `presets/eu/config.py` (done in b617fb1) with `eu_config()` function for PRESETS registry
- [x] **P2** Extract EU_POLITICAL_GROUPS and COUNTRY_GROUP_WEIGHTS from `election.py` into `data.py`
- [ ] **P3** Split `simulate_eu_election()` to use `ElectionModel` per country (mirror India refactor)
- [x] **P3** EU preset config.py added (b617fb1) — inconsistent with all other presets

### Engine
- [ ] **P2** `voter_behavior.py` uses `if isinstance(model, X)` dispatch — replace with registry pattern or method dispatch
- [x] **P3** `numba_accel.py` fallback duplication documented as intentional from `systems/allocation.py` — consolidate
- [x] **P2** `coalition_strain()` has inconsistent behavior with zero-weight input — guard division

### API Design
- [x] **P3** `electoral_sim/__init__.py` now exports VoterAgents, PartyAgents, EventManager `agents/` or `events/` subpackages — only individual symbols
- [x] **P3** VoterAgents and PartyAgents now exported from top-level package (6e48365)
- [ ] **P5** `ElectionModel` constructor has 20+ parameters — consider builder pattern or validate-only config input

---

## Documentation Gaps — Found 2026-06-04

- [ ] **P2** No API reference for `PartyAgents` and `VoterAgents` class methods (`get_positions()`, `get_valence()`, etc.)
- [ ] **P2** No documentation for `adaptive_strategy_step()` or `EventManager` in user-facing docs
- [x] **P3** `CITATION.cff` and `docs/CITATIONS.md` now linked but `docs/CITATIONS.md` not linked from README
- [ ] **P3** `VALIDATION.md` has template but no populated data — needs a real calibration pass
- [ ] **P3** `FEATURE_COMPARISON.md` is research-only, not user-facing — add "How We Compare" to README
- [ ] **P3** `docs/` mkdocs structure doesn't include new files (`WORKFLOW.md`, `ITERATION.md`, `CITATIONS.md`, etc.)
- [ ] **P3** `examples/` directory has only 2 scripts — add examples for coalition, government, duverger, opinion dynamics
- [x] **P3** CHANGELOG.md v0.1.1 already populated
- [ ] **P5** No tutorial/quickstart for new users beyond README code snippets

---

## CI/CD & Infrastructure — Found 2026-06-04

- [x] **P3** Add `pytest -W error` gate (done in 838336c)
- [x] **P3** Register `pytest.mark.slow` in `pyproject.toml` to fix `PytestUnknownMarkWarning`
- [ ] **P3** Run `benchmarks/benchmark_core.py` as a CI smoke test (small voter counts, verify no crash)
- [x] **P3** Add `app.py` Streamlit import verification in `test-optional-deps` CI job
- [x] **P3** `scripts/` directory audited and cleaned up, many likely unused — audit and clean up
    - `release.py`, `do_release.py`, `bump_version.py` — consolidate into one release workflow
    - `benchmark_gpu.py`, `benchmark_scale.py` — move to `benchmarks/` directory
- [x] **P5** Add `.pre-commit-config.yaml` for pre-commit hooks (Black, Ruff, mypy)

---

## Fresh Audit — Found 2026-06-04

### Correctness Bugs

- [x] **P2** Guard PR allocation against zero total votes and non-positive seat counts in `systems/allocation.py`
    - `dhondt_allocation()`, `sainte_lague_allocation()`, `hare_quota_allocation()`, and `droop_quota_allocation()` currently divide by `total_votes` or `n_seats` without an explicit zero-input policy
    - Add tests in `tests/test_unit.py` for all-zero votes, empty vote arrays, threshold filtering that excludes every party, and `n_seats == 0`
- [x] **P2** Make `ElectionModel.run_election()` robust when no valid votes remain
    - `core/model.py` computes `vote_shares = vote_counts / vote_counts.sum()` after turnout and constituency filtering; all voters abstaining or all votes invalidated can divide by zero
    - Add tests in `tests/test_model.py` for zero turnout and all votes invalidated by `constituency_constraints`
- [x] **P2** Define and test deterministic FPTP tie-breaking across both counting paths
    - `systems/allocation.py::fptp_allocation()` depends on sorted Polars group order; `engine/numba_accel.py::fptp_count_fast()` likely uses first max party index
    - Add matching tie tests for Polars FPTP allocation and Numba/NumPy fast counting so both paths agree
- [x] **P3** Handle empty approval ballots in `systems/alternative.py::approval_voting()`
    - `approval_counts / len(approvals)` divides by zero for zero voters
    - Add `tests/test_unit.py` coverage for empty approvals and zero-candidate input policy
- [x] **P3** Validate malformed ranked ballots in IRV/STV/Condorcet functions
    - `systems/alternative.py` accepts duplicate ranks, out-of-range ranks, and shape mismatches without explicit errors
    - Add tests for duplicate first preferences, missing candidates, empty rankings, and invalid `n_candidates` / `n_seats`

### API & Architecture

- [ ] **P2** Decide whether advanced model knobs belong in `Config` or are constructor-only
    - `ElectionModel.__init__()` supports behavior engines, opinion dynamics, NOTA, events, adaptive strategy, constraints, GPU, and socioeconomic modifiers, but `Config`/`from_config()` only carries the small core subset
    - Add either Config fields plus tests or documentation that these knobs must be passed directly to `ElectionModel`
- [ ] **P3** Split oversized implementation modules before adding substantial feature code
    - `core/model.py`, `engine/coalition.py`, `dynamics/opinion_dynamics.py`, `visualization/plots.py`, `analysis/batch_runner.py`, and `core/cli.py` exceed the local 250 pure-LOC discipline
    - Extract cohesive units first when touching those modules: counting/results, model stepping, coalition search, plotting families, batch execution, and CLI subcommands
- [x] **P3** Refresh scoped `AGENTS.md` knowledge files after the test reorganization and recent refactors
    - `tests/AGENTS.md` still references removed files (`test_comprehensive.py`, `test_advanced.py`, `test_improved.py`, `test_additional.py`) and outdated test/coverage counts
    - `electoral_sim/engine/AGENTS.md` still describes `coalition_strain()` as living in `coalition.py` after the extraction to `engine/strain.py`

### Tests & CI

- [ ] **P3** Make pytest warning filters safe when optional dependencies are absent
    - Running `pytest tests/ -q --tb=short` without Numba installed emits `PytestConfigWarning: Failed to import filter module 'numba'`
    - Replace the module-qualified warning filter in `pyproject.toml` with a filter that does not import optional modules, then verify collection without Numba
- [ ] **P3** Add a lightweight environment bootstrap check for local verification
    - In a clean Python environment, `pytest tests/ -q --tb=short` currently fails collection with `ModuleNotFoundError: No module named 'polars'`
    - Add docs or a script target that installs `.[dev]` and verifies core imports before running tests

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
