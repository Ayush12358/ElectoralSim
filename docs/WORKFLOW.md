# ElectoralSim Feature Implementation Workflow

> Step-by-step agent workflow for implementing features, fixes, and enhancements.

---

## Phase 1: Intake & Research

### 1.1 Parse the Request
- [ ] Identify the **feature type**: new module, new function, bug fix, refactor, test, docs
- [ ] Identify the **scope**: single file, single module, cross-module, project-wide
- [ ] Identify **constraints**: backward compatibility, performance, API stability

### 1.2 Map Affected Files
Use this lookup to find where the work lives:

| Feature Type | Primary File(s) | Test File(s) |
|-------------|-----------------|--------------|
| New voting system | `systems/allocation.py` or `systems/alternative.py` | `tests/test_engine.py` |
| New behavior model | `behavior/voter_behavior.py` | `tests/test_behavior.py` |
| New country preset | `presets/<country>/config.py` + `__init__.py` | `tests/test_presets.py` |
| ElectionModel change | `core/model.py` | `tests/test_model.py` |
| Coalition/government | `engine/coalition.py` or `engine/government.py` | `tests/test_engine.py` |
| Opinion dynamics | `dynamics/opinion_dynamics.py` | `tests/test_dynamics.py` |
| Metrics | `metrics/indices.py` | `tests/test_metrics.py` |
| Events | `events/event_manager.py` | `tests/test_infra.py` |
| CLI | `core/cli.py` | `tests/test_infra.py` |
| Visualization | `visualization/plots.py` or `visualization/specialized.py` | `tests/test_infra.py` |
| Batch analysis | `analysis/batch_runner.py` | `tests/test_batch_runner.py` |
| Cross-module | Multiple files | `tests/test_integration.py` |

### 1.3 Read Existing Code
- [ ] Read the target module(s) fully
- [ ] Read the corresponding test file
- [ ] Check `AGENTS.md` for conventions and anti-patterns
- [ ] Check `TODO.md` for related items
- [ ] Search for similar existing implementations (grep for function names, patterns)

---

## Phase 2: Plan

### 2.1 Design the Implementation
- [ ] Define the **public API** (function signatures, class interfaces)
- [ ] Define **inputs/outputs** (types, shapes, ranges)
- [ ] Identify **edge cases** (empty input, single party, zero voters, etc.)
- [ ] Identify **dependencies** (what existing code to call, what to avoid)
- [ ] Plan **backward compatibility** (new params should have defaults)

### 2.2 Plan the Tests
- [ ] List **happy path** tests (basic functionality)
- [ ] List **edge case** tests (boundary conditions)
- [ ] List **integration** tests (cross-module interactions)
- [ ] Identify which test file the tests go in (see mapping above)

### 2.3 Estimate Coverage Impact
- [ ] Check current coverage: `pytest tests/ --cov=electoral_sim --cov-report=term`
- [ ] Identify which lines the new code will cover
- [ ] Estimate if the change moves the needle

---

## Phase 3: Implement

### 3.1 Write the Code
Follow these conventions:

```python
# Module docstring
"""
Brief description of what this module does.

Implements:
- Feature 1
- Feature 2
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import numpy as np
import polars as pl

if TYPE_CHECKING:
    from electoral_sim.core.model import ElectionModel


def new_function(
    param1: np.ndarray,
    param2: int = 10,
    threshold: float = 0.0,
) -> dict:
    """
    Short description.

    Args:
        param1: Description with shape
        param2: Description with default
        threshold: Description with range

    Returns:
        Dictionary with keys: ...

    Example:
        >>> result = new_function(np.array([1, 2, 3]), param2=5)
        >>> result["seats"].sum()
        5
    """
    # Implementation
    ...
```

**Rules:**
- Type hints on all parameters and return values
- NumPy-style docstrings on all public functions/classes
- `from __future__ import annotations` at top of module
- Polars DataFrames for tabular data (never pandas)
- NumPy arrays for numeric computation
- Numba JIT for hot loops (with pure NumPy fallback)
- 100-char line length (Black formatter)

### 3.2 Wire into the System
- [ ] If new module: add exports to module `__init__.py`
- [ ] If new public API: add to `electoral_sim/__init__.py` under appropriate section (STABLE or BETA)
- [ ] If new preset: add to `PRESETS` dict in `core/config.py`
- [ ] If new behavior model: ensure `BehaviorEngine.compute_all()` dispatches to it
- [ ] If new allocation method: add to `ALLOCATION_METHODS` registry in `systems/allocation.py`

### 3.3 Format and Lint
```bash
black electoral_sim/ tests/
ruff check electoral_sim/ tests/
```

