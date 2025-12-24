from electoral_sim.presets.india.election import simulate_india_election
from electoral_sim.visualization.plots import plot_ideological_space
from electoral_sim.visualization.specialized import plot_swing_analysis
import matplotlib.pyplot as plt

def verify_viz():
    print("Running India simulation for verification...")
    results = simulate_india_election(n_voters_per_constituency=100, seed=42, verbose=False)
    
    print("Verifying plot_ideological_space...")
    # Check that data is collected
    if results.voter_df is not None:
        print(f"  Voter sample size: {len(results.voter_df)}")
        fig = plot_ideological_space(
            results.voter_df.select(["ideology_x", "ideology_y"]).to_numpy(),
            results.party_positions,
            list(results.seats.keys())
        )
        fig.savefig("verify_space.png")
        print("  Saved verify_space.png")
    else:
        print("  ERROR: voter_df is None")
        
    print("Verifying plot_swing_analysis...")
    fig_swing = plot_swing_analysis(
        {"seats": results.seats}, 
        target_party="BJP"
    )
    # Plotly figures don't use savefig the same way, but we can verify it exists
    if fig_swing:
        print("  Swing analysis figure created.")
        
if __name__ == "__main__":
    verify_viz()
