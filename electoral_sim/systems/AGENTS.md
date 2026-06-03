# electoral_sim/systems/ Knowledge Base

**Generated:** 2026-05-29
**Commit:** 62c3d05
**Branch:** master

## Overview

Seat allocation algorithms and alternative voting methods. Pure NumPy implementations with optional Numba JIT fallback. All PR allocation functions share the same signature. FPTP is the outlier (takes a Polars DataFrame).

## Files

| File | Lines | Contents |
|------|-------|----------|
| `allocation.py` | 222 | 5 allocators + `allocate_seats()` dispatcher + `ALLOCATION_METHODS` registry |
| `alternative.py` | 355 | IRV, STV, approval, condorcet, ranking generator |

## Signatures

**PR allocation** (4 functions) share this exact signature:

```python
def dhondt_allocation(votes: np.ndarray, n_seats: int, threshold: float = 0.0) -> np.ndarray
```

Same for: `sainte_lague_allocation`, `hare_quota_allocation`, `droop_quota_allocation`. All normalize via `votes.astype(float)` on entry. Threshold is a vote share (0-1), not a raw count.

**FPTP** is different:

```python
def fptp_allocation(votes_by_constituency: pl.DataFrame, n_constituencies: int) -> np.ndarray
```

Expects a DataFrame with `[constituency, party, votes]` columns.

## Registering a New Allocator

1. Write a function matching the PR signature in `allocation.py`
2. Add it to `ALLOCATION_METHODS` dict (line ~181)
3. Export from `__init__.py` (add to import + `__all__`)
4. That's it. `allocate_seats()` dispatches via the dict.

## Anti-Patterns

- **Passing Python lists to allocators.** The `votes` param is `np.ndarray`. Call `np.array(lst)` first. The functions call `.astype(float)`, which silently no-ops on arrays but errors on bare lists.
- **Ignoring the threshold param.** It's a fraction (0.05 = 5%), not a raw vote count. Applying your own pre-filter AND passing threshold double-filters.
- **Mutating the returned seats array.** The caller owns it, but treat it as read-only to avoid bizarre bugs downstream.
