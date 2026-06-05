"""Summary and ideological space chart functions.

Extracted from plots.py to keep each file under the 250-LOC ceiling.
"""

import numpy as np

from electoral_sim.visualization.plots import _check_matplotlib, DEFAULT_COLORS

try:
    import matplotlib.pyplot as plt

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None


def plot_election_summary(
    results: dict,
    party_names: list[str],
    colors: list[str] | None = None,
    title: str = "Election Summary",
    figsize: tuple = (14, 6),
) -> "plt.Figure":
    """Create a comprehensive 2-panel election summary.

    Left: Seat distribution bar chart
    Right: Seats vs Votes comparison

    Args:
        results: Election results dict
        party_names: List of party names
        colors: Optional list of colors
        title: Overall title
        figsize: Figure size

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    if colors is None:
        colors = DEFAULT_COLORS[: len(party_names)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    seats = results["seats"]
    vote_counts = results["vote_counts"]
    total_votes = vote_counts.sum()
    total_seats = seats.sum()

    vote_shares = vote_counts / total_votes * 100
    seat_shares = seats / total_seats * 100 if total_seats > 0 else np.zeros_like(seats)

    sorted_indices = np.argsort(seats)[::-1]
    sorted_names = [party_names[i] for i in sorted_indices]
    sorted_seats = seats[sorted_indices]
    sorted_colors = [colors[i % len(colors)] for i in sorted_indices]

    y_pos = np.arange(len(sorted_names))
    ax1.barh(y_pos, sorted_seats, color=sorted_colors, edgecolor="white")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(sorted_names)
    ax1.invert_yaxis()
    ax1.set_xlabel("Seats")
    ax1.set_title("Seat Distribution", fontsize=12, fontweight="bold")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    x = np.arange(len(party_names))
    width = 0.35

    ax2.bar(x - width / 2, vote_shares, width, label="Vote %", color="#4ECDC4")
    ax2.bar(x + width / 2, seat_shares, width, label="Seat %", color="#FF6B6B")
    ax2.set_ylabel("Percentage (%)")
    ax2.set_title("Votes vs Seats", fontsize=12, fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(party_names, rotation=45, ha="right")
    ax2.legend(loc="upper right")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle(title, fontsize=16, fontweight="bold", y=1.02)

    turnout = results.get("turnout", 0)
    gallagher = results.get("gallagher", 0)
    enp = results.get("enp_votes", 0)

    summary_text = f"Turnout: {turnout*100:.1f}% | Gallagher: {gallagher:.2f} | ENP: {enp:.2f}"
    fig.text(0.5, -0.02, summary_text, ha="center", fontsize=11, style="italic")

    plt.tight_layout()
    return fig


def plot_ideological_space(
    voter_positions: np.ndarray,
    party_positions: np.ndarray,
    party_names: list[str],
    colors: list[str] | None = None,
    title: str = "Ideological Space (Economic vs Social)",
    figsize: tuple = (10, 8),
) -> "plt.Figure":
    """Plot 2D scatter of voter opinions and party positions."""
    _check_matplotlib()

    if colors is None:
        colors = DEFAULT_COLORS[: len(party_names)]

    fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(
        voter_positions[:, 0], voter_positions[:, 1], c="gray", alpha=0.1, s=2, label="Voters"
    )

    for i, name in enumerate(party_names):
        ax.scatter(
            party_positions[i, 0],
            party_positions[i, 1],
            marker="*",
            s=300,
            color=colors[i % len(colors)],
            edgecolor="black",
            label=name,
            zorder=5,
        )

    ax.set_xlabel("Economic Axis (Left <-> Right)")
    ax.set_ylabel("Social Axis (Lib <-> Auth)")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(alpha=0.3)
    ax.axhline(0, color="black", alpha=0.2)
    ax.axvline(0, color="black", alpha=0.2)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    return fig
