# Visualization

Chart functions for election result visualization using matplotlib. All functions return the matplotlib `Figure` for further customization or saving.

> **Requires:** `matplotlib`. Install with `pip install matplotlib` or `pip install electoral-sim[viz]`.

---

## plot_seat_distribution

Horizontal bar chart of seat distribution, sorted by seats descending.

```python
from electoral_sim.visualization.plots import plot_seat_distribution

fig = plot_seat_distribution(
    results=results,
    party_names=party_names,
    colors=None,
    title="Seat Distribution",
    figsize=(10, 6),
    show_values=True,
)
fig.savefig("seats.png")
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `results` | dict | *required* | Election results dict with `'seats'` key |
| `party_names` | `list[str]` | *required* | List of party names |
| `colors` | `list[str] \| None` | `None` | Optional list of colors per party |
| `title` | str | `"Seat Distribution"` | Chart title |
| `figsize` | tuple | `(10, 6)` | Figure size (width, height) |
| `show_values` | bool | `True` | Show seat counts on bars |

**Returns:** matplotlib `Figure` object.

**Example:**
```python
from electoral_sim import ElectionModel
from electoral_sim.visualization.plots import plot_seat_distribution

model = ElectionModel(n_voters=10_000)
results = model.run_election()

fig = plot_seat_distribution(
    results,
    model.parties.get_names(),
    title="2024 General Election",
)
fig.show()
```

---

## plot_vote_shares

Pie chart of vote shares. Small parties below threshold are grouped as "Others".

```python
from electoral_sim.visualization.plots import plot_vote_shares

fig = plot_vote_shares(
    results=results,
    party_names=party_names,
    colors=None,
    title="Vote Share",
    figsize=(8, 8),
    threshold=0.02,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `results` | dict | *required* | Election results dict with `'vote_counts'` key |
| `party_names` | `list[str]` | *required* | List of party names |
| `colors` | `list[str] \| None` | `None` | Optional list of colors per party |
| `title` | str | `"Vote Share"` | Chart title |
| `figsize` | tuple | `(8, 8)` | Figure size |
| `threshold` | float | `0.02` | Minimum share to show label (2%) |

**Returns:** matplotlib `Figure` object.

---

## plot_seats_vs_votes

Grouped bar chart comparing vote share to seat share per party. Includes Gallagher Index annotation.

```python
from electoral_sim.visualization.plots import plot_seats_vs_votes

fig = plot_seats_vs_votes(
    results=results,
    party_names=party_names,
    colors=None,
    title="Seats vs Votes",
    figsize=(10, 6),
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `results` | dict | *required* | Election results with `'vote_counts'` and `'seats'` keys |
| `party_names` | `list[str]` | *required* | List of party names |
| `colors` | `list[str] \| None` | `None` | Optional list of colors per party |
| `title` | str | `"Seats vs Votes"` | Chart title |
| `figsize` | tuple | `(10, 6)` | Figure size |

**Returns:** matplotlib `Figure` object.

**Example:**
```python
# Compare different electoral systems visually
fig_fptp = plot_seats_vs_votes(
    fptp_results, party_names, title="FPTP — Seats vs Votes"
)
fig_pr = plot_seats_vs_votes(
    pr_results, party_names, title="PR — Seats vs Votes"
)
```

---

## plot_election_summary

Comprehensive 2-panel election summary: seat distribution (left) and seats vs votes comparison (right). Includes turnout, Gallagher Index, and ENP in a footer.

```python
from electoral_sim.visualization._summary_plots import plot_election_summary

fig = plot_election_summary(
    results=results,
    party_names=party_names,
    colors=None,
    title="Election Summary",
    figsize=(14, 6),
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `results` | dict | *required* | Election results dict |
| `party_names` | `list[str]` | *required* | List of party names |
| `colors` | `list[str] \| None` | `None` | Optional list of colors |
| `title` | str | `"Election Summary"` | Overall title |
| `figsize` | tuple | `(14, 6)` | Figure size |

**Returns:** matplotlib `Figure` object.

---

## plot_ideological_space

2D scatter plot of voter opinions and party positions in ideological space.

```python
from electoral_sim.visualization._summary_plots import plot_ideological_space

fig = plot_ideological_space(
    voter_positions=voter_positions,
    party_positions=party_positions,
    party_names=party_names,
    colors=None,
    title="Ideological Space (Economic vs Social)",
    figsize=(10, 8),
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `voter_positions` | `np.ndarray` | *required* | `(n_voters, 2)` voter ideology coordinates |
| `party_positions` | `np.ndarray` | *required* | `(n_parties, 2)` party ideology coordinates |
| `party_names` | `list[str]` | *required* | List of party names |
| `colors` | `list[str] \| None` | `None` | Optional list of colors per party |
| `title` | str | `"Ideological Space (Economic vs Social)"` | Chart title |
| `figsize` | tuple | `(10, 8)` | Figure size |

**Returns:** matplotlib `Figure` object.

**Example:**
```python
from electoral_sim import ElectionModel
from electoral_sim.visualization._summary_plots import plot_ideological_space

model = ElectionModel(n_voters=5_000)
model.run_election()

voter_pos = model.voters.get_positions()
party_pos = model.parties.get_positions()
names = model.parties.get_names()

fig = plot_ideological_space(voter_pos, party_pos, names)
fig.savefig("ideology.png", dpi=150)
```
