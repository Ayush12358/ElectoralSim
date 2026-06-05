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
Chart functions for election result visualization.

Uses matplotlib for plotting. All functions return the matplotlib Figure
for further customization or saving.
"""

import numpy as np

try:
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None


def _check_matplotlib():
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib is required for visualization. " "Install it with: pip install matplotlib"
        )


# Default party colors
DEFAULT_COLORS = [
    "#FF6B6B",  # Red
    "#4ECDC4",  # Teal
    "#45B7D1",  # Blue
    "#96CEB4",  # Green
    "#FFEAA7",  # Yellow
    "#DDA0DD",  # Plum
    "#98D8C8",  # Mint
    "#F7DC6F",  # Gold
    "#BB8FCE",  # Purple
    "#85C1E9",  # Light Blue
]


def plot_seat_distribution(
    results: dict,
    party_names: list[str],
    colors: list[str] | None = None,
    title: str = "Seat Distribution",
    figsize: tuple = (10, 6),
    show_values: bool = True,
) -> "plt.Figure":
    """
    Plot horizontal bar chart of seat distribution.

    Args:
        results: Election results dict with 'seats' key
        party_names: List of party names
        colors: Optional list of colors per party
        title: Chart title
        figsize: Figure size (width, height)
        show_values: Show seat counts on bars

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    seats = results["seats"]
    if colors is None:
        colors = DEFAULT_COLORS[: len(party_names)]

    # Sort by seats descending
    sorted_indices = np.argsort(seats)[::-1]
    sorted_names = [party_names[i] for i in sorted_indices]
    sorted_seats = seats[sorted_indices]
    sorted_colors = [colors[i % len(colors)] for i in sorted_indices]

    fig, ax = plt.subplots(figsize=figsize)

    y_pos = np.arange(len(sorted_names))
    bars = ax.barh(y_pos, sorted_seats, color=sorted_colors, edgecolor="white")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_names)
    ax.invert_yaxis()  # Largest at top
    ax.set_xlabel("Seats")
    ax.set_title(title, fontsize=14, fontweight="bold")

    if show_values:
        for bar, seat in zip(bars, sorted_seats):
            if seat > 0:
                ax.text(
                    bar.get_width() + 0.5,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(seat)}",
                    va="center",
                    fontsize=10,
                )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


def plot_vote_shares(
    results: dict,
    party_names: list[str],
    colors: list[str] | None = None,
    title: str = "Vote Share",
    figsize: tuple = (8, 8),
    threshold: float = 0.02,
) -> "plt.Figure":
    """
    Plot pie chart of vote shares.

    Args:
        results: Election results dict with 'vote_counts' key
        party_names: List of party names
        colors: Optional list of colors per party
        title: Chart title
        figsize: Figure size
        threshold: Minimum share to show label (others grouped as "Other")

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    vote_counts = results["vote_counts"]
    total_votes = vote_counts.sum()
    vote_shares = vote_counts / total_votes

    if colors is None:
        colors = DEFAULT_COLORS[: len(party_names)]

    # Group small parties
    labels = []
    sizes = []
    chart_colors = []
    other_share = 0.0

    for i, (name, share) in enumerate(zip(party_names, vote_shares)):
        if share >= threshold:
            labels.append(f"{name} ({share*100:.1f}%)")
            sizes.append(share)
            chart_colors.append(colors[i % len(colors)])
        else:
            other_share += share

    if other_share > 0:
        labels.append(f"Others ({other_share*100:.1f}%)")
        sizes.append(other_share)
        chart_colors.append("#808080")

    fig, ax = plt.subplots(figsize=figsize)

    wedges, texts = ax.pie(
        sizes,
        labels=labels,
        colors=chart_colors,
        startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=2),
    )

    ax.set_title(title, fontsize=14, fontweight="bold")

    plt.tight_layout()
    return fig


def plot_seats_vs_votes(
    results: dict,
    party_names: list[str],
    colors: list[str] | None = None,
    title: str = "Seats vs Votes",
    figsize: tuple = (10, 6),
) -> "plt.Figure":
    """
    Plot grouped bar chart comparing vote share to seat share.

    Args:
        results: Election results dict with 'vote_counts' and 'seats' keys
        party_names: List of party names
        colors: Optional list of colors per party
        title: Chart title
        figsize: Figure size

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    vote_counts = results["vote_counts"]
    seats = results["seats"]

    total_votes = vote_counts.sum()
    total_seats = seats.sum()

    vote_shares = vote_counts / total_votes * 100
    seat_shares = seats / total_seats * 100 if total_seats > 0 else np.zeros_like(seats)

    if colors is None:
        colors = DEFAULT_COLORS[: len(party_names)]

    # Sort by vote share descending
    sorted_indices = np.argsort(vote_shares)[::-1]
    sorted_names = [party_names[i] for i in sorted_indices]
    sorted_vote_shares = vote_shares[sorted_indices]
    sorted_seat_shares = seat_shares[sorted_indices]

    fig, ax = plt.subplots(figsize=figsize)

    x = np.arange(len(sorted_names))
    width = 0.35

    bars1 = ax.bar(x - width / 2, sorted_vote_shares, width, label="Vote %", color="#4ECDC4")
    bars2 = ax.bar(x + width / 2, sorted_seat_shares, width, label="Seat %", color="#FF6B6B")

    ax.set_ylabel("Percentage (%)")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_names, rotation=45, ha="right")
    ax.legend()

    # Add Gallagher index annotation
    gallagher = results.get("gallagher", 0)
    ax.annotate(
        f"Gallagher Index: {gallagher:.2f}",
        xy=(0.98, 0.95),
        xycoords="axes fraction",
        ha="right",
        va="top",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="wheat"),
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


from electoral_sim.visualization._summary_plots import (  # noqa: E402
    plot_election_summary,
    plot_ideological_space,
)  # noqa: F401
