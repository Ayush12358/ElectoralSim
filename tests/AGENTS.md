# Tests — ElectoralSim

## OVERVIEW

11 test files, 349 tests, ~80% coverage. pytest with `-v --tb=short`, Hypothesis property-based testing, numpy array comparisons. Warnings: `DeprecationWarning`, `FutureWarning`, `NumbaDeprecationWarning` silenced.

## FILES

| File | Focus |
|------|-------|
| `test_unit.py` | FPTP, PR allocation, IRV, STV, approval, Condorcet — Hypothesis property tests, numpy comparisons |
| `test_model.py` | ElectionModel creation, chainable API, edge cases, error handling |
| `test_engine.py` | Coalition, government, Numba wrappers, allocation, alternative voting |
| `test_behavior.py` | Voter behavior models and BehaviorEngine |
| `test_presets.py` | Country preset loading, structure, smoke tests |
| `test_dynamics.py` | Opinion dynamics and network topologies |
| `test_metrics.py` | Electoral metrics (Gallagher, ENP, VSE, etc.) |
| `test_integration.py` | Cross-module integration flows |
| `test_infra.py` | CLI, EventManager, visualization return types |
| `test_batch_runner.py` | Batch parameter sweep tests |
| `test_smoke.py` | Basic imports, model creation |

## BENCHMARKS

Standalone performance scripts in `benchmarks/`:
| File | Focus |
|------|-------|
| `benchmark_core.py` | Core performance benchmarks |
| `benchmark_cache.py` | Timing/performance with caching |
| `stress_test.py` | Large-scale stress tests |
| `benchmark_gpu.py` | GPU acceleration benchmarks |
| `benchmark_scale.py` | Scalability benchmarks |

## RUNNING

```bash
pytest tests/ -v              # All tests (349)
pytest tests/test_unit.py -v  # Single file
pytest tests/ --cov           # With coverage
python benchmarks/stress_test.py   # Stress/benchmark (standalone)
```

## PATTERNS

- **Imports**: `from electoral_sim.<module>.<submodule> import <Symbol>` — direct, no internal test helpers
- **Hypothesis**: `@given` decorators for random vote distributions, allocation inputs, edge cases
- **Numpy**: `np.array_equal()` / `np.allclose()` for vectorized seat or index comparisons
- **Parametrize**: `@pytest.mark.parametrize` across systems, presets, allocation methods
- **Standalone scripts**: benchmark files run via `python`, not pytest

## COVERAGE

~80% across 349 tests. Covers all electoral systems, 11+ presets, coalition logic, opinion dynamics, and acceleration paths. Source measurement in `electoral_sim/`; `tests/` excluded from coverage.
