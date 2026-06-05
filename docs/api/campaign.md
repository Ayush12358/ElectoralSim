# Campaign Models

Campaign modeling subsystem: finance, media environment, voter registration,
constituency targeting, turnout mobilization, and polling access.

## CampaignFinance

Campaign finance model with spending-to-valence conversion.

```python
from electoral_sim.behavior.campaign import CampaignFinance

cf = CampaignFinance(
    base_spending=1_000_000.0,
    incumbent_advantage=1.5,
    diminishing_factor=0.5,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_spending` | float | `1_000_000.0` | Base campaign spending per party (monetary units) |
| `incumbent_advantage` | float | `1.5` | Multiplier for incumbent fundraising |
| `diminishing_factor` | float | `0.5` | Diminishing returns exponent (<1 = steeper curve) |

### compute_spending

```python
def compute_spending(
    self,
    n_parties: int,
    incumbents: np.ndarray | None = None,
    rng: np.random.Generator | None = None,
) -> np.ndarray
```

Compute campaign spending per party. Incumbent parties get a spending advantage.

**Returns:** Array of spending per party.

**Example:**
```python
import numpy as np

spending = cf.compute_spending(
    n_parties=5,
    incumbents=np.array([True, False, False, False, False]),
    rng=np.random.default_rng(42)
)
```

### spending_to_valence

```python
def spending_to_valence(self, spending: np.ndarray) -> np.ndarray
```

Convert campaign spending to valence boost with diminishing returns. Formula: `log1p(spending) ** diminishing_factor * 5.0`.

**Returns:** Valence boost per party (additive to base valence).

### district_targeting

```python
def district_targeting(
    self,
    spending: np.ndarray,
    n_districts: int,
    marginal_seats: np.ndarray | None = None,
) -> np.ndarray
```

Allocate campaign spending across districts. Parties allocate more resources to marginal (competitive) districts.

**Returns:** `(n_parties, n_districts)` spending allocation matrix.

---

## MediaEnvironment

Media environment model: tracks party exposure, sentiment, reach, and misinformation susceptibility with time decay.

```python
from electoral_sim.behavior.campaign import MediaEnvironment

media = MediaEnvironment(
    base_exposure=0.5,
    sentiment_bias=0.0,
    reach_decay=0.95,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_exposure` | float | `0.5` | Base media exposure level (0-1) |
| `sentiment_bias` | float | `0.0` | Media sentiment bias (-1=anti-incumbent, +1=pro-incumbent) |
| `reach_decay` | float | `0.95` | Time-decay factor for past media effects (<1 = fading) |

### step

```python
def step(
    self,
    n_parties: int,
    incumbents: np.ndarray | None = None,
    rng: np.random.Generator | None = None,
) -> dict
```

Advance one media cycle, generating new exposure and sentiment data.

**Returns:** Dict with `exposure`, `sentiment`, and `reach` per party.

**Example:**
```python
for _ in range(10):
    result = media.step(n_parties=5)
    print(f"Exposure: {result['exposure']}")
```

### misinformation_susceptibility

```python
def misinformation_susceptibility(self, media_diet: np.ndarray | None = None) -> float
```

Estimate population-level susceptibility to misinformation. Lower media diet diversity → higher susceptibility.

**Returns:** Misinformation susceptibility (0-1).

---

## VoterRegistration

Voter registration and eligibility model. Models eligible population, registration status, turnout probability, and age effects.

```python
from electoral_sim.behavior._campaign_models import VoterRegistration

vr = VoterRegistration(
    eligible_rate=0.85,
    registration_rate=0.75,
    base_turnout=0.65,
    age_effect=0.1,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `eligible_rate` | float | `0.85` | Fraction of population eligible to vote |
| `registration_rate` | float | `0.75` | Fraction of eligible voters who register |
| `base_turnout` | float | `0.65` | Baseline turnout probability |
| `age_effect` | float | `0.1` | Effect of age on turnout (per 10 years from median) |

### compute_eligibility

```python
def compute_eligibility(
    self,
    n_voters: int,
    age: np.ndarray | None = None,
    rng: np.random.Generator | None = None,
) -> dict[str, np.ndarray]
```

Compute eligibility, registration, and voting status.

**Returns:** Dict with boolean arrays: `eligible`, `registered`, `will_vote`.

---

## CampaignTargeting

Local campaign targeting: parties allocate resources across constituencies based on marginal-seat value with budget constraints and diminishing returns on persuasion.

```python
from electoral_sim.behavior._campaign_models import CampaignTargeting

ct = CampaignTargeting(
    total_budget=100.0,
    marginal_weight=0.7,
    persuasion_decay=0.5,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `total_budget` | float | `100.0` | Total campaign budget |
| `marginal_weight` | float | `0.7` | Weight given to marginal seats (vs uniform) |
| `persuasion_decay` | float | `0.5` | Diminishing returns exponent on spending |

### allocate_resources

```python
def allocate_resources(self, marginality: np.ndarray) -> np.ndarray
```

Allocate budget proportionally to constituency marginality.

### persuasion_effect

```python
def persuasion_effect(self, spending: np.ndarray) -> np.ndarray
```

Compute persuasion effect from spending with diminishing returns. Formula: `spending ** persuasion_decay * 0.01`.

---

## TurnoutMobilization

Turnout mobilization: models canvassing, GOTV, persuasion vs mobilization, targeted demographics, and resource allocation.

```python
from electoral_sim.behavior._campaign_models import TurnoutMobilization

tm = TurnoutMobilization(
    base_turnout=0.65,
    canvass_effect=0.05,
    mobilization_effect=0.08,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_turnout` | float | `0.65` | Baseline turnout level |
| `canvass_effect` | float | `0.05` | Impact of canvassing on turnout |
| `mobilization_effect` | float | `0.08` | Impact of mobilization efforts |

### decompose_turnout

```python
def decompose_turnout(
    self,
    baseline: float,
    alienation: float,
    indifference: float,
    mobilization: float,
) -> dict[str, float]
```

Decompose total turnout into its constituent factors.

**Returns:** Dict with `baseline`, `alienation_effect`, `indifference_effect`, `mobilization_effect`, `total`.

---

## PollingAccess

Polling-place accessibility model: distance, wait time, and registration friction effects on turnout.

```python
from electoral_sim.behavior._campaign_models import PollingAccess

pa = PollingAccess(
    distance_decay=0.1,
    wait_penalty=0.05,
    registration_friction=0.02,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `distance_decay` | float | `0.1` | Turnout reduction per unit distance |
| `wait_penalty` | float | `0.05` | Turnout reduction per unit wait time |
| `registration_friction` | float | `0.02` | Fixed turnout penalty from registration hurdles |

### compute_turnout_adjustment

```python
def compute_turnout_adjustment(
    self,
    distances: np.ndarray,
    wait_times: np.ndarray | None = None,
    base_turnout: float = 0.65,
) -> np.ndarray
```

Compute adjusted turnout probabilities accounting for polling access barriers.

**Returns:** Clipped turnout probabilities per voter.

**Example:**
```python
distances = np.random.uniform(0, 10, 1000)
adjusted = pa.compute_turnout_adjustment(distances, base_turnout=0.65)
```
