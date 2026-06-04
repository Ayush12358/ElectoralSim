# Benchmarks

Reproducible performance benchmarks for ElectoralSim.

## Quick Run

```bash
python benchmarks/benchmark_core.py
```

## Options

```bash
python benchmarks/benchmark_core.py --voters 10000 100000 500000 1000000
python benchmarks/benchmark_core.py --warmup 5 --runs 10
```

## Methodology

- **Warmup**: Numba JIT is triggered before measurement to report steady-state performance.
- **Timing**: `time.perf_counter()` around the operation, best of N runs reported.
- **Memory**: RSS delta via `psutil` (process resident set size). Falls back to "N/A" if psutil not installed.
- **Election**: Model creation + `run_election()` combined, FPTP with default 3 parties, 10 constituencies.

## Environment Notes

Record hardware details when publishing numbers. The scripts auto-print OS, Python version, and library versions. Add hardware manually:

| Run | CPU | RAM | OS | Python |
|-----|-----|-----|-----|--------|
| local | Intel i5-1135G7 | 16 GB | Ubuntu 22.04 | 3.12 |
