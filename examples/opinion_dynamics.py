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

"""
Opinion Dynamics Example.

Demonstrates social network-based opinion evolution using noisy voter
and bounded confidence models across different network topologies.
"""

import numpy as np
from electoral_sim import OpinionDynamics

print("=" * 60)
print("Opinion Dynamics Example")
print("=" * 60)

rng = np.random.default_rng(42)

for topo in ["barabasi_albert", "watts_strogatz", "erdos_renyi"]:
    print(f"\n{topo}:")
    od = OpinionDynamics(n_agents=500, topology=topo, m=3, seed=42)
    opinions = rng.integers(0, 3, od.n_agents)

    # Run 50 steps of noisy voter
    for _ in range(50):
        opinions = od.step(opinions, model="noisy_voter", noise_rate=0.01)

    # Opinion distribution
    shares = od.get_opinion_shares(opinions, 3)
    for i, s in enumerate(shares):
        print(f"  Opinion {i}: {s:.1%}")

# Network diagnostics
from electoral_sim.dynamics.opinion_dynamics import generate_network, network_diagnostics

adj_list, G = generate_network(100, "barabasi_albert", m=3)
diag = network_diagnostics(G, rng.integers(0, 3, 100))
print("\nNetwork diagnostics:")
print(f"  Clustering: {diag['clustering_coefficient']:.3f}")
print(f"  Components: {diag['connected_components']}")
print(f"  Homophily: {diag['homophily']:.3f}")
