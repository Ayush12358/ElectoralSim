import streamlit as st
import numpy as np
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from electoral_sim import ElectionModel, Config
from electoral_sim.presets.india.election import simulate_india_election
from electoral_sim.visualization.plots import (
    plot_seat_distribution, plot_vote_shares, plot_seats_vs_votes, plot_ideological_space
)
from electoral_sim.visualization.specialized import (
    plot_swing_analysis, animate_opinion_dynamics, plot_india_state_map
)

# Page configuration
st.set_page_config(
    page_title="ElectoralSim | Interactive Explorer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2227;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e444b;
    }
    h1, h2, h3 {
        color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

st.title("ElectoralSim: Advanced Simulation Engine")
st.markdown("---")

# Sidebar settings
st.sidebar.header("Simulation Settings")
preset = st.sidebar.selectbox("Select Preset", ["India (Lok Sabha)", "USA", "UK", "Germany", "Brazil", "France", "Japan"])

n_voters = st.sidebar.slider("Voter Sample Size", 1000, 100000, 5000, step=1000)
seed = st.sidebar.number_input("Random Seed", value=42)

st.sidebar.subheader("Dynamic Parameters")
economic_growth = st.sidebar.slider("Economic Growth (%)", -10.0, 10.0, 2.0)
national_mood = st.sidebar.slider("National Mood (Wave)", -5.0, 5.0, 0.0)
anti_incumbency = st.sidebar.slider("Anti-Incumbency Penalty", -2.0, 0.0, -0.1)

# Run simulation
if st.button("Run Simulation", type="primary"):
    with st.spinner("Processing voters and ballots..."):
        if preset == "India (Lok Sabha)":
            # Use the specialized India simulation
            results = simulate_india_election(
                n_voters_per_constituency=n_voters // 543 if n_voters > 543 else 100,
                seed=seed,
                verbose=False
            )
            
            # Overview Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Seats", 543)
            # Find largest party
            top_party = max(results.seats, key=results.seats.get)
            m2.metric("Winning Party", top_party, f"{results.seats[top_party]} seats")
            m3.metric("Gallagher Index", f"{results.gallagher:.2f}")
            m4.metric("ENP (Seats)", f"{results.enp_seats:.2f}")
            
            st.markdown("### Election Outcome")
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution Chart
                fig_seats = plot_seat_distribution(results.seats)
                st.plotly_chart(fig_seats, use_container_width=True)
                
            with col2:
                # Vote Shares
                fig_votes = plot_vote_shares(results.vote_shares)
                st.plotly_chart(fig_votes, use_container_width=True)
                
            st.markdown("### Seats vs Votes Disproportionality")
            fig_comp = plot_seats_vs_votes(results.vote_shares, {p: (s/543) for p, s in results.seats.items()})
            st.plotly_chart(fig_comp, use_container_width=True)
            
            st.markdown("### Ideological Landscape")
            # We take a sample of voters for performance in the UI
            df_sample = results.voter_df.sample(min(2000, len(results.voter_df)))
            fig_space = plot_ideological_space(
                df_sample.select(["ideology_x", "ideology_y"]).to_numpy(),
                results.party_positions,
                list(results.seats.keys())
            )
            st.pyplot(fig_space)
            
            st.markdown("### Swing Analysis (What-if?)")
            target_p = st.selectbox("Select Target Party", list(results.seats.keys()))
            fig_swing = plot_swing_analysis(
                {"seats": results.seats}, 
                swing_range=np.arange(-10, 11, 1),
                target_party=target_p
            )
            st.plotly_chart(fig_swing, use_container_width=True)
            
            st.markdown("### Regional Seat Map")
            fig_map = plot_india_state_map(results.state_results)
            if fig_map:
                st.plotly_chart(fig_map, use_container_width=True)
            
            # State-wise details
            with st.expander("Detailed State-wise Results"):
                st.write(results.state_results)
                
            st.markdown("---")
            st.markdown("### Opinion Evolution Gallery")
            if st.checkbox("Show Opinion Dynamics Animation"):
                try:
                    st.image("opinion_dynamics.gif", caption="Voter Opinion Clusters Shifting Over Time")
                except:
                    st.warning("Animation not found. Run 'demo_animation.py' to generate it.")
                
        else:
            # Multi-country fallback using the generic Config
            from electoral_sim.core.config import PRESETS
            
            config_map = {
                "USA": "usa", "UK": "uk", "Germany": "germany", 
                "Brazil": "brazil", "France": "france", "Japan": "japan"
            }
            preset_key = config_map[preset]
            
            # Get the preset config
            config = PRESETS[preset_key](n_voters=n_voters, seed=seed)
            
            # Create model with both config params and dynamic params  
            model = ElectionModel(
                n_voters=config.n_voters,
                n_constituencies=config.n_constituencies,
                parties=config.get_party_dicts(),
                electoral_system=config.electoral_system,
                allocation_method=config.allocation_method,
                threshold=config.threshold,
                temperature=config.temperature,
                seed=config.seed,
                economic_growth=economic_growth / 100.0,  # Convert percentage
                national_mood=national_mood,
                anti_incumbency=anti_incumbency
            )
            results = model.run_election()
            
            party_names = model.parties.df["name"].to_list()
            vote_shares = {p: s for p, s in zip(party_names, results['vote_counts'] / results['vote_counts'].sum())}
            seat_shares = {p: s for p, s in zip(party_names, results['seats'])}
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Turnout", f"{results['turnout']:.1%}")
            m2.metric("Gallagher Index", f"{results['gallagher']:.2f}")
            m3.metric("ENP (Votes)", f"{results['enp_votes']:.2f}")
            
            st.markdown("### Election Outcome")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_seat_distribution(seat_shares), use_container_width=True)
            with col2:
                st.plotly_chart(plot_vote_shares(vote_shares), use_container_width=True)

else:
    st.info("Click 'Run Simulation' to start the analysis.")
    st.image("https://img.freepik.com/free-vector/election-campaign-concept_23-2148593457.jpg?w=1000", use_container_width=True)

st.markdown("---")
st.caption("ElectoralSim v1.0.0 | Built with Streamlit, Plotly, and Polars")
