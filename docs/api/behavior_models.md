# Behavior Models

Voter behavior models compute utility matrices that determine how voters choose between parties.

## BehaviorEngine

Combines multiple behavior models into a single utility calculation.

```python
from electoral_sim import BehaviorEngine, ProximityModel, ValenceModel

engine = BehaviorEngine()
engine.add_model(ProximityModel(weight=1.0))
engine.add_model(ValenceModel(weight=0.5))

model = ElectionModel(n_voters=10_000, behavior_engine=engine)
```

### Methods

#### add_model
```python
def add_model(self, model: BehaviorModel, weight: float = 1.0)
```
Add a behavior model with optional weight.

#### compute_all
```python
def compute_all(self, voter_data: dict, party_data: dict, **kwargs) -> np.ndarray
```
Compute combined utility matrix from all registered models.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `voter_data` | dict | Dict with `n_voters`, `positions`, `ideology_x`, `ideology_y`, `df` |
| `party_data` | dict | Dict with `n_parties`, `positions`, `valence`, `incumbents`, `viability`, `df` |
| `use_gpu` | bool | Enable CuPy GPU acceleration path (default False) |
| `growth` | float | Economic growth for RetrospectiveModel |
| `viability` | np.ndarray | Viability scores for strategic voting models |
| `**kwargs` | — | Forwarded to individual model `compute_utility()` calls |

**Returns:** (n_voters, n_parties) utility matrix

**GPU Acceleration:** When `use_gpu=True`, the utility computation runs on GPU via CuPy for Proximity, Valence, and Retrospective models. Other models fall back to CPU with automatic CuPy array conversion. Creates significant speedup at large scales (>100K voters).

---

## ProximityModel

Standard spatial voting model. Utility decreases with ideological distance.

```python
ProximityModel(weight: float = 1.0, dimensionality: int = 2)
```

**Formula:** `U = -weight × distance(voter, party)`

**Example:**
```python
from electoral_sim import ProximityModel

model = ProximityModel(weight=2.0)  # Stronger distance penalty
```

---

## ValenceModel

Non-policy candidate appeal (charisma, competence, integrity).

```python
ValenceModel(weight: float = 0.01)
```

**Formula:** `U = weight × valence_score`

---

## RetrospectiveModel

Economic/retrospective voting. Rewards or punishes incumbents based on economic conditions.

```python
RetrospectiveModel(weight: float = 0.5)
```

**Parameters:**
- `weight` — Strength of economic effect

**Usage:**
```python
model = ElectionModel(
    n_voters=10_000,
    economic_growth=0.03,  # 3% growth helps incumbents
)
```

---

## StrategicVotingModel

