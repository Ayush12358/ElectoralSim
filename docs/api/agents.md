# Agents

Agent classes for voters, parties, and adaptive party strategies. Agents are stored as Polars DataFrames for vectorized operations, not as individual Python objects.

---

## VoterAgents

Voter agents stored as a Polars DataFrame for high-performance vectorized operations.

```python
# VoterAgents is created internally by ElectionModel
model = ElectionModel(n_voters=100_000)
voters = model.voters  # VoterAgents instance

# Access underlying data
n = voters.n_voters
positions = voters.get_positions()  # shape (n_voters, 2)
```

**Constructor (internal):**
```python
VoterAgents(model: ElectionModel, df: pl.DataFrame)
```

**DataFrame columns:**

| Column | Type | Description |
|--------|------|-------------|
| `unique_id` | int | Auto-generated agent identifier |
| `constituency` | int | Constituency index (0 to n_constituencies-1) |
| `ideology_x` | float | Economic left-right (-1 to 1) |
| `ideology_y` | float | Social liberal-conservative (-1 to 1) |
| `party_id` | int | Current party identification |
| `knowledge` | float | Political knowledge (0-100) |
| `turnout_prob` | float | Base probability of voting (0-1) |
| `media_susceptibility` | float | Susceptibility to media influence (0-1) |
| `is_zealot` | bool | Whether agent has fixed opinion |

### Properties & Methods

#### n_voters

```python
@property
def n_voters(self) -> int
```

Total number of voters.

#### get_positions

```python
def get_positions(self) -> np.ndarray
```

Return ideology positions as `(n_voters, 2)` array `[ideology_x, ideology_y]`. Results are cached.

#### get_ideology_x

```python
def get_ideology_x(self) -> np.ndarray
```

Return economic left-right positions as `(n_voters,)` array, values in [-1, 1]. Cached.

#### get_ideology_y

```python
def get_ideology_y(self) -> np.ndarray
```

Return social liberal-conservative positions as `(n_voters,)` array, values in [-1, 1]. Cached.

#### get_constituencies

```python
def get_constituencies(self) -> np.ndarray
```

Return constituency indices. Cached.

#### get_turnout_prob

```python
def get_turnout_prob(self) -> np.ndarray
```

Return turnout probabilities. Cached.

#### invalidate_cache

```python
def invalidate_cache(self)
```

Clear all cached arrays. Call after modifying the underlying DataFrame.

#### step

```python
def step(self)
```

Mesa-compatible hook. Intentionally inert — voter behavior is handled in batch by `ElectionModel.run_election()`, not per-agent.

---

## PartyAgents

Party agents stored as a Polars DataFrame.

```python
model = ElectionModel.from_preset("uk")
parties = model.parties  # PartyAgents instance

n = parties.n_parties
names = parties.get_names()
positions = parties.get_positions()
valences = parties.get_valence()
```

**Constructor (internal):**
```python
PartyAgents(model: ElectionModel, df: pl.DataFrame)
```

**DataFrame columns:**

| Column | Type | Description |
|--------|------|-------------|
| `unique_id` | int | Party identifier |
| `name` | str | Party name |
| `position_x` | float | Economic left-right (-1 to 1) |
| `position_y` | float | Social liberal-conservative (-1 to 1) |
| `valence` | float | Non-policy appeal (0-100) |
| `incumbent` | bool | Whether currently in government |
| `seats` | int | Current seat count |
| `vote_share` | float | Last election vote share |

### Properties & Methods

#### n_parties

```python
@property
def n_parties(self) -> int
```

Number of parties.

#### get_positions

```python
def get_positions(self) -> np.ndarray
```

Return party positions as `(n_parties, 2)` array `[position_x, position_y]`. Cached.

#### get_valence

```python
def get_valence(self) -> np.ndarray
```

Return party valence scores as `(n_parties,)` array. Cached.

#### get_names

```python
def get_names(self) -> list[str]
```

Return party names.

#### update_results

```python
def update_results(self, seats: np.ndarray, vote_shares: np.ndarray)
```

Update party results after an election.

#### step

```python
def step(self)
```

Mesa-compatible hook. When `use_adaptive_strategy=True`, party positions are updated via `adaptive_strategy_step()` called from `ElectionModel.step()`.

#### invalidate_cache

```python
def invalidate_cache(self)
```

Clear all cached arrays.

---

## adaptive_strategy_step

Update party positions dynamically based on voter distribution and polling data.

```python
from electoral_sim.agents.party_strategy import adaptive_strategy_step

updated_df = adaptive_strategy_step(
    parties_df=parties.df,
    voters_df=voters.df,
    strategy="median_voter",
    learning_rate=0.01,
    noise=0.0,
    rng=np.random.default_rng(42),
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `parties_df` | `pl.DataFrame` | *required* | Party DataFrame (must have `position_x` column) |
| `voters_df` | `pl.DataFrame` | *required* | Voter DataFrame |
| `strategy` | `Literal["median_voter", "stick_to_base", "random_walk"]` | `"median_voter"` | Adaptation strategy |
| `learning_rate` | float | `0.01` | How much to move per step (0-1) |
| `noise` | float | `0.0` | Random noise added to movement |
| `rng` | `np.random.Generator \| None` | `None` | Random generator |

**Returns:** Updated parties DataFrame with modified `position_x` and `position_y`.

**Strategies:**
| Strategy | Behavior |
|----------|----------|
| `"median_voter"` | Move towards median voter ideology position |
| `"stick_to_base"` | Move towards party supporters' mean (requires voting history) |
| `"random_walk"` | Random drift with `learning_rate` as standard deviation |

**Example:**
```python
import numpy as np
from electoral_sim.agents.party_strategy import adaptive_strategy_step

# Run 20 steps of adaptive strategy
for step in range(20):
    new_parties = adaptive_strategy_step(
        parties_df=parties_df,
        voters_df=voters_df,
        strategy="median_voter",
        learning_rate=0.02,
        noise=0.005,
    )
    # Update in-place
    parties_df = new_parties
```
