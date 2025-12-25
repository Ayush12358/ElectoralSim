# Opinion Dynamics

Social network-based opinion evolution system.

## OpinionDynamics

Creates and manages social networks for voter opinion evolution.

```python
from electoral_sim import OpinionDynamics

od = OpinionDynamics(
    n_agents=10_000,
    topology="barabasi_albert",
    m=3,  # edges per new node
    seed=42
)
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n_agents` | int | required | Number of agents in network |
| `topology` | str | "barabasi_albert" | Network type |
| `m` | int | 3 | BA: edges per new node |
| `k` | int | 4 | WS: each node connected to k neighbors |
| `p` | float | 0.1 | WS/ER: rewiring/edge probability |
| `seed` | int | None | Random seed |

### Network Topologies

#### Barabási-Albert (Scale-Free)
Realistic social network structure with hubs.
```python
od = OpinionDynamics(n_agents=1000, topology="barabasi_albert", m=3)
```

#### Watts-Strogatz (Small World)
High clustering with short path lengths.
```python
od = OpinionDynamics(n_agents=1000, topology="watts_strogatz", k=4, p=0.1)
```

#### Erdős-Rényi (Random)
Random graph with specified edge probability.
```python
od = OpinionDynamics(n_agents=1000, topology="erdos_renyi", p=0.01)
```

---

## step Method

Evolve opinions by one time step.

```python
new_opinions = od.step(
    opinions,
    model="bounded_confidence",
    epsilon=0.3,
    media_bias=0.0,
    media_strength=0.1,
    system="FPTP"
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `opinions` | np.ndarray | required | Current opinion values |
| `model` | str | "bounded_confidence" | Opinion dynamics model |
| `epsilon` | float | 0.3 | BC: confidence threshold |
| `media_bias` | float/array | 0.0 | Media broadcast position |
| `media_strength` | float | 0.1 | Media influence strength |
| `system` | str | "PR" | Electoral system (affects susceptibility) |

---

## Opinion Models

### Bounded Confidence

Agents only influence each other if opinions are within threshold ε.

```python
opinions = od.step(opinions, model="bounded_confidence", epsilon=0.3)
```

**Dynamics:** If `|opinion_i - opinion_j| < epsilon`, agents move toward each other.

### Noisy Voter

Random neighbor copying with mutation.

```python
opinions = od.step(opinions, model="noisy_voter", mutation_rate=0.01)
```

**Dynamics:** With probability p, copy random neighbor's opinion. With probability mutation_rate, randomly change.

---

## Media Effects

### Scalar Media Bias

All agents receive same media signal.

```python
opinions = od.step(
    opinions,
    media_bias=0.5,      # Right-leaning media
    media_strength=0.1   # 10% influence per step
)
```

### Vectorized Media Bias

Agent-specific media diet (from voter `media_bias` column).

```python
# Different media for each agent
media_bias_vector = np.array([-0.5] * 500 + [0.5] * 500)

opinions = od.step(
    opinions,
    media_bias=media_bias_vector,
    media_strength=0.1
)
```

### Raducha Susceptibility

FPTP voters are more susceptible to media/waves than PR voters.

```python
# FPTP: 1.5x media effect
opinions_fptp = od.step(opinions, system="FPTP", media_bias=0.5, media_strength=0.1)

# PR: 1.0x media effect  
opinions_pr = od.step(opinions, system="PR", media_bias=0.5, media_strength=0.1)
```

---

## Integration with ElectionModel

```python
from electoral_sim import ElectionModel, OpinionDynamics

# Create social network
od = OpinionDynamics(n_agents=10_000, topology="barabasi_albert", m=3)

# Create model with opinion dynamics
model = ElectionModel(
    n_voters=10_000,
    opinion_dynamics=od,
    seed=42
)

# Run simulation with opinion evolution
for _ in range(100):
    model.step()  # Opinions evolve

# Run election with evolved opinions
results = model.run_election()
```

---

## Zealots

Fixed-opinion agents that never change.

```python
# Mark 5% as zealots (won't change opinion)
zealot_mask = np.random.rand(1000) < 0.05
zealot_opinions = np.where(zealot_mask, 1.0, opinions)  # Fixed at 1.0

# Zealots maintain their position
new_opinions = od.step(zealot_opinions, model="bounded_confidence")
new_opinions[zealot_mask] = 1.0  # Restore zealot positions
```
