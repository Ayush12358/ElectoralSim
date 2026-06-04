#!/usr/bin/env python3
"""
Core Performance Benchmarks for ElectoralSim

Reproducible benchmarks for voter creation, election run, and batch throughput.
Reports hardware/environment details so numbers are interpretable.

Usage:
    python benchmarks/benchmark_core.py
    python benchmarks/benchmark_core.py --voters 10000 100000 500000
    python benchmarks/benchmark_core.py --warmup 3 --runs 5
"""

import argparse
import platform
import sys
import time

import numpy as np
import polars as pl


def report_environment():
    """Print hardware and software environment details."""
    print("=" * 70)
    print("ENVIRONMENT")
    print("=" * 70)
    print(f"  OS:         {platform.system()} {platform.release()}")
    print(f"  CPU:        {platform.processor() or 'unknown'}")
    print(f"  Python:     {sys.version.split()[0]}")
    print(f"  Polars:     {pl.__version__}")
    print(f"  NumPy:      {np.__version__}")

    try:
        import numba
        print(f"  Numba:      {numba.__version__}")
    except ImportError:
        print("  Numba:      NOT INSTALLED")

    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024**3)
        print(f"  RAM:        {ram_gb:.1f} GB")
        _HAS_PSUTIL = True
    except ImportError:
        print("  RAM:        unknown (install psutil for memory reporting)")
        _HAS_PSUTIL = False

    print()


def measure_memory():
    """Return current process RSS in MB, or -1 if psutil unavailable."""
    try:
        import psutil
        import os
        return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    except ImportError:
        return -1


def warmup_numba():
    """Trigger Numba JIT compilation so warm runs reflect steady-state perf."""
    from electoral_sim import ElectionModel

    m = ElectionModel(n_voters=1000, n_constituencies=3, seed=42)
    _ = m.run_election()
    # Also warm up dhondt/sainte-lague numba paths
    from electoral_sim.engine.numba_accel import NUMBA_AVAILABLE
    if NUMBA_AVAILABLE:
        from electoral_sim.engine.numba_accel import dhondt_numba, sainte_lague_numba
        votes = np.array([1000, 800, 500, 300], dtype=np.int64)
        _ = dhondt_numba(votes, 10)
        _ = sainte_lague_numba(votes, 10)


def benchmark_voter_creation(n_voters: int, n_constituencies: int = 10):
    """Benchmark voter DataFrame generation."""
    from electoral_sim.core.voter_generation import generate_voter_frame

    rng = np.random.default_rng(42)

    mem_before = measure_memory()
    t0 = time.perf_counter()
    df = generate_voter_frame(n_voters, n_constituencies, rng)
    elapsed = time.perf_counter() - t0
    mem_after = measure_memory()
    mem_delta = mem_after - mem_before if mem_before > 0 else -1

    return {
        "n_voters": n_voters,
        "columns": len(df.columns),
        "rows": len(df),
        "time_ms": elapsed * 1000,
        "memory_mb": mem_delta,
    }


def benchmark_election(n_voters: int, system: str = "FPTP", allocation: str = "dhondt"):
    """Benchmark a single election run end-to-end."""
    from electoral_sim import ElectionModel

    mem_before = measure_memory()
    t0 = time.perf_counter()
    m = ElectionModel(
        n_voters=n_voters,
        n_constituencies=10,
        electoral_system=system,
        allocation_method=allocation,
        seed=42,
    )
    results = m.run_election()
    elapsed = time.perf_counter() - t0
    mem_after = measure_memory()
    mem_delta = mem_after - mem_before if mem_before > 0 else -1

    return {
        "system": system,
        "n_voters": n_voters,
        "time_ms": elapsed * 1000,
        "memory_mb": mem_delta,
        "turnout": results.get("turnout", 0),
        "gallagher": results.get("gallagher", 0),
    }


def benchmark_batch_throughput(n_voters: int, n_elections: int = 20):
    """Benchmark batch election throughput."""
    from electoral_sim import ElectionModel

    m = ElectionModel(n_voters=n_voters, n_constituencies=10, electoral_system="FPTP", seed=42)

    t0 = time.perf_counter()
    for _ in range(n_elections):
        m.run_election()
    elapsed = time.perf_counter() - t0

    return {
        "n_voters": n_voters,
        "n_elections": n_elections,
        "total_time_ms": elapsed * 1000,
        "avg_time_ms": (elapsed / n_elections) * 1000,
        "elections_per_sec": n_elections / elapsed,
    }