Voters discount parties seen as unviable (Duverger's Law psychological effect).

```python
StrategicVotingModel(sensitivity: float = 1.0)
```

**Formula:** `U = sensitivity × log(viability)`

Low viability parties receive utility penalty, discouraging "wasted" votes.

---

## WastedVoteModel

Tactical voting with threshold-based penalty.

```python
WastedVoteModel(penalty: float = 2.0, viability_threshold: float = 0.05)
```

**Parameters:**
- `penalty` — Utility penalty for parties below threshold
- `viability_threshold` — Minimum vote share to be considered viable

**Example:**
```python
from electoral_sim import BehaviorEngine, ProximityModel, WastedVoteModel

engine = BehaviorEngine()
engine.add_model(ProximityModel())
engine.add_model(WastedVoteModel(penalty=3.0, viability_threshold=0.10))
```

---

## SociotropicPocketbookModel

Distinguishes between national (sociotropic) and personal (pocketbook) economic evaluations.

```python
SociotropicPocketbookModel(
    sociotropic_weight: float = 0.5,
    pocketbook_weight: float = 0.5
)
```

**Research basis:** Higher-educated voters tend to be more sociotropic (evaluate based on national economy), while lower-educated voters are more pocketbook-oriented (evaluate based on personal finances).

**Voter attribute:** Uses `economic_perception` column (0 = pocketbook, 1 = sociotropic).

---

## Campaign Models

Campaign-ecosystem models for finance, media, registration, mobilization, targeting, and polling access.

### CampaignFinance

Campaign spending-to-valence conversion with diminishing returns and incumbency advantage.

```python
from electoral_sim.behavior.campaign import CampaignFinance

cf = CampaignFinance(
    base_spending=1_000_000.0,
    incumbent_advantage=1.5,
    diminishing_factor=0.5,
)
```

**Parameters:**
- `base_spending` — Base campaign spending per party (monetary units, default 1,000,000)
- `incumbent_advantage` — Multiplier for incumbent fundraising (default 1.5)
- `diminishing_factor` — Diminishing returns exponent, <1 = steeper curve (default 0.5)

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `compute_spending(n_parties, incumbents, rng)` | np.ndarray | Compute per-party spending |
| `spending_to_valence(spending)` | np.ndarray | Convert spending to valence boost (diminishing returns) |
| `district_targeting(spending, n_districts, marginal_seats)` | np.ndarray | Allocate spending across districts |

---

### MediaEnvironment

Media exposure, sentiment, reach, and time-decay tracking. Also models misinformation susceptibility.

```python
from electoral_sim.behavior.campaign import MediaEnvironment

media = MediaEnvironment(
    base_exposure=0.5,
    sentiment_bias=0.0,
    reach_decay=0.95,
)

# Advance one media cycle
result = media.step(n_parties=4)
print(f"Exposure: {result['exposure']}, Sentiment: {result['sentiment']}, Reach: {result['reach']}")

# Estimate misinformation susceptibility
susceptibility = media.misinformation_susceptibility(media_diet=None)
```

**Parameters:**
- `base_exposure` — Base media exposure level 0-1 (default 0.5)
- `sentiment_bias` — Bias toward incumbents: -1 anti, +1 pro (default 0.0)
- `reach_decay` — Time-decay factor for past effects, <1 = fading (default 0.95)

**Methods:**
- `step(n_parties, incumbents, rng)` → dict with exposure, sentiment, reach
- `misinformation_susceptibility(media_diet)` → float 0-1

---

### CampaignTargeting

Local campaign resource allocation to constituencies based on marginal-seat value.

```python
from electoral_sim.behavior._campaign_models import CampaignTargeting

ct = CampaignTargeting(
    total_budget=100.0,
    marginal_weight=0.7,
    persuasion_decay=0.5,
)

# Allocate resources to districts by marginality
marginality = np.array([0.3, 0.1, 0.6])  # 3 districts
allocation = ct.allocate_resources(marginality)

# Convert spending to persuasion effect
effect = ct.persuasion_effect(allocation)
```

**Parameters:**
- `total_budget` — Total campaign resource pool (default 100.0)
- `marginal_weight` — Weight on marginal seats vs uniform allocation (default 0.7)
- `persuasion_decay` — Diminishing returns exponent for persuasion (default 0.5)

---

### VoterRegistration

Eligibility, registration, and turnout probability modeling.

```python
from electoral_sim.behavior._campaign_models import VoterRegistration

vr = VoterRegistration(
    eligible_rate=0.85,
    registration_rate=0.75,
    base_turnout=0.65,
    age_effect=0.1,
)

result = vr.compute_eligibility(n_voters=10000)
print(f"Eligible: {result['eligible'].mean():.1%}")
print(f"Registered: {result['registered'].mean():.1%}")
print(f"Will vote: {result['will_vote'].mean():.1%}")
```

**Parameters:**
- `eligible_rate` — Fraction of population eligible to vote (default 0.85)
- `registration_rate` — Fraction of eligible who register (default 0.75)
- `base_turnout` — Base turnout probability (default 0.65)
- `age_effect` — Age-driven turnout adjustment per 10 years (default 0.1)

---

### TurnoutMobilization

Canvassing, GOTV effects, and decomposition of turnout drivers.

```python
from electoral_sim.behavior._campaign_models import TurnoutMobilization

tm = TurnoutMobilization(
    base_turnout=0.65,
    canvass_effect=0.05,
    mobilization_effect=0.08,
)

breakdown = tm.decompose_turnout(
    baseline=0.65, alienation=0.05,
    indifference=0.03, mobilization=0.08
)
print(f"Total turnout: {breakdown['total']:.2f}")
```

**Parameters:**
- `base_turnout` — Baseline turnout rate (default 0.65)
- `canvass_effect` — Per-voter canvassing lift (default 0.05)
- `mobilization_effect` — GOTV campaign lift (default 0.08)

---

### PollingAccess

Distance, wait time, and registration friction effects on polling-place turnout.

```python
from electoral_sim.behavior._campaign_models import PollingAccess

pa = PollingAccess(
    distance_decay=0.1,
    wait_penalty=0.05,
    registration_friction=0.02,
)

distances = np.array([0.5, 2.0, 5.0])  # km
adjusted_turnout = pa.compute_turnout_adjustment(
    distances=distances, base_turnout=0.65
)
```

**Parameters:**
- `distance_decay` — Turnout drop per unit distance (default 0.1)
- `wait_penalty` — Turnout penalty per unit wait time (default 0.05)
- `registration_friction` — Constant turnout penalty (default 0.02)

---

## BehaviorModel Protocol

The `BehaviorModel` protocol class defines the interface for custom behavior models. Models must implement `compute_utility()`.

```python
from electoral_sim.behavior._models import BehaviorModel

class BehaviorModel:
    """Protocol for voter behavior models."""

    def compute_utility(
        self,
        *args,
        **kwargs,
    ) -> np.ndarray:
        """
        Compute a (n_voters, n_parties) utility matrix.

        Signature varies by model type:
        - ProximityModel: compute_utility(voter_positions, party_positions)
        - ValenceModel: compute_utility(n_voters, valence_array)
        - RetrospectiveModel: compute_utility(n_voters, n_parties, incumbents, growth)
        - StrategicVotingModel: compute_utility(n_voters, viability)
        - WastedVoteModel: compute_utility(n_voters, viability)

        All variants must return (n_voters, n_parties) ndarray.
        """
        ...
```

## Creating Custom Models

Implement the `BehaviorModel` protocol:

```python
from electoral_sim.behavior.voter_behavior import BehaviorModel
import numpy as np

class MyCustomModel:
    def __init__(self, strength: float = 1.0):
        self.strength = strength
    
    def compute_utility(
        self, 
        n_voters: int, 
        n_parties: int, 
        **kwargs
    ) -> np.ndarray:
        """Return (n_voters, n_parties) utility matrix."""
        # Your logic here
        return np.zeros((n_voters, n_parties))

# Use it
engine = BehaviorEngine()
engine.add_model(ProximityModel())
engine.add_model(MyCustomModel(strength=0.5))
```
