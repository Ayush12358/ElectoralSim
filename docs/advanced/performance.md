# Performance Optimization

Guide to maximizing ElectoralSim performance for large-scale simulations.

## Benchmarks

| Scale | Create Time | Election Time | Memory |
|-------|-------------|---------------|--------|
| 10K voters | 18ms | 5ms | 52 MB |
| 100K voters | 109ms | 35ms | 15 MB |
| 500K voters | 608ms | 176ms | 95 MB |
| 1M voters | 1.2s | 316ms | 148 MB |
| 2M voters | 2.4s | 672ms | 181 MB |

**Batch processing:** ~200ms/election at 500K voters (~5 elections/sec)

---

## Numba JIT Acceleration

Core loops are accelerated with Numba (enabled by default):

```python
from electoral_sim.engine.numba_accel import NUMBA_AVAILABLE

print(f"Numba available: {NUMBA_AVAILABLE}")  # True if installed
```

### Accelerated Functions
- `vote_mnl_fast` — Multinomial logit voting
- `fptp_count_fast` — FPTP vote counting
- `compute_utilities_numba` — Utility matrix calculation

### First-Run Compilation
Numba compiles functions on first call. Expect ~500ms delay initially.

---

## GPU Acceleration (CuPy)

For 1M+ voter simulations, enable GPU:

```python
model = ElectionModel(
    n_voters=2_000_000,
    use_gpu=True,
    seed=42
)
```

### Requirements
```bash
pip install cupy-cuda12x  # For CUDA 12
# or
pip install cupy-cuda11x  # For CUDA 11
```

### Checking GPU Availability

```python
from electoral_sim.engine.gpu_accel import is_gpu_available

if is_gpu_available():
    print("GPU acceleration enabled")
else:
    print("Falling back to CPU/Numba")
```

### GPU-Accelerated Operations
- Utility matrix computation
- Multinomial logit sampling
- Distance calculations

---

## Batch Elections

For Monte Carlo analysis, use batch processing:

```python
model = ElectionModel(n_voters=500_000, seed=42)

# Run 100 elections efficiently
results = model.run_elections_batch(
    n_elections=100,
    reset_voters=False  # Reuse voter frame
)

# Get aggregate statistics
stats = model.get_aggregate_stats(results)
```

### reset_voters Parameter
- `False`: Reuse same voter population (faster, same demographics)
- `True`: Regenerate stochastic columns (ideology, turnout) each run

---

## Data Type Optimization

Voter data uses optimized dtypes:

| Column | dtype | Memory |
|--------|-------|--------|
| Integers (age, knowledge) | int8/int16 | 1-2 bytes |
| Floats (ideology, probabilities) | float32 | 4 bytes |
| IDs | int64 | 8 bytes |

### Custom Voter Frame

For maximum control:

```python
import polars as pl
import numpy as np

# Create minimal voter frame
n = 1_000_000
voter_frame = pl.DataFrame({
    "constituency": np.random.randint(0, 543, n, dtype=np.int16),
    "ideology_x": np.random.randn(n).astype(np.float32),
    "ideology_y": np.random.randn(n).astype(np.float32),
    "turnout_prob": np.random.uniform(0.6, 0.9, n).astype(np.float32),
    "unique_id": np.arange(n, dtype=np.int64),
})

model = ElectionModel(voter_frame=voter_frame)
```

---

## Memory Management

For very large simulations:

```python
import gc

# Run election
results = model.run_election()

# Clear cached data
model.voters.invalidate_cache()

# Force garbage collection
gc.collect()
```

---

## Parallel Processing

For multiple independent simulations:

```python
from concurrent.futures import ProcessPoolExecutor

def run_simulation(seed):
    model = ElectionModel(n_voters=100_000, seed=seed)
    return model.run_election()

# Run 10 simulations in parallel
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(run_simulation, range(10)))
```

---

## Profiling

Identify bottlenecks:

```python
import cProfile
import pstats

with cProfile.Profile() as pr:
    model = ElectionModel(n_voters=100_000)
    model.run_election()

stats = pstats.Stats(pr)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

---

## Tips

1. **Start small**: Test with 10K voters before scaling up
2. **Use seeds**: Ensure reproducibility while benchmarking
3. **Batch when possible**: `run_elections_batch` is faster than repeated `run_election`
4. **Profile first**: Identify actual bottlenecks before optimizing
5. **GPU for 1M+**: Below 1M voters, CPU/Numba is often faster due to transfer overhead
