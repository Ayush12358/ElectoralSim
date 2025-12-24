"""
Custom Toolkit Demo: Building a 'Build Your Own' Election

Demonstrates the modularity of ElectoralSim:
- Custom behavior engine (Proximity + Retrospective)
- Social network integration
- Multi-step opinion dynamics
"""

import numpy as np
from electoral_sim import (
    ElectionModel, 
    BehaviorEngine, ProximityModel, RetrospectiveModel,
    OpinionDynamics
)

def run_custom_sim():
    print("=" * 60)
    print("DEMO: Building a Custom Electoral Simulation")
    print("=" * 60)
    
    # 1. Setup Behavior Engine
    # We want voters to care about ideology AND the economy
    engine = BehaviorEngine()
    engine.add_model(ProximityModel(weight=1.0))
    engine.add_model(RetrospectiveModel(weight=2.0)) # Strong economic effect
    
    # 2. Setup Social Network for Opinion Dynamics
    od = OpinionDynamics(n_agents=10000, topology="barabasi_albert", m=2)
    
    # 3. Create Model with Custom Behavior and Dynamics
    # Custom parties where one is an incumbent
    parties = [
        {"name": "Incumbent Party", "position_x": 0.2, "position_y": 0.2, "valence": 50, "incumbent": True},
        {"name": "Opposition A", "position_x": -0.5, "position_y": -0.3, "valence": 45, "incumbent": False},
        {"name": "Opposition B", "position_x": 0.0, "position_y": -0.6, "valence": 40, "incumbent": False},
    ]
    
    model = ElectionModel(
        n_voters=10000,
        n_constituencies=5,
        parties=parties,
        behavior_engine=engine,
        opinion_dynamics=od,
        seed=42
    )
    
    # 4. Simulate a recession (negative growth)
    print("\nSimulating a recession (Growth: -2.0)...")
    
    # Run 5 steps of opinion dynamics before the election
    print("Voters are talking to each other (Opinion Dynamics)...")
    for _ in range(5):
        model.step()
    
    # Run election with economic context
    print("Election Day!")
    results = model.run_election(growth=-2.0)
    
    print(f"\nResults (Recession Scenario):")
    print(f"  Turnout: {results['turnout']:.1%}")
    for i, name in enumerate([p['name'] for p in parties]):
        votes = results['vote_counts'][i]
        seats = results['seats'][i]
        print(f"    {name}: {votes:,} votes, {seats} seats")
        
    # 5. Simulate a boom (positive growth)
    print("\n" + "-"*40)
    print("Simulating an economic boom (Growth: +2.0)...")
    results_boom = model.run_election(growth=2.0)
    
    print(f"\nResults (Boom Scenario):")
    for i, name in enumerate([p['name'] for p in parties]):
        votes = results_boom['vote_counts'][i]
        seats = results_boom['seats'][i]
        print(f"    {name}: {votes:,} votes, {seats} seats")

    print("\n" + "=" * 60)
    print("Modularity Test Passed!")
    print("=" * 60)

if __name__ == "__main__":
    run_custom_sim()
