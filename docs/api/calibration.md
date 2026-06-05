# Calibration

Calibration framework for fitting simulation parameters against historical election results using loss functions and grid search.

## mse_loss

Calculate Mean Squared Error between simulation outputs and historical targets.

```python
from electoral_sim.analysis.calibration import mse_loss

loss = mse_loss(
    model_class=ElectionModel,
    params={"n_voters": 100_000, "temperature": 0.5},
    targets={"gallagher": 3.5, "turnout": 0.68},
    metric_weights={"gallagher": 2.0, "turnout": 1.0},
    n_runs=5,
    seed=42,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `model_class` | type | ElectionModel class |
| `params` | dict | Simulation parameters |
| `targets` | `dict[str, float]` | Dict mapping metric names to target values |
| `metric_weights` | `dict[str, float] \| None` | Per-metric weight in loss (default: equal) |
| `n_runs` | int | Runs for averaging (default `5`) |
| `seed` | int | Base random seed (default `42`) |

**Returns:** Weighted MSE loss (lower = better fit).

**Supported target metrics:** `"gallagher"`, `"turnout"`, `"enp_votes"`, `"enp_seats"`.

**Example:**
```python
from electoral_sim import ElectionModel
from electoral_sim.analysis.calibration import mse_loss

# Calibrate against historical Irish election (ENP ≈ 4.5, Gallagher ≈ 5.0)
loss = mse_loss(
    ElectionModel,
    params={"n_voters": 50_000, "n_constituencies": 43, "temperature": 0.3},
    targets={"enp_seats": 4.5, "gallagher": 5.0},
    metric_weights={"enp_seats": 1.5, "gallagher": 1.0},
)
print(f"Loss: {loss:.4f}")
```

---

## grid_search_calibration

Grid-search calibration across a defined parameter space.

```python
from electoral_sim.analysis.calibration import grid_search_calibration

results = grid_search_calibration(
    model_class=ElectionModel,
    param_grid={
        "temperature": [0.1, 0.3, 0.5, 0.7],
        "n_constituencies": [10, 20, 30],
    },
    targets={"gallagher": 4.0, "enp_votes": 3.5},
    metric_weights={"gallagher": 1.0, "enp_votes": 0.5},
    n_runs=5,
    seed=42,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `model_class` | type | ElectionModel class |
| `param_grid` | `dict[str, list]` | Dict mapping param names to lists of values to search |
| `targets` | `dict[str, float]` | Target metric values from historical data |
| `metric_weights` | `dict[str, float] \| None` | Optional per-metric weights |
| `n_runs` | int | Simulation runs per parameter combo (default `3`) |
| `seed` | int | Base seed (default `42`) |

**Returns:** List of result dicts **sorted by loss (best first)**, each containing:
| Key | Description |
|-----|-------------|
| `params` | Dict of parameter values for this configuration |
| `loss` | Weighted MSE loss |

**Example:**
```python
results = grid_search_calibration(
    ElectionModel,
    param_grid={
        "temperature": [0.1, 0.3, 0.5],
        "economic_growth": [-0.02, 0.0, 0.02],
    },
    targets={"turnout": 0.65, "gallagher": 3.0},
)

best = results[0]
print(f"Best config: {best['params']} (loss={best['loss']:.4f})")
```

---

## generate_calibration_report

Generate a human-readable calibration report from grid search results.

```python
from electoral_sim.analysis.calibration import generate_calibration_report

report = generate_calibration_report(
    results=results,
    targets={"gallagher": 4.0, "enp_votes": 3.5},
)
print(report)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `results` | `list[dict]` | Calibration results from `grid_search_calibration()` |
| `targets` | `dict[str, float]` | Target metric values for reference |

**Returns:** Formatted report string showing targets, best configuration, and top 5 results.
