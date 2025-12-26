# Command-Line Interface (CLI)

ElectoralSim provides a powerful command-line interface for running elections and batch simulations.

## Installation

The CLI is automatically installed when you install the package:

```bash
pip install electoral-sim
```

Verify installation:

```bash
electoral-sim --version
```

## Commands

### `run` - Single Simulation

Run an election simulation with customizable parameters or country presets.

#### Basic Usage

```bash
# Simple simulation
electoral-sim run --voters 50000 --constituencies 10

# With specific system
electoral-sim run --system PR --allocation dhondt --threshold 0.05

# Save results
electoral-sim run --voters 100000 --output results.json
```

#### Using Presets

```bash
# India (Lok Sabha)
electoral-sim run --preset india --voters 100000

# Germany (Bundestag)
electoral-sim run --preset germany

# EU Parliament
electoral-sim run --preset eu
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--voters` | `-n` | Number of voters | 100,000 |
| `--constituencies` | `-c` | Number of constituencies | 10 |
| `--system` | `-s` | Electoral system (FPTP, PR, IRV, STV) | FPTP |
| `--allocation` | `-a` | PR method (dhondt, sainte_lague, hare, droop) | dhondt |
| `--threshold` | `-t` | Electoral threshold (0-1) | 0.0 |
| `--preset` | `-p` | Country preset | None |
| `--seed` | | Random seed | None |
| `--output` | `-o` | Output file (JSON) | None |
| `--quiet` | `-q` | Suppress output | False |

---

### `batch` - Parameter Sweeps

Execute multiple simulations with varying parameters for sensitivity analysis.

#### Configuration File

Create a JSON config file (`batch_config.json`):

```json
{
  "parameters": {
    "n_voters": [10000, 50000, 100000],
    "temperature": [0.3, 0.5, 0.7],
    "economic_growth": [-0.02, 0.0, 0.02],
    "electoral_system": ["FPTP", "PR"]
  },
  "fixed_params": {
    "n_constituencies": 10
  },
  "sweep_type": "grid",
  "n_runs_per_config": 5,
  "n_jobs": 4,
  "seed": 42
}
```

#### Running Batch Simulations

```bash
# Basic batch
electoral-sim batch --config batch_config.json --output results.csv

# With summary statistics
electoral-sim batch --config batch_config.json --output results.csv --summary summary.csv

# Parallel execution
electoral-sim batch --config batch_config.json --output results.csv --jobs 8
```

#### Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `parameters` | Dictionary of parameters to sweep (lists of values) |
| `fixed_params` | Parameters that don't vary across runs |
| `sweep_type` | `"grid"` (all combinations) or `"random"` (sampling) |
| `n_samples` | Number of random samples (for random sweep) |
| `n_runs_per_config` | Monte Carlo iterations per configuration |
| `n_jobs` | Parallel workers |
| `seed` | Random seed for reproducibility |

#### Output Formats

- `.csv` - CSV format (compatible with Excel, R, etc.)
- `.parquet` - Parquet format (compressed, fast)
- `.json` - JSON format

---

### `list-presets` - Available Presets

Display all available country/region electoral system presets.

```bash
electoral-sim list-presets
```

#### Available Presets

| Preset | Description |
|--------|-------------|
| `india` | 543 constituencies, FPTP, 17 parties (Lok Sabha) |
| `usa` | 435 districts, FPTP, 2 parties (House) |
| `uk` | 650 constituencies, FPTP, 5+ parties (Commons) |
| `germany` | 299 districts, MMP (PR), 5% threshold (Bundestag) |
| `france` | 577 constituencies, Two-round, 5 parties |
| `japan` | 289 constituencies, Mixed, 2% threshold |
| `brazil` | 513 seats, Open-list PR, 8 parties |
| `australia_house` | 151 electorates, IRV, 5 parties |
| `australia_senate` | 76 seats, STV, 5 parties |
| `south_africa` | 400 seats, Closed-list PR, 8 parties |
| `eu` | 720 MEPs, 27 states, D'Hondt (EU Parliament) |

---

## Examples

### Example 1: Quick FPTP Simulation

```bash
electoral-sim run --voters 50000 --constituencies 25 --output uk_style.json
```

### Example 2: Proportional Representation with Threshold

```bash
electoral-sim run --system PR --allocation sainte_lague --threshold 0.05 --voters 100000
```

### Example 3: India Election

```bash
electoral-sim run --preset india --voters 500000 --seed 42 --output india_election.json
```

### Example 4: Sensitivity Analysis

Create `sensitivity_config.json`:

```json
{
  "parameters": {
    "temperature": [0.1, 0.3, 0.5, 0.7, 0.9],
    "economic_growth": [-0.05, -0.02, 0.0, 0.02, 0.05]
  },
  "fixed_params": {
    "n_voters": 50000,
    "n_constituencies": 20,
    "electoral_system": "FPTP"
  },
  "n_runs_per_config": 10,
  "n_jobs": 4
}
```

Run:

```bash
electoral-sim batch --config sensitivity_config.json --output sensitivity_results.csv --summary sensitivity_summary.csv
```

### Example 5: Multi-Country Comparison

```bash
# Run multiple presets
for country in india usa uk germany; do
  electoral-sim run --preset $country --output ${country}_results.json
done
```

---

## Output Format

### Single Simulation (JSON)

```json
{
  "metadata": {
    "system": "FPTP",
    "voters": 100000,
    "constituencies": 10
  },
  "results": {
    "turnout": 0.75,
    "gallagher": 12.5,
    "enp_votes": 3.2,
    "enp_seats": 2.8
  },
  "parties": {
    "Party A": {
      "votes": 45000,
      "seats": 6,
      "vote_share": 0.45
    }
  }
}
```

### Batch Simulation (CSV)

| config_idx | run_idx | n_voters | temperature | turnout | gallagher | enp_votes |
|------------|---------|----------|-------------|---------|-----------|-----------|
| 0 | 0 | 10000 | 0.3 | 0.78 | 11.2 | 3.1 |
| 0 | 1 | 10000 | 0.3 | 0.76 | 12.5 | 3.0 |
| 1 | 0 | 10000 | 0.5 | 0.75 | 13.1 | 3.2 |

---

## Tips

1. **Use `--seed`** for reproducible results
2. **Start small** with voter counts for testing
3. **Use presets** for realistic country simulations
4. **Parallel execution** (`--jobs`) speeds up batch runs significantly
5. **Parquet format** is faster and more compact for large datasets

---

## Man Page

View detailed documentation:

```bash
man electoral-sim
```

Or view the man page file directly:

```bash
man ./electoral-sim.1
```

---

## Related Documentation

- [Python API Reference](../api/README.md)
- [Country Presets](../presets/README.md)
- [Quick Start Guide](../quickstart.md)
