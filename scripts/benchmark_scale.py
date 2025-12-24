import time
import numpy as np
import polars as pl
import psutil
import os
from electoral_sim import ElectionModel, Config

def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB

def run_benchmark(n_voters):
    print(f"\n--- Benchmarking {n_voters:,} agents ---")
    start_mem = get_process_memory()
    
    start_time = time.perf_counter()
    
    # 1. Initialization (Voter Generation)
    init_start = time.perf_counter()
    config = Config(n_voters=n_voters, n_constituencies=100)
    model = ElectionModel(
        n_voters=n_voters,
        n_constituencies=100,
        seed=42
    )
    init_time = time.perf_counter() - init_start
    init_mem = get_process_memory() - start_mem
    print(f"  Initialization: {init_time:.2f}s, Mem: {init_mem:.2f}MB")
    
    # 2. Run Election (Utility compute + Counting)
    election_start = time.perf_counter()
    results = model.run_election()
    election_time = time.perf_counter() - election_start
    peak_mem = get_process_memory() - start_mem
    print(f"  Election Run: {election_time:.2f}s, Peak Mem: {peak_mem:.2f}MB")
    
    total_time = time.perf_counter() - start_time
    print(f"  TOTAL: {total_time:.2f}s")
    
    return {
        "n_voters": n_voters,
        "init_time": init_time,
        "election_time": election_time,
        "total_time": total_time,
        "init_mem_mb": init_mem,
        "peak_mem_mb": peak_mem
    }

if __name__ == "__main__":
    scales = [1_000_000, 5_000_000, 10_000_000]
    results = []
    
    for scale in scales:
        try:
            results.append(run_benchmark(scale))
        except Exception as e:
            print(f"FAILED scale {scale}: {e}")
            break
            
    print("\nSummary Results:")
    print(f"{'Voters':>12} | {'Init(s)':>8} | {'Elec(s)':>8} | {'Mem(MB)':>8}")
    print("-" * 45)
    for r in results:
        print(f"{r['n_voters']:12,d} | {r['init_time']:8.2f} | {r['election_time']:8.2f} | {r['peak_mem_mb']:8.2f}")
