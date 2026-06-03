# engine/ Knowledge Base

**Scope:** Performance-critical compute kernels and political coalition/government logic.

## Overview

Two distinct responsibilities live here: (1) accelerated backend functions (Numba JIT, optional CuPy GPU) that hot-path vote counting, seat allocation, and utility computation, and (2) coalition formation and government stability models that sit atop election results.

## Files

| File | Lines | Purpose |
|------|-------|---------|
| `numba_accel.py` | 352 | JIT-compiled `dhondt_numba()`, `sainte_lague_numba()`, `fptp_count_numba()` (parallel), `mnl_sample_numba()`, `compute_utilities_numba()`. Wrapper functions (`fptp_count_fast`, `vote_mnl_fast`, `dhondt_fast`) decide at runtime whether to call JIT or fallback. Includes `benchmark_numba()`. |
| `gpu_accel.py` | 136 | CuPy-based GPU kernels for utility matrix and MNL sampling. `is_gpu_available()` gates usage. Raises `RuntimeError` if CuPy absent. |
| `coalition.py` | 471 | `minimum_winning_coalitions()` (exhaustive search over 2^n combinations), `minimum_connected_winning()` (ideological contiguity), `coalition_strain()`, `predict_coalition_stability()`, `form_government()`, `allocate_portfolios_laver_shepsle()`, `junior_partner_penalty()`, `form_coalition_with_utility()` (P4 policy vs office tradeoff). |
| `government.py` | 300 | `GovernmentSimulator` class with `step()`/`simulate()` lifecycle. `collapse_probability()` (sigmoid/linear/exponential models), `hazard_rate()` (bathtub curve + event weights), `cox_proportional_hazard()` (Warwick 1994 default coefficients). |

## Key Patterns

- **Numba fallback**: `try/except ImportError` at module level. If Numba is missing, a no-op `@jit` decorator returns the raw function, and `prange` aliases to `range`. Wrapper functions (`dhondt_fast`, etc.) check `NUMBA_AVAILABLE` flag to branch. Callers never import Numba directly.
- **Arrays only to JIT**: All `@jit` functions accept/return `np.ndarray` (int64/float64). No dicts, lists, or optional params.
- **Pure NumPy fallbacks** use vectorized operations (`bincount`, `argmax`, broadcasting) to avoid performance cliffs.
- **GPU gating**: `gpu_accel.py` checks presence at import time; functions raise at call time. Callers should check `is_gpu_available()` first.

## Conventions

- Numba functions get `_numba` suffix; wrapper functions get `_fast` suffix.
- Wrapper functions own the dtype casting (callers pass whatever, wrappers convert to int64/float64 for Numba).
- Coalition functions accept bare `np.ndarray` (not Polars) for seat/position vectors.
- `@jit(nopython=True, cache=True)` everywhere; use `parallel=True` + `prange` only for embarrassingly parallel loops (constituency-level FPTP, per-voter utility).
- Benchmark function in `numba_accel.py` is guarded by `if __name__ == "__main__"`.

## Anti-Patterns

- **Do not pass Python objects to Numba functions.** Lists, dicts, tuples, and `Optional` args cause compilation failure. Cast to ndarray before calling.
- **Do not import Numba in callers.** Use the `_fast` wrappers. Importing Numba directly breaks the graceful fallback contract.
- **Do not use Polars Series inside `@jit`.** Convert to `np.ndarray` first. Numba has zero Polars awareness.
- **Do not use `@jit` on functions that return variable-length structures.** Return fixed-size arrays.
- **Do not call `gpu_accel` functions without checking `is_gpu_available()`.** They raise `RuntimeError` on failure, not fall back.
