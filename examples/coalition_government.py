"""
Coalition Formation and Government Stability Example.

Demonstrates running an election and forming a government from the results,
including coalition strain, stability prediction, and government simulation.
"""

import numpy as np
from electoral_sim import ElectionModel, form_government, coalition_strain
from electoral_sim.engine.government import (
    GovernmentSimulator,
    collapse_probability,
    simulate_government_survival,
)

print("=" * 60)
print("Coalition & Government Example")
print("=" * 60)

# Run a PR election (multi-party system)
model = ElectionModel.from_preset("germany", n_voters=5000)
results = model.run_election()
print(f"\nElection: turnout={results['turnout']:.1%}, Gallagher={results['gallagher']:.2f}")

# Form a government
seats = results["seats"]
positions = model.parties.get_positions()[:, 0]
names = model.parties.get_names()
gov = form_government(seats, positions, names)
print(f"\nGovernment: {gov['coalition_names']} ({gov['seats']} seats)")

# Coalition strain
strain = coalition_strain(positions[gov['coalition']])
print(f"Coalition strain: {strain:.3f}")

# Stability prediction
for model_name in ["sigmoid", "linear", "exponential"]:
    prob = collapse_probability(12, strain, gov["stability"], model=model_name)
    print(f"  {model_name}: collapse prob at 12 months = {prob:.2%}")

# Government simulation
print("\nSimulating government survival...")
gov_sim = GovernmentSimulator(
    strain=strain, stability=gov["stability"],
    coalition_parties=gov["coalition_names"], seed=42
)
months = gov_sim.simulate(max_months=48)
print(f"Government lasted {months} months (out of 48)")
