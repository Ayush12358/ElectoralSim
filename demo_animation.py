from electoral_sim import ElectionModel, Config
import polars as pl
from electoral_sim.visualization.specialized import animate_opinion_dynamics
import numpy as np

def run_animation_demo():
    print("Initializing simulation for animation...")
    n_voters = 2000
    
    # Initialize OpinionDynamics manually
    from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics
    od = OpinionDynamics(n_agents=n_voters, topology="barabasi_albert", seed=42)
    
    # Smaller population for quick animation generation
    model = ElectionModel(n_voters=n_voters, seed=42, opinion_dynamics=od)
    
    # Run simulation for 10 steps of opinion dynamics
    history = []
    current_x = model.voters.df["ideology_x"].to_numpy()
    current_y = model.voters.df["ideology_y"].to_numpy()
    
    for t in range(15):
        print(f"  Step {t}...")
        results = model.run_election()
        history.append(model.voters.df.select(["ideology_x", "ideology_y"]))
        
        # In this demo, we shift ideology_x as a proxy for the simple OpinionDynamics model
        # Real multi-dimensional dynamics would call step on both or use a specialized model
        new_x = od.step(current_x, model="bounded_confidence", epsilon=0.2)
        new_y = od.step(current_y, model="bounded_confidence", epsilon=0.2)
        
        # Update model voters (Simplified update for demo)
        model.voters.df = model.voters.df.with_columns([
            pl.Series("ideology_x", new_x),
            pl.Series("ideology_y", new_y)
        ])
        current_x, current_y = new_x, new_y
        
    print("Generating animation...")
    ani = animate_opinion_dynamics(
        history, 
        model.parties.get_positions(),
        model.parties.df["name"].to_list(),
        filename="opinion_dynamics.gif"
    )
    print("Animation saved as opinion_dynamics.gif")

if __name__ == "__main__":
    run_animation_demo()