---

## Phase 4: Test

### 4.1 Write Tests
Place tests in the correct file per the mapping table. Follow this pattern:

```python
class TestNewFeature:
    """Tests for the new feature."""

    def test_basic_functionality(self):
        """Happy path test."""
        from electoral_sim.module import new_function

        result = new_function(np.array([1, 2, 3]))
        assert result is not None
        assert "expected_key" in result

    def test_edge_case_empty(self):
        """Edge case: empty input."""
        from electoral_sim.module import new_function

        result = new_function(np.array([]))
        assert result is not None

    def test_edge_case_single(self):
        """Edge case: single element."""
        from electoral_sim.module import new_function

        result = new_function(np.array([42]))
        assert result["count"] == 1

    def test_integration_with_model(self):
        """Integration: works with ElectionModel."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=500, seed=42)
        # ... exercise the new feature through the model
        results = model.run_election()
        assert results is not None
```

**Rules:**
- Import inside test functions (not at module top) for isolation
- Use `pytest.importorskip()` for optional dependencies
- Use `pytest.mark.parametrize` for systematic variations
- Use `tmp_path` fixture for file I/O tests
- Use `capsys` fixture for stdout testing

### 4.2 Run Tests
```bash
# Full suite
pytest tests/ -q --tb=short

# Just the affected file
pytest tests/test_<module>.py -v --tb=short

# With coverage
pytest tests/ --cov=electoral_sim --cov-report=term-missing --tb=no -q
```

### 4.3 Verify Coverage
- [ ] Run coverage and check the affected module's percentage
- [ ] If new code has uncovered branches, add tests for them
- [ ] Target: each module should be ≥80% (except Numba JIT and GPU code)

---

## Phase 5: Document

### 5.1 Update TODO.md
- [ ] Check off any related items
- [ ] Add new items if the feature has follow-up work

### 5.2 Update Docstrings
- [ ] All new public functions have NumPy-style docstrings
- [ ] All new classes have class-level docstrings with examples
- [ ] Module docstring updated if new functionality added

### 5.3 Update README (if user-facing)
- [ ] Add to feature list if significant
- [ ] Update Feature Status table (Stable/Beta/Experimental)
- [ ] Add to Quick Start if it's a common use case
- [ ] Update Limitations if the feature has known constraints

### 5.4 Update AGENTS.md (if architectural)
- [ ] Add to "Where to Look" table if new module/path
- [ ] Update conventions if new patterns introduced

---

## Phase 6: Verify & Commit

### 6.1 Final Checks
```bash
# All tests pass
pytest tests/ -q --tb=short

# No lint errors
ruff check electoral_sim/ tests/

# Formatting is correct
black --check electoral_sim/ tests/

# Coverage meets target
pytest tests/ --cov=electoral_sim --cov-report=term --tb=no -q
```

### 6.2 Commit
```bash
git add -A
git commit -m "feat: <short description>

<bullet points of what changed>

Tests: <N> passed, 0 failed
Coverage: <old>% → <new>%"
```

### 6.3 Push
```bash
git push
```

---

## Quick Reference: Adding a New Country Preset

1. Create `electoral_sim/presets/<country>/config.py`:
   - Define `<country>_config()` function returning `Config`
   - Define `<COUNTRY>_PARTIES` dict
   - Add data provenance docstring and parameter rationale

2. Create `electoral_sim/presets/<country>/__init__.py`:
   - Re-export config function and parties dict

3. Register in `electoral_sim/core/config.py`:
   - Import the config function
   - Add to `PRESETS` dict

4. Add tests in `tests/test_presets.py`:
   - Test config loads
   - Test preset runs with `ElectionModel.from_preset()`
   - Test structure (correct number of parties, electoral system, etc.)

---

## Quick Reference: Adding a New Behavior Model

1. Create class in `electoral_sim/behavior/voter_behavior.py`:
   - Implement `compute_utility()` method
   - Follow `BehaviorModel` protocol

2. Wire into `BehaviorEngine.compute_all()`:
   - Add `isinstance` check and dispatch

3. Add tests in `tests/test_behavior.py`:
   - Test creation, utility shape, edge cases
   - Test integration with `BehaviorEngine`

4. Export from `electoral_sim/__init__.py` under BETA section

---

## Quick Reference: Adding a New Metric

1. Add function to `electoral_sim/metrics/indices.py`:
   - Pure function: takes arrays, returns float
   - Handle edge cases (zero division, empty input)

2. Add tests in `tests/test_metrics.py`:
   - Test with known values
   - Test edge cases
   - Test integration (compute from election results)

3. Export from `electoral_sim/__init__.py` under STABLE section
