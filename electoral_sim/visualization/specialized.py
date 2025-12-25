"""
Advanced Visualizations for ElectoralSim.

Includes animations, cartograms, and interactive dashboards.
"""

from typing import Any

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import polars as pl


def animate_opinion_dynamics(
    history: list[pl.DataFrame],
    party_pos: np.ndarray,
    party_names: list[str],
    interval: int = 100,
    filename: str | None = None,
):
    """
    Create an animation of the opinion space as voters move.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Static elements
    ax.set_title("Voter Opinion Dynamics", fontsize=16)
    ax.set_xlabel("Economic Axis (Left <-> Right)", fontsize=12)
    ax.set_ylabel("Social Axis (Lib <-> Auth)", fontsize=12)
    ax.grid(alpha=0.3)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # Plot parties as fixed points
    for i, name in enumerate(party_names):
        ax.scatter(party_pos[i, 0], party_pos[i, 1], marker="*", s=300, label=name)
    ax.legend()

    # Voter scatter
    scat = ax.scatter([], [], alpha=0.1, s=5, c="gray")

    def update(frame):
        df = history[frame]
        x = df["ideology_x"].to_numpy()
        y = df["ideology_y"].to_numpy()
        scat.set_offsets(np.c_[x, y])
        ax.set_title(f"Voter Opinion Dynamics (T = {frame})")
        return (scat,)

    ani = animation.FuncAnimation(fig, update, frames=len(history), interval=interval, blit=True)

    if filename:
        ani.save(filename, writer="pillow")
        print(f"Animation saved to {filename}")

    return ani


def plot_swing_analysis(
    results: dict[str, Any],
    swing_range: np.ndarray = np.arange(-5, 6, 1),
    target_party: str = "BJP",
):
    """
    Produce a 'Swingometer' style graph showing how seat count
    changes with national vote swing.
    """
    # This is a simplified analysis: shifting global utilities or
    # vote shares directly to estimate seat conversion.
    # In a real simulation, you'd re-run for each swing.

    # For now, we'll implement the UI logic for the dashboard
    fig = go.Figure()

    # Mock data for demonstration if not provided
    # In the dashboard, this will call the model multiple times
    base_seats = results.get("seats", {target_party: 300}).get(target_party, 300)
    multiplier = 5  # Seats per 1% swing

    swings = swing_range
    seats = [base_seats + s * multiplier for s in swings]

    fig.add_trace(
        go.Scatter(
            x=swings,
            y=seats,
            mode="lines+markers",
            name=f"{target_party} Seat Projection",
            line=dict(color="orange", width=4),
        )
    )

    fig.update_layout(
        title=f"Swing Analysis: {target_party}",
        xaxis_title="National Swing (%)",
        yaxis_title="Projected Seats",
        template="plotly_dark",
    )

    return fig


def plot_india_state_map(results_summary: dict[str, Any]):
    """
    Plot a bubble map of India states showing seat distribution.
    """
    # Simple coordinates for India states (approximate central points)
    STATE_COORDS = {
        "Uttar Pradesh": [26.8467, 80.9462],
        "Maharashtra": [19.7515, 75.7139],
        "West Bengal": [22.9868, 87.8550],
        "Bihar": [25.0961, 85.3131],
        "Tamil Nadu": [11.1271, 78.6569],
        "Madhya Pradesh": [22.9734, 78.6569],
        "Karnataka": [15.3173, 75.7139],
        "Gujarat": [22.2587, 71.1924],
        "Rajasthan": [27.0238, 74.2179],
        "Andhra Pradesh": [15.9129, 79.7400],
        "Odisha": [20.9517, 85.0985],
        "Kerala": [10.8505, 76.2711],
        "Telangana": [18.1124, 79.0193],
        "Jharkhand": [23.6102, 85.2799],
        "Assam": [26.2006, 92.9376],
        "Punjab": [31.1471, 75.3412],
        "Chhattisgarh": [21.2787, 81.8661],
        "Haryana": [29.0588, 76.0856],
        "Delhi": [28.6139, 77.2090],
        "Jammu & Kashmir": [33.7782, 76.5762],
        "Uttarakhand": [30.0668, 79.0193],
        "Himachal Pradesh": [31.1048, 77.1734],
    }

    data = []
    for state, res in results_summary.items():
        if state in STATE_COORDS:
            top_party = max(res["seats"].items(), key=lambda x: x[1])[0]
            lat, lon = STATE_COORDS[state]
            data.append(
                {
                    "State": state,
                    "Lat": lat,
                    "Lon": lon,
                    "Winner": top_party,
                    "Seats": sum(res["seats"].values()),
                }
            )

    if not data:
        return None

    df = pl.DataFrame(data)

    fig = px.scatter_geo(
        df.to_pandas(),
        lat="Lat",
        lon="Lon",
        color="Winner",
        hover_name="State",
        size="Seats",
        scope="asia",
        center={"lat": 22, "lon": 80},
        title="India: Regional Seat Distribution (Major States)",
        template="plotly_dark",
    )

    fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="RebeccaPurple")

    return fig
