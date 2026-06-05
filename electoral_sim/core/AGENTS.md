# core/ — Simulation Orchestration

## OVERVIEW

Central module: model creation, configuration, vote counting, CLI, and voter generation. Everything flows through `ElectionModel`.

## FILES

| File | Lines | Purpose |
|------|-------|---------|
| `model.py` | 1000 | `ElectionModel(Model)` — chainable entry point; `ElectionResult` dataclass |
| `config.py` | 233 | `Config` / `PartyConfig` dataclasses, `PRESETS` registry, `CalibrationStatus` enum |
| `cli.py` | 247 | `main()` — run, batch, list-presets subcommands; handlers in `_cli_commands.py` |
| `voter_generation.py` | 77 | `generate_party_frame()`; voter generation in `_voter_gen.py` (232 lines) |
| `_provenance.py` | 142 | `PRESET_PROVENANCE` dict — calibration status, source metadata per preset |
| `_cli_commands.py` | 233 | `run_simulation()`, `run_batch()`, `list_presets()`, `preset_info()`, `validate_preset()` |
| `_voter_gen.py` | 232 | `generate_voter_frame()` — demographics, ideology, Big Five, Moral Foundations |
| `counting.py` | 78 | `count_fptp()`, `count_pr()` — delegates to Numba |
| `constituency.py` | 63 | `ConstituencyMetadata`, `ConstituencyManager` |
| `__init__.py` | 17 | Re-exports public API (facade pattern) |

## KEY ARCHITECTURE

- **Config drives model.** Create a `Config` dataclass, pass to `ElectionModel(config)` or use kwargs constructor. Config is frozen after model init.
- **Chainable API.** `.with_system("PR").with_allocation("sainte_lague").run_election()` — each `with_*()` sets a config field and returns `self`.
- **Two data paths.** FPTP: `count_fptp()` → `fptp_count_fast()` (Numba). PR: `count_pr()` → `allocate_seats()` from `systems.allocation`.
- **Polars for agents.** Voters stored as `pl.DataFrame` on model, not Mesa's `AgentSet`. Generated via `generate_voter_frame()` with demographics, ideology, turnout prob.
- **CLI flows.** `main()` parses args, imports `ElectionModel` lazily, runs election or batch, outputs JSON/CSV.

## CONVENTIONS (core-specific)

- `from __future__ import annotations` at top of every module.
- Numba-accelerated functions imported at module level in `model.py` and `counting.py` (not deferred).
- Config fields use `Literal` types for constrained string values (e.g., `electoral_system: Literal["FPTP", "PR"]`).
- `PartyConfig` uses `@dataclass` with defaults; `Config` uses `@dataclass` with `field(default_factory=...)` for mutable defaults.
- `rng: np.random.Generator` passed explicitly through generation functions (not global seed).
- `__init__.py` re-exports every public symbol from all submodules.

## ANTI-PATTERNS

- **Modifying Config after model creation.** Config is read once in `__init__`. Mutating it later has no effect.
- **Using non-Literal strings for `electoral_system`.** Only `"FPTP"` and `"PR"` are valid. Other values silently produce no-op counts.
- **Importing Numba functions inside hot loops.** They are already compiled; re-importing defeats purpose and adds overhead.
- **Calling `run_election()` before `with_*()` chain completes.** Order matters: chain first, then call `run_election()`.
