"""Benchmark with caching"""

import time
from electoral_sim import ElectionModel

# Warm up
model = ElectionModel(n_voters=10_000, seed=42)
model.run_election()

print("=== Full Benchmark with Caching ===")
print()

# Single election
for n in [100_000, 500_000, 1_000_000]:
    model = ElectionModel(n_voters=n, n_constituencies=100, seed=42)
    start = time.perf_counter()
    model.run_election()
    t1 = time.perf_counter() - start

    # Second run (cached)
    start = time.perf_counter()
    model.run_election()
    t2 = time.perf_counter() - start

    print(f"{n:>10,} voters: {t1*1000:>6.1f} ms (first), {t2*1000:>6.1f} ms (cached)")

print()

# Batch elections
model = ElectionModel(n_voters=500_000, n_constituencies=100, seed=42)
start = time.perf_counter()
results = model.run_elections_batch(n_elections=10)
elapsed = time.perf_counter() - start
print(f"Batch 10 elections (500K voters): {elapsed*1000:.0f} ms ({elapsed*100:.0f} ms/election)")

stats = model.get_aggregate_stats(results)
print(f"  Turnout: {stats['turnout_mean']:.1%} +/- {stats['turnout_std']:.1%}")
print(f"  Gallagher: {stats['gallagher_mean']:.2f} +/- {stats['gallagher_std']:.2f}")
