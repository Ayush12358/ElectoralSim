# electoral_sim/analysis

**Systematic parameter exploration, Duverger's Law experiments, and VSE calculations.**

## Files

| File | Exports | Purpose |
|------|---------|---------|
| `batch_runner.py` | `BatchRunner`, `ParameterSweep` | Grid/random parameter sweeps with multiprocessing, export to CSV/Parquet/JSON |
| `duverger.py` | `run_duverger_experiment()` | Multi-step simulation showing FPTP converges to ENP ~2 while PR stays multi-party |
| `vse.py` | `calculate_vse()` | Voter Satisfaction Efficiency: (W_actual - W_random) / (W_optimal - W_random) |

## Usage Patterns

**BatchRunner workflow:**
1. Define a `ParameterSweep(dict)` mapping param names to value lists
2. Pass it to `BatchRunner(model_class, parameter_sweep, n_runs_per_config, n_jobs)`
3. Call `.run()` to get a `pl.DataFrame`, then `.export_results(path)` or `.get_summary_stats()`

**ParameterSweep dict format:**
- Keys match `ElectionModel.__init__` kwargs (e.g. `n_voters`, `temperature`)
- `sweep_type="grid"` (default, all combinations) or `"random"` (samples from list)
- `fixed_params` dict for non-varying settings

**Duverger experiment:**
- `run_duverger_experiment(n_voters, n_parties, n_steps, system="FPTP"|"PR")`
- Returns list of step dicts with `enp`, `vote_shares`, `winner`
- Wired with `WastedVoteModel` for the psychological effect

**VSE:**
- `calculate_vse(utilities: (n_voters, n_parties), seat_shares: (n_parties,)) -> float`
- Assumes single-winner optimal; `w_random` = mean utility across parties

## Conventions

- Parallel execution via `concurrent.futures.ProcessPoolExecutor` (flat worker function, not method)
- Results stored as `pl.DataFrame` — `.write_csv()`, `.write_parquet()`, `.write_json()` for export
- Duverger experiment uses `BehaviorEngine` with `ProximityModel + WastedVoteModel`
- `ParameterSweep.generate_configs()` returns `list[dict]` — one dict per config
- All exports re-exported through `__init__.py`
