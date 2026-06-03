# Tests — ElectoralSim

## OVERVIEW

10 test files, ~222 tests, ~70% coverage. pytest with `-v --tb=short`, Hypothesis property-based testing, numpy array comparisons. Warnings: `DeprecationWarning`, `FutureWarning`, `NumbaDeprecationWarning` silenced.

## FILES

| File | Focus |
|------|-------|
| `test_unit.py` | FPTP, PR allocation, IRV, STV, approval, Condorcet — Hypothesis property tests, numpy comparisons |
| `test_integration.py` | Cross-module integration flows |
| `test_smoke.py` | Basic imports, model creation |
| `test_comprehensive.py` | Full system coverage |
| `test_advanced.py` | Advanced feature validation |
| `test_improved.py` | Coverage gap filling |
| `test_additional.py` | Supplementary edge cases |
| `test_batch_runner.py` | Batch parameter sweep tests |
| `benchmark_cache.py` | Timing/performance benchmarks (standalone) |
| `stress_test.py` | Large-scale stress tests (standalone) |

## RUNNING

```bash
pytest tests/ -v              # All tests
pytest tests/test_unit.py -v  # Single file
pytest tests/ --cov           # With coverage
python tests/stress_test.py   # Stress/benchmark (standalone)
```

## PATTERNS

- **Imports**: `from electoral_sim.<module>.<submodule> import <Symbol>` — direct, no internal test helpers
- **Hypothesis**: `@given` decorators for random vote distributions, allocation inputs, edge cases
- **Numpy**: `np.array_equal()` / `np.allclose()` for vectorized seat or index comparisons
- **Parametrize**: `@pytest.mark.parametrize` across systems, presets, allocation methods
- **Standalone scripts**: `benchmark_cache.py` and `stress_test.py` run via `python`, not pytest

## COVERAGE

~70% across 222 tests. Covers all electoral systems, 11 presets, coalition logic, opinion dynamics, and acceleration paths. Source measurement in `electoral_sim/`; `tests/` excluded from coverage.
