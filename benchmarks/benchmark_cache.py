# Copyright 2025-2026 Ayush Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
