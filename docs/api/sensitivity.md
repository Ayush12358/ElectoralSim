# Sensitivity Analysis

Parameter sensitivity analysis: one-at-a-time (OAT), grid-based, and swing analysis for exploring how parameter changes affect simulation outcomes.

## one_at_a_time

One-at-a-time sensitivity: vary a single parameter while holding all others fixed.

```python
from electoral_sim.analysis.sensitivity import one_at_a_time
from electoral_sim import ElectionModel

results = one_at_a_time(
    model_class=ElectionModel,
    base_params={"n_voters": 10_000, "n_constituencies": 10},
    vary_param="temperature",
    vary_values=[0.1, 0.3, 0.5, 0.7, 0.9],
    metric="gallagher",
    n_runs=5,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `model_class` | type | ElectionModel class (or compatible) |
| `base_params` | dict | Dictionary of default parameter values |
| `vary_param` | str | Name of the parameter to vary |
| `vary_values` | list | List of values to test for the varying parameter |
| `metric` | str | Metric to track (default `"gallagher"`) |
| `n_runs` | int | Runs per parameter value for averaging (default `3`) |
| `**model_kwargs` | — | Additional kwargs passed to `model_class` |

**Returns:** List of dicts, each containing:
| Key | Description |
|-----|-------------|
| `param` | Name of the varied parameter |
| `value` | The parameter value tested |
| `{metric}_mean` | Mean of the tracked metric across runs |
| `{metric}_std` | Standard deviation across runs |
| `n_runs` | Number of runs |

**Example:**
```python
results = one_at_a_time(
    ElectionModel,
    {"n_voters": 50_000},
    "n_constituencies",
    [5, 10, 20, 50, 100],
    metric="enp_seats",
    n_runs=10,
)

for r in results:
    print(f"Constituencies={r['value']}: ENP={r['enp_seats_mean']:.2f} ± {r['enp_seats_std']:.2f}")
```

---

## grid_sensitivity

Grid-based sensitivity: evaluate all combinations of multiple parameter values.

```python
from electoral_sim.analysis.sensitivity import grid_sensitivity

results = grid_sensitivity(
    model_class=ElectionModel,
    param_grid={
        "n_voters": [10_000, 50_000],
        "temperature": [0.3, 0.7],
        "n_constituencies": [5, 20],
    },
    metric="gallagher",
    n_runs=3,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `model_class` | type | ElectionModel class |
| `param_grid` | `dict[str, list]` | Dict mapping param names to lists of values |
| `metric` | str | Metric to track (default `"gallagher"`) |
| `n_runs` | int | Runs per configuration (default `3`) |
| `**model_kwargs` | — | Additional kwargs passed to `model_class` |

**Returns:** List of dicts, each containing all param values plus `{metric}_mean`, `{metric}_std`, and `n_runs`.

**Example:**
```python
results = grid_sensitivity(
    ElectionModel,
    {
        "temperature": [0.1, 0.5, 0.9],
        "economic_growth": [-0.02, 0.0, 0.02],
    },
    metric="turnout",
    n_runs=5,
    electoral_system="PR",
)
```

---

## swing_analysis

Swing-state/district analysis: perturb a single parameter and track metric tipping points across a range.

```python
from electoral_sim.analysis.sensitivity import swing_analysis

results = swing_analysis(
    model_class=ElectionModel,
    base_params={"n_voters": 50_000, "n_constituencies": 20},
    swing_param="national_mood",
    swing_range=[-3.0, -1.5, 0.0, 1.5, 3.0],
    metric="gallagher",
    n_runs=5,
    seed=42,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `model_class` | type | ElectionModel class |
| `base_params` | dict | Dictionary of default parameter values |
| `swing_param` | str | Parameter to perturb (default `"national_mood"`) |
| `swing_range` | `list[float] \| None` | Values to test (default: -3.0 to +3.0 in 0.5 steps) |
| `metric` | str | Metric to track |
| `n_runs` | int | Runs per swing value (default `3`) |
| `seed` | int | Base seed (default `42`) |
| `**model_kwargs` | — | Additional kwargs for model_class |

**Returns:** List of dicts with `swing_param`, `swing_value`, `{metric}_mean`, `{metric}_std`.

**Example:**
```python
results = swing_analysis(
    ElectionModel,
    {"n_voters": 100_000, "n_constituencies": 50},
    swing_param="economic_growth",
    swing_range=[-0.05 + x * 0.01 for x in range(11)],
    metric="turnout",
    n_runs=10,
)

import polars as pl
df = pl.DataFrame(results)
print(df)
```
