# ElectionModel

The central class for running electoral simulations.

## Constructor

```python
ElectionModel(
    n_voters: int = 100_000,
    n_constituencies: int = 10,
    parties: list[dict] | None = None,
    electoral_system: str = "FPTP",
    allocation_method: str = "dhondt",
    threshold: float = 0.0,
    temperature: float = 0.5,
    seed: int | None = None,
    behavior_engine: BehaviorEngine | None = None,
    opinion_dynamics: OpinionDynamics | None = None,
    include_nota: bool = False,
    constituency_constraints: dict[int, list[str]] | None = None,
    anti_incumbency: float = 0.0,
    economic_growth: float = 0.0,
    national_mood: float = 0.0,
    alienation_threshold: float = -2.0,
    indifference_threshold: float = 0.3,
    event_probs: dict[str, float] | None = None,
    use_adaptive_strategy: bool = False,
    use_gpu: bool = False,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n_voters` | int | 100,000 | Total number of voter agents |
| `n_constituencies` | int | 10 | Number of electoral districts |
| `parties` | list[dict] | None | Party configurations (auto-generated if None) |
| `electoral_system` | str | "FPTP" | "FPTP" or "PR" |
| `allocation_method` | str | "dhondt" | For PR: "dhondt", "sainte_lague", "hare", "droop" |
| `threshold` | float | 0.0 | Electoral threshold (0-1) |
| `temperature` | float | 0.5 | MNL temperature (lower = more deterministic) |
| `seed` | int | None | Random seed for reproducibility |
| `behavior_engine` | BehaviorEngine | None | Custom voter behavior models |
| `opinion_dynamics` | OpinionDynamics | None | Social network for opinion evolution |
| `include_nota` | bool | False | Include "None of the Above" option |
| `anti_incumbency` | float | 0.0 | Penalty to incumbent parties |
| `economic_growth` | float | 0.0 | Economic growth rate (affects retrospective voting) |
| `national_mood` | float | 0.0 | Wave election modifier (+ pro-incumbent, - anti-incumbent) |
| `alienation_threshold` | float | -2.0 | Abstain if max utility below this |
| `indifference_threshold` | float | 0.3 | Abstain if utility range below this |
| `use_gpu` | bool | False | Use CuPy GPU acceleration |

---

## Class Methods

### from_config

Create model from a Config object.

```python
@classmethod
def from_config(cls, config: Config) -> ElectionModel
```

**Example:**
```python
from electoral_sim import Config, ElectionModel, PartyConfig

config = Config(
    n_voters=100_000,
    parties=[
        PartyConfig("Left", -0.5, 0.0, 50),
        PartyConfig("Right", 0.5, 0.0, 50),
    ],
    electoral_system="PR"
)
model = ElectionModel.from_config(config)
```

### from_preset

Create model from a country preset.

```python
@classmethod
def from_preset(cls, preset: str, **kwargs) -> ElectionModel
```

**Available presets:** `"india"`, `"usa"`, `"uk"`, `"germany"`, `"brazil"`, `"france"`, `"japan"`, `"australia_house"`, `"australia_senate"`, `"south_africa"`

**Example:**
```python
model = ElectionModel.from_preset("germany", n_voters=50_000)
```

---

## Chainable Methods

### with_system

```python
def with_system(self, system: str) -> ElectionModel
```
Set electoral system ("FPTP" or "PR").

### with_allocation

```python
def with_allocation(self, method: str) -> ElectionModel
```
Set PR allocation method.

### with_threshold

```python
def with_threshold(self, threshold: float) -> ElectionModel
```
Set electoral threshold (0-1).

### with_temperature

```python
def with_temperature(self, temperature: float) -> ElectionModel
```
Set MNL temperature.

**Example:**
```python
results = (
    ElectionModel(n_voters=50_000)
    .with_system("PR")
    .with_allocation("sainte_lague")
    .with_threshold(0.05)
    .run_election()
)
```

---

## Instance Methods

### run_election

Run a single election simulation.

```python
def run_election(self, **kwargs) -> dict
```

**Returns:** Dictionary with:
| Key | Type | Description |
|-----|------|-------------|
| `seats` | np.ndarray | Seats won by each party |
| `vote_counts` | np.ndarray | Votes received by each party |
| `turnout` | float | Fraction of voters who voted |
| `gallagher` | float | Disproportionality index |
| `enp_votes` | float | ENP by vote share |
| `enp_seats` | float | ENP by seat share |
| `vse` | float | Voter Satisfaction Efficiency |

### run_elections_batch

Run multiple elections for Monte Carlo analysis.

```python
def run_elections_batch(
    self, 
    n_elections: int = 10, 
    reset_voters: bool = False
) -> list[dict]
```

### get_aggregate_stats

Compute statistics across multiple elections.

```python
def get_aggregate_stats(self, results: list[dict] | None = None) -> dict
```

**Returns:**
```python
{
    "n_elections": 100,
    "turnout_mean": 0.754,
    "turnout_std": 0.012,
    "gallagher_mean": 12.5,
    "gallagher_std": 2.1,
    ...
}
```

### step

Run one simulation step (for opinion dynamics).

```python
def step(self) -> None
```

---

## Accessing Agent Data

### Voters
```python
model.voters.df  # Polars DataFrame with voter attributes
```

Columns include:
- `constituency` — District assignment
- `age`, `gender`, `education`, `income`, `religion` — Demographics
- `party_id_7pt` — Party identification (-3 to +3)
- `ideology_x`, `ideology_y` — 2D ideological position
- `openness`, `conscientiousness`, `extraversion`, `agreeableness`, `neuroticism` — Big Five
- `mf_care`, `mf_fairness`, `mf_loyalty`, `mf_authority`, `mf_sanctity` — Moral Foundations
- `political_knowledge`, `misinfo_susceptibility` — Information attributes
- `turnout_prob` — Base turnout probability

### Parties
```python
model.parties.df  # Polars DataFrame with party attributes
```

Columns:
- `name` — Party name
- `position_x`, `position_y` — Ideological position
- `valence` — Non-policy appeal score
- `incumbent` — Is incumbent party
- `seats`, `vote_share` — Results (after election)

---

## Config

Configuration dataclass for model setup.

```python
@dataclass
class Config:
    n_voters: int = 100_000
    n_constituencies: int = 10
    parties: list[PartyConfig | dict] = field(default_factory=list)
    electoral_system: Literal["FPTP", "PR"] = "FPTP"
    allocation_method: Literal["dhondt", "sainte_lague", "hare", "droop"] = "dhondt"
    threshold: float = 0.0
    temperature: float = 0.5
    seed: int | None = None
```

## PartyConfig

Party definition dataclass.

```python
@dataclass
class PartyConfig:
    name: str
    position_x: float = 0.0
    position_y: float = 0.0
    valence: float = 50.0
    incumbent: bool = False
```
