# Events & Timeline

Dynamic event management subsystem: scandals, economic shocks, election timelines, and synthetic poll generation.

## Event

Dataclass representing a dynamic event in the simulation.

```python
from electoral_sim.events.event_manager import Event

event = Event(
    id=0,
    type="scandal",
    start_step=5,
    duration=8,
    severity=25.0,
    target_party_id=2,
    description="Scandal hitting Party 2",
)
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Unique event identifier |
| `type` | `Literal["scandal", "economic_shock", "international_crisis"]` | Event category |
| `start_step` | int | Simulation step when the event begins |
| `duration` | int | Number of steps the event lasts |
| `severity` | float | Impact magnitude (0-50+ for scandals, ±5.0 for shocks) |
| `target_party_id` | int \| None | Party targeted (or None for economy-wide) |
| `description` | str | Human-readable event description |

**Property:**
- `end_step` → `int`: Computed as `start_step + duration`.

---

## EventManager

Manages generation, tracking, and expiration of dynamic events during a simulation.

```python
from electoral_sim.events.event_manager import EventManager

manager = EventManager(
    rng=np.random.default_rng(42),
    prob_scandal=0.01,
    prob_shock=0.005,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rng` | `np.random.Generator` | *required* | Random number generator |
| `prob_scandal` | float | `0.01` | Per-step probability of a scandal |
| `prob_shock` | float | `0.005` | Per-step probability of an economic shock |

**Attributes:**
- `active_events` — List of currently active `Event` objects
- `history` — List of all past events

### step

```python
def step(self, n_parties: int) -> list[Event]
```

Advance one step: expire old events, possibly generate new scandals/shocks.

**Returns:** List of newly generated events this step.

**Example:**
```python
# Run a campaign timeline with events
for step in range(30):
    new = manager.step(n_parties=5)
    for e in new:
        print(f"Step {step}: {e.description}")
```

### get_valence_modifiers

```python
def get_valence_modifiers(self) -> dict[int, float]
```

Get total valence penalty/bonus for each party from active scandal events. Penalty decays linearly over the event's duration.

**Returns:** Dict mapping party ID → net valence modifier.

### get_economic_modifier

```python
def get_economic_modifier(self) -> float
```

Get total modification to economic growth from active economic shocks. Shocks decay linearly over duration.

**Returns:** Net economic shock value (positive for booms, negative for crashes).

---

## ElectionTimeline

Discrete-event campaign/election timeline for scheduling campaign phases, polls, debates, and election day.

```python
from electoral_sim.events.timeline import ElectionTimeline

timeline = ElectionTimeline(
    total_steps=30,
    campaign_start=5,
    debate_steps=[10, 20],
    poll_steps=[8, 15, 25],
    election_day=30,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `total_steps` | int | `30` | Total time steps in the election cycle |
| `campaign_start` | int | `5` | Step when campaigning begins |
| `debate_steps` | list[int] \| None | `[10, 20]` | Steps at which debates occur |
| `poll_steps` | list[int] \| None | `[8, 15, 25]` | Steps at which polls are taken |
| `election_day` | int \| None | `total_steps` | Step of the election |

### step

```python
def step(self) -> dict
```

Advance one time step and return any events triggered.

**Returns:** Dict with `step` (current step) and `events` (list of triggered event dicts).

### is_election_day

```python
def is_election_day(self) -> bool
```

Return `True` if the current step is election day.

### simulate_poll

```python
def simulate_poll(
    self,
    n_parties: int,
    rng: np.random.Generator | None = None,
) -> np.ndarray
```

Generate a synthetic poll with sampling error via Dirichlet distribution + Gaussian noise.

**Returns:** `(n_parties,)` poll results as normalized vote shares.

---

## PollGenerator

Synthetic poll generation with house effects, sampling error, likely-voter screens, nonresponse, and correlated misses.

```python
from electoral_sim.events.timeline import PollGenerator

polls = PollGenerator(
    sample_size=1000,
    house_effect=0.0,
    moe=0.03,
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sample_size` | int | `1000` | Poll sample size |
| `house_effect` | float | `0.0` | Pollster's systematic bias (-0.05 to +0.05) |
| `moe` | float | `0.03` | Margin of error (default 3pp) |

### generate_poll

```python
def generate_poll(
    self,
    true_shares: np.ndarray,
    rng: np.random.Generator | None = None,
) -> dict
```

Generate a poll from true vote shares with realistic error modeling.

**Returns:** Dict with `poll_shares`, `sample_size`, `moe`, `house_effect`.

**Example:**
```python
import numpy as np

true_votes = np.array([0.40, 0.30, 0.15, 0.10, 0.05])
poll = polls.generate_poll(true_votes)
for i, share in enumerate(poll["poll_shares"]):
    print(f"Party {i}: {share*100:.1f}%")
```
