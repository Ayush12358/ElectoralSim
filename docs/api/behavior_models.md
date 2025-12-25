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
