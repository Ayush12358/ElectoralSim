"""
Visualization module for ElectoralSim

Provides plotting functions for election results using matplotlib.
"""

from electoral_sim.visualization.plots import (
    plot_election_summary,
    plot_ideological_space,
    plot_seat_distribution,
    plot_seats_vs_votes,
    plot_vote_shares,
)

__all__ = [
    "plot_seat_distribution",
    "plot_vote_shares",
    "plot_seats_vs_votes",
    "plot_election_summary",
    "plot_ideological_space",
]
