import time
import numpy as np
import pandas as pd
from electoral_sim import ElectionModel, Config
from electoral_sim.engine.gpu_accel import is_gpu_available


def benchmark_gpu(n_voters=1_000_000):
    print(f"--- Benchmarking {n_voters:,} agents ---")

    # 1. CPU / Numba
    print("Running on CPU (Numba enabled)...")
    start = time.perf_counter()
    model_cpu = ElectionModel(n_voters=n_voters, seed=42, use_gpu=False)
    model_cpu.run_election()
    cpu_time = time.perf_counter() - start
    print(f"  CPU Time: {cpu_time:.2f}s")

    # 2. GPU / CuPy
    gpu_available = is_gpu_available()
    if not gpu_available:
        print("GPU / CuPy not available. Skipping GPU benchmark.")
        return

    print("Running on GPU (CuPy)...")
    start = time.perf_counter()
    model_gpu = ElectionModel(n_voters=n_voters, seed=42, use_gpu=True)
    model_gpu.run_election()
    gpu_time = time.perf_counter() - start
    print(f"  GPU Time: {gpu_time:.2f}s")

    print(f"\nSpeedup: {cpu_time / gpu_time:.1f}x")


if __name__ == "__main__":
    benchmark_gpu(2_000_000)
