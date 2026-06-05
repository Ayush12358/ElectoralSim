# Duverger's Law Experiment

Multi-step simulation demonstrating Duverger's Law: FPTP tends toward two-party systems while PR maintains multi-party diversity.

## run_duverger_experiment

Run a sequence of elections with strategic voting to observe convergence effects.

```python
from electoral_sim.analysis.duverger import run_duverger_experiment

history = run_duverger_experiment(
    n_voters=2000,
    n_parties=5,
    n_steps=10,
    system="FPTP",
    seed=42,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n_voters` | int | `2000` | Number of voters |
| `n_parties` | int | `5` | Number of initial parties |
| `n_steps` | int | `10` | Number of sequential elections |
| `system` | `Literal["FPTP", "PR"]` | `"FPTP"` | Electoral system to simulate |
| `seed` | int | `42` | Random seed |
| `strategic_penalty` | float | `50.0` | Utility penalty for voting for unviable parties |
| `viability_threshold` | float | `0.15` | Vote share threshold for party viability |
| `temperature` | float | `0.1` | Logit temperature (lower = sharper choices) |

**Returns:** List of per-step dicts, each containing:
| Key | Type | Description |
|-----|------|-------------|
| `step` | int | Election number (0-indexed) |
| `enp` | float | Effective Number of Parties |
| `vote_shares` | `list[float]` | Vote share per party |
| `winner` | int | Index of winning party |

**Mechanics:** The experiment uses `BehaviorEngine` with `ProximityModel` + `WastedVoteModel` to capture the psychological effect of Duverger's Law. After each election, vote shares become the viability signal for the next round, creating a feedback loop that amplifies strategic voting.

**Example:**
```python
# Compare FPTP vs PR convergence
import polars as pl

fptp = run_duverger_experiment(n_voters=5000, system="FPTP", n_steps=15)
pr = run_duverger_experiment(n_voters=5000, system="PR", n_steps=15)

for h in fptp:
    print(f"Step {h['step']}: ENP = {h['enp']:.2f}")

# Under FPTP, ENP should converge towards ~2
# Under PR, ENP should remain close to n_parties
```

---

## Research Basis

Duverger's Law mechanics rely on two effects:

1. **Mechanical Effect:** High threshold for representation in FPTP — only the largest party in each constituency wins a seat.
2. **Psychological Effect:** Strategic voting to avoid wasted votes — voters abandon unviable parties over repeated election cycles.

The experiment simulates both effects simultaneously using `WastedVoteModel` with a viability feedback loop.

See also: [Electoral Systems](electoral_systems.md), [Behavior Models](behavior_models.md).
