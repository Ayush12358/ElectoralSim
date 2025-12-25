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


def plot_election_summary(
    results: dict,
    party_names: list[str],
    colors: list[str] | None = None,
    title: str = "Election Summary",
    figsize: tuple = (14, 6),
) -> "plt.Figure":
    """
    Create a comprehensive 2-panel election summary.

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

    # Left panel: Seat distribution
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

    # Right panel: Seats vs Votes
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

    # Overall title and metrics
    fig.suptitle(title, fontsize=16, fontweight="bold", y=1.02)

    # Add summary text
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
    """
    Plot 2D scatter of voter opinions and party positions.
    """
    _check_matplotlib()

    if colors is None:
        colors = DEFAULT_COLORS[: len(party_names)]

    fig, ax = plt.subplots(figsize=figsize)

    # Plot voters with low alpha to show density
    ax.scatter(
        voter_positions[:, 0], voter_positions[:, 1], c="gray", alpha=0.1, s=2, label="Voters"
    )

    # Plot parties with large markers
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

    # Legend outside to the right
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    return fig


# =============================================================================
# Quick test
# =============================================================================

if __name__ == "__main__":
    _check_matplotlib()

    # Mock results for testing
    mock_results = {
        "seats": np.array([45, 35, 15, 5, 0]),
        "vote_counts": np.array([10000, 8000, 5000, 3000, 1000]),
        "turnout": 0.72,
        "gallagher": 8.5,
        "enp_votes": 3.2,
        "enp_seats": 2.5,
    }
    party_names = ["Party A", "Party B", "Party C", "Party D", "Party E"]

    print("Generating test plots...")

    fig1 = plot_seat_distribution(mock_results, party_names)
    fig1.savefig("test_seats.png", dpi=100, bbox_inches="tight")
    print("  Saved test_seats.png")

    fig2 = plot_vote_shares(mock_results, party_names)
    fig2.savefig("test_votes.png", dpi=100, bbox_inches="tight")
    print("  Saved test_votes.png")

    fig3 = plot_seats_vs_votes(mock_results, party_names)
    fig3.savefig("test_comparison.png", dpi=100, bbox_inches="tight")
    print("  Saved test_comparison.png")

    fig4 = plot_election_summary(mock_results, party_names)
    fig4.savefig("test_summary.png", dpi=100, bbox_inches="tight")
    print("  Saved test_summary.png")

    print("Done!")