def run_all_benchmarks(voter_scales: list[int], warmup_runs: int = 2, measure_runs: int = 3):
    """Run the full benchmark suite."""
    print("=" * 70)
    print("BENCHMARKS")
    print("=" * 70)

    # --- Warmup ---
    print(f"\nWarming up JIT ({warmup_runs} passes)...", end=" ", flush=True)
    for _ in range(warmup_runs):
        warmup_numba()
    print("done.\n")

    # --- Voter Creation ---
    print("-" * 70)
    print("VOTER CREATION (DataFrame generation)")
    print("-" * 70)
    print(f"{'Voters':>12} {'Columns':>8} {'Time (ms)':>10} {'Memory (MB)':>12}")
    print("-" * 70)
    for scale in voter_scales:
        best = float("inf")
        for _ in range(measure_runs):
            r = benchmark_voter_creation(scale)
            if r["time_ms"] < best:
                best = r["time_ms"]
                best_result = r
        mem_str = f"{best_result['memory_mb']:.0f}" if best_result['memory_mb'] > 0 else "N/A"
        print(f"{best_result['n_voters']:>12,} {best_result['columns']:>8} {best:>10.1f} {mem_str:>12}")

    # --- FPTP Election ---
    print("\n" + "-" * 70)
    print("FPTP ELECTION (create model + run_election)")
    print("-" * 70)
    print(f"{'Voters':>12} {'Time (ms)':>10} {'Memory (MB)':>12} {'Turnout':>8} {'Gallagher':>10}")
    print("-" * 70)
    for scale in voter_scales:
        best = float("inf")
        for _ in range(measure_runs):
            r = benchmark_election(scale, "FPTP")
            if r["time_ms"] < best:
                best = r["time_ms"]
                best_result = r
        mem_str = f"{best_result['memory_mb']:.0f}" if best_result['memory_mb'] > 0 else "N/A"
        print(f"{best_result['n_voters']:>12,} {best:>10.1f} {mem_str:>12} {best_result['turnout']:>7.1%} {best_result['gallagher']:>10.2f}")

    # --- PR Election ---
    print("\n" + "-" * 70)
    print("PR ELECTION (Sainte-Laguë, 5% threshold)")
    print("-" * 70)
    print(f"{'Voters':>12} {'Time (ms)':>10} {'Gallagher':>10}")
    print("-" * 70)
    for scale in voter_scales:
        if scale > 200_000:  # Skip very large PR for speed
            continue
        best = float("inf")
        for _ in range(measure_runs):
            r = benchmark_election(scale, "PR", "sainte_lague")
            if r["time_ms"] < best:
                best = r["time_ms"]
                best_result = r
        print(f"{best_result['n_voters']:>12,} {best:>10.1f} {best_result['gallagher']:>10.2f}")

    # --- Batch Throughput ---
    print("\n" + "-" * 70)
    print("BATCH THROUGHPUT (repeated elections, FPTP)")
    print("-" * 70)
    print(f"{'Voters':>12} {'Avg (ms)':>10} {'Elections/s':>12}")
    print("-" * 70)
    for scale in [v for v in voter_scales if v <= 200_000]:
        r = benchmark_batch_throughput(scale, n_elections=20)
        print(f"{r['n_voters']:>12,} {r['avg_time_ms']:>10.1f} {r['elections_per_sec']:>12.1f}")

    print("\n" + "=" * 70)
    print("BENCHMARKS COMPLETE")
    print("=" * 70)
    print("\nNote: Timings exclude Numba JIT warmup (compiled in warmup passes above).")
    print("Memory is RSS delta (process memory increase) in MB.")
    print("Run on:", platform.node(), "/", platform.system(), platform.release())
    print("Reproduce: python benchmarks/benchmark_core.py --warmup 3 --runs 5")


def main():
    parser = argparse.ArgumentParser(
        description="ElectoralSim Core Performance Benchmarks"
    )
    parser.add_argument(
        "--voters",
        type=int,
        nargs="+",
        default=[10_000, 50_000, 100_000, 500_000, 1_000_000],
        help="Voter counts to benchmark (default: 10K 50K 100K 500K 1M)",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=2,
        help="JIT warmup passes before measurement (default: 2)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Measurement runs per data point, best taken (default: 3)",
    )
    args = parser.parse_args()

    report_environment()
    run_all_benchmarks(args.voters, args.warmup, args.runs)


if __name__ == "__main__":
    main()
