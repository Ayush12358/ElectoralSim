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
| `use_zealots` | bool | False | Apply zealot constraints after step |

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

---

## Additional Methods

### simulate

Run multiple steps and return opinion history.

```python
initial_opinions = rng.choice([0, 1, 2], size=1000)  # 3-party discrete
history = od.simulate(
    initial_opinions=initial_opinions,
    n_steps=100,
    model="noisy_voter",
    noise_rate=0.02,
)
# history[0] = initial, history[100] = after 100 steps
```

**Parameters:**
- `initial_opinions` — Starting opinion array
- `n_steps` — Number of steps to simulate (default 100)
- `model` — "noisy_voter" or "bounded_confidence"
- `**kwargs` — Forwarded to `step()`

**Returns:** List of opinion arrays, one per step (length n_steps + 1)

---

### set_zealots

Mark certain agents as zealots with fixed, unchanging opinions.

```python
zealot_indices = np.array([0, 5, 10, 15])
od.set_zealots(indices=zealot_indices, opinions=current_opinions)
# These agents now maintain their current opinion indefinitely
```

**Parameters:**
- `indices` — Agent indices to mark as zealots
- `opinions` — Current opinion array (zealots capture their current positions)

---

### get_opinion_shares

Calculate the distribution of opinions across discrete categories.

```python
opinions = np.array([0, 0, 1, 2, 1, 0, 2])  # Party IDs
shares = od.get_opinion_shares(opinions=opinions, n_parties=3)
print(shares)  # [0.428, 0.286, 0.286]
```

**Parameters:**
- `opinions` — Integer opinion/party array
- `n_parties` — Number of discrete categories

**Returns:** (n_parties,) array of shares summing to 1

---

## Standalone Step Functions

These functions operate on raw adjacency lists without requiring an OpinionDynamics instance.

### noisy_voter_step

```python
from electoral_sim.dynamics.opinion_dynamics import noisy_voter_step

adj_list = [[1, 2], [0, 2], [0, 1]]  # 3-agent triangle
opinions = np.array([0, 1, 2])

new_opinions = noisy_voter_step(
    opinions=opinions,
    adj_list=adj_list,
    noise_rate=0.01,
    rng=np.random.default_rng(42),
)
```

**Parameters:**
- `opinions` — Current discrete opinion/party array
- `adj_list` — List of neighbor lists per agent
- `noise_rate` — Probability of random mutation (default 0.01)
- `rng` — Random generator

**Returns:** Updated opinions array (same shape)

---

### bounded_confidence_step

```python
from electoral_sim.dynamics.opinion_dynamics import bounded_confidence_step

opinions = np.random.uniform(-1, 1, 1000)  # Continuous [-1, 1]

new_opinions = bounded_confidence_step(
    opinions=opinions,
    adj_list=adj_list,
    epsilon=0.3,      # Only interact if |opinion_i - opinion_j| < epsilon
    mu=0.5,           # Convergence rate
    rng=np.random.default_rng(42),
)
```

**Parameters:**
- `opinions` — Continuous opinions in [-1, 1]
- `adj_list` — Network adjacency list
- `epsilon` — Confidence bound: only interact if difference < epsilon (default 0.3)
- `mu` — Convergence rate toward neighbor (default 0.5)
- `rng` — Random generator

**Returns:** Updated opinions, clipped to [-1, 1]

---

### zealot_step

```python
from electoral_sim.dynamics.opinion_dynamics import zealot_step

zealot_mask = np.zeros(1000, dtype=bool)
zealot_mask[:50] = True  # First 50 agents are zealots

new_opinions = zealot_step(
    opinions=opinions,
    adj_list=adj_list,
    zealot_mask=zealot_mask,
    noise_rate=0.01,
    rng=np.random.default_rng(42),
)
```

**Parameters:**
- `opinions` — Current opinions
- `adj_list` — Network adjacency list
- `zealot_mask` — Boolean mask marking zealot agents
- `noise_rate` — Mutation probability (default 0.01)
- `rng` — Random generator

**Returns:** Updated opinions with zealots unchanged

---

## Network Utilities

### generate_network

Generate social network topologies as adjacency lists.

```python
from electoral_sim.dynamics._networks import generate_network

# All available topologies
adj_list, graph = generate_network(
    n_agents=1000,
    topology="barabasi_albert",  # or "watts_strogatz", "erdos_renyi", "random_regular"
    m=3,     # BA: edges per new node
    # k=4,   # WS: neighbors per node
    # p=0.1, # WS/ER: rewiring/edge probability
    # d=4,   # RR: degree
)
```

**Parameters:**
- `n_agents` — Number of nodes
- `topology` — "barabasi_albert", "watts_strogatz", "erdos_renyi", or "random_regular"
- `**kwargs` — Topology-specific parameters (m, k, p, d)

**Returns:** (adj_list, NetworkX graph)

**Dependency:** Requires NetworkX. The constant `NETWORKX_AVAILABLE` (from `electoral_sim.dynamics._networks`) indicates availability.

---

### network_stats

Compute basic network statistics (nodes, edges, degree, clustering).

```python
from electoral_sim.dynamics._networks import network_stats

stats = network_stats(graph)
print(f"Nodes: {stats['n_nodes']}, Edges: {stats['n_edges']}")
print(f"Avg degree: {stats['avg_degree']:.1f}")
print(f"Clustering: {stats['clustering_coeff']:.3f}")
```

**Returns:** Dict with `n_nodes`, `n_edges`, `avg_degree`, `max_degree`, `clustering_coeff`

---

### network_diagnostics

Comprehensive diagnostics: degree distribution, components, homophily, influence concentration.

```python
from electoral_sim.dynamics._networks import network_diagnostics

diag = network_diagnostics(graph, opinions=opinions)
print(f"Components: {diag['connected_components']}")
print(f"Largest component: {diag['largest_component_size']}")
print(f"Homophily: {diag['homophily']:.3f}")
print(f"Influence Gini: {diag['influence_gini']:.3f}")
```

**Parameters:**
- `graph` — NetworkX graph
- `opinions` — Optional opinion vector for homophily computation

**Returns:** Dict with `degree_distribution` (mean/std/median/max), `clustering_coefficient`, `connected_components`, `largest_component_size`, `homophily`, `influence_gini`
