"""Test P2 Features"""
from electoral_sim import (
    ElectionModel, OpinionDynamics,
    irv_election, stv_election, generate_rankings
)
import numpy as np

print("=== P2 Features Test ===")

# 1. Opinion Dynamics
print("\n1. Opinion Dynamics with Social Networks:")
od = OpinionDynamics(n_agents=5000, topology="barabasi_albert", m=3, seed=42)
print(f"   Network: {od.stats['n_nodes']} nodes, {od.stats['n_edges']} edges")
opinions = od.rng.integers(0, 3, od.n_agents)
for _ in range(20):
    opinions = od.step(opinions, model="noisy_voter", noise_rate=0.01)
print(f"   Shares after 20 steps: {od.get_opinion_shares(opinions, 3)}")

# 2. IRV
print("\n2. IRV/RCV:")
np.random.seed(42)
utilities = np.random.randn(1000, 5)
rankings = generate_rankings(utilities)
result = irv_election(rankings, 5)
print(f"   Winner: Candidate {result['winner']}")
print(f"   Rounds: {len(result['rounds'])}")

# 3. STV
print("\n3. STV (3 seats):")
result = stv_election(rankings, 5, n_seats=3)
print(f"   Elected: {result['elected']}")

print("\n=== All P2 features working! ===")
