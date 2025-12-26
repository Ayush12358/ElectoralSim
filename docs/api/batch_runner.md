# Batch Runner API

Advanced batch simulation with parameter sweeping for sensitivity analysis and Monte Carlo studies.

## Overview

The `BatchRunner` enables systematic parameter exploration by running multiple simulations with varying configurations. It supports:

- **Parameter sweeps**: Grid search or random sampling
- **Parallel execution**: Multi-core processing for faster results
- **Results aggregation**: Automatic statistics computation
- **Multiple export formats**: CSV, Parquet, JSON

## Classes

### `ParameterSweep`

Defines parameter combinations to explore.

```python
from electoral_sim.analysis import ParameterSweep

sweep = ParameterSweep(
    parameters={
        'n_voters': [10_000, 50_000, 100_000],
        'temperature': [0.3, 0.5, 0.7],
        'economic_growth': [-0.02, 0.0, 0.02]
    },
    fixed_params={
        'n_constituencies': 10,
        'electoral_system': 'FPTP'
    },
    sweep_type='grid',  # 'grid' or 'random'
    n_samples=100  # For random sampling
)
```

**Parameters**:
- `parameters` (dict): Dictionary mapping parameter names to lists of values
- `fixed_params` (dict): Parameters that don't vary across runs
- `sweep_type` (str): `'grid'` for all combinations or `'random'` for sampling
- `n_samples` (int): Number of random samples (for sweep_type='random')

**Methods**:
- `generate_configs()` → `list[dict]`: Generate all parameter configurations
- `__len__()` → `int`: Number of configurations

---

### `BatchRunner`

Executes multiple simulations with varying parameters.

```python
from electoral_sim import ElectionModel
from electoral_sim.analysis import BatchRunner, ParameterSweep

runner = BatchRunner(
    model_class=ElectionModel,
    parameter_sweep=sweep,
    n_runs_per_config=5,
    n_jobs=4,
    seed=42,
    verbose=True
)
```

**Parameters**:
- `model_class` (Type): `ElectionModel` or compatible class
- `parameter_sweep` (ParameterSweep): Parameter sweep configuration
- `n_runs_per_config` (int): Monte Carlo iterations per configuration (default: 1)
- `n_jobs` (int): Number of parallel workers (default: 1, sequential)
- `election_kwargs` (dict): Extra kwargs passed to `run_election()`
- `seed` (int): Random seed for reproducibility
- `verbose` (bool): Show progress bars (default: True)

**Methods**:

#### `run()`
Execute the batch run.

```python
results_df = runner.run()
```

**Returns**: `polars.DataFrame` with all simulation results

**Result Columns**:
- `config_idx`: Configuration index
- `run_idx`: Run index within configuration
- `seed`: Random seed used
- Parameter columns (e.g., `n_voters`, `temperature`)
- Metric columns (`turnout`, `gallagher`, `enp_votes`, `enp_seats`, `vse`)

---

#### `get_summary_stats()`
Aggregate statistics across runs for each configuration.

```python
summary = runner.get_summary_stats()
```

**Returns**: `polars.DataFrame` with mean, std for each configuration

**Summary Columns**:
- `config_idx`: Configuration index
- Parameter columns
- `*_mean`: Mean of each metric
- `*_std`: Standard deviation of each metric
- `n_runs`: Number of runs per config

---

#### `export_results(filepath, format='auto')`
Export full results to file.

```python
runner.export_results('results.csv')
runner.export_results('results.parquet')
runner.export_results('results.json')
```

**Parameters**:
- `filepath` (str): Output file path
- `format` (str): `'csv'`, `'parquet'`, `'json'`, or `'auto'` (infer from extension)

---

#### `export_summary(filepath, format='auto')`
Export summary statistics to file.

```python
runner.export_summary('summary.csv')
```

---

## Examples

### Basic Parameter Sweep

```python
from electoral_sim import ElectionModel
from electoral_sim.analysis import BatchRunner, ParameterSweep

# Simple grid search
sweep = ParameterSweep({
    'n_voters': [10_000, 50_000],
    'temperature': [0.3, 0.5, 0.7]
})

runner = BatchRunner(
    model_class=ElectionModel,
    parameter_sweep=sweep,
    n_runs_per_config=10,
    seed=42
)

results_df = runner.run()
runner.export_results('sweep_results.csv')
```

### Sensitivity Analysis

Test how different parameters affect outcomes:

```python
sweep = ParameterSweep({
    'temperature': [0.1, 0.3, 0.5, 0.7, 0.9],
    'economic_growth': [-0.05, -0.02, 0.0, 0.02, 0.05]
}, fixed_params={
    'n_voters': 50_000,
    'n_constituencies': 20
})

runner = BatchRunner(
    model_class=ElectionModel,
    parameter_sweep=sweep,
    n_runs_per_config=20,
    n_jobs=8,  # Use 8 cores
    seed=42
)

results_df = runner.run()
summary = runner.get_summary_stats()

# Analyze temperature effect
import polars as pl
print(summary.select(['temperature', 'gallagher_mean', 'enp_votes_mean']))
```

### Random Sampling

For high-dimensional parameter spaces:

```python
sweep = ParameterSweep(
    parameters={
        'n_voters': [10_000, 25_000, 50_000, 75_000, 100_000],
        'temperature': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        'economic_growth': [-0.05, -0.02, 0.0, 0.02, 0.05],
        'anti_incumbency': [0.0, 0.1, 0.2, 0.3]
    },
    sweep_type='random',
    n_samples=200  # Sample 200 random combinations
)

runner = BatchRunner(
    model_class=ElectionModel,
    parameter_sweep=sweep,
    n_runs_per_config=5,
    n_jobs=4
)

results_df = runner.run()
```

### Electoral System Comparison

```python
sweep = ParameterSweep({
    'electoral_system': ['FPTP', 'PR'],
    'n_voters': [50_000, 100_000]
}, fixed_params={
    'n_constituencies': 20
})

runner = BatchRunner(
    model_class=ElectionModel,
    parameter_sweep=sweep,
    n_runs_per_config=10,
    seed=42
)

results_df = runner.run()

# Compare systems
comparison = results_df.group_by('electoral_system').agg([
    pl.col('gallagher').mean().alias('avg_gallagher'),
    pl.col('enp_seats').mean().alias('avg_enp_seats')
])
print(comparison)
```

---

## Command-Line Usage

Run batch simulations from the terminal:

```bash
# Create config file
cat > batch_config.json << EOF
{
  "parameters": {
    "n_voters": [10000, 50000, 100000],
    "temperature": [0.3, 0.5, 0.7]
  },
  "fixed_params": {
    "n_constituencies": 10
  },
  "n_runs_per_config": 5,
  "n_jobs": 4
}
EOF

# Run batch
electoral-sim batch --config batch_config.json --output results.csv --summary summary.csv
```

See the [CLI Guide](../cli.md) for more details.

---

## Performance Tips

1. **Use parallel execution** (`n_jobs > 1`) for significant speedup
2. **Start small**: Test with few configurations before full sweep
3. **Parquet format** is faster and more compact than CSV for large datasets
4. **Fixed seed** ensures reproducibility across runs
5. **Progress bars** (`verbose=True`) help monitor long-running batches

---

## See Also

- [ElectionModel API](election_model.md) - Core simulation class
- [CLI Guide](../cli.md) - Command-line batch execution
- [Quick Start](../quickstart.md) - Basic usage examples
