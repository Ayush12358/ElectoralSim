# Redistricting

Redistricting module — inspired by GerryChain. Provides precinct/constituency graph representation, district assignment tracking, population balance checking, contiguity validation, ReCom-style proposal generation, and ensemble analysis.

> **Note:** Heavy GIS dependencies are kept optional under a `'geo'` extra.

## PrecinctGraph

Represents a precinct/constituency adjacency graph for redistricting. Nodes are precincts; edges represent geographic adjacency.

```python
from electoral_sim.analysis.redistricting import PrecinctGraph
import numpy as np

graph = PrecinctGraph(
    n_precincts=100,
    adj_list=adjacency,
    populations=populations,
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `n_precincts` | int | Number of precincts |
| `adj_list` | `list[list[int]] \| None` | Adjacency list (neighbor indices per precinct) |
| `populations` | `np.ndarray \| None` | Precinct populations (default: all ones) |

**Attributes:**
- `n_precincts` — Number of precincts
- `adj_list` — Adjacency list
- `populations` — Population per precinct
- `assignment` — Current district assignment array

### assign_districts

```python
def assign_districts(self, assignment: np.ndarray)
```

Set the district assignment for all precincts. Raises `ValueError` if length mismatches `n_precincts`.

### population_balance

```python
def population_balance(self, n_districts: int) -> dict[str, float]
```

Compute population balance statistics across districts.

**Returns:** Dict with keys:
| Key | Description |
|-----|-------------|
| `ideal_population` | Target population per district |
| `max_deviation` | Maximum absolute fractional deviation |
| `min_deviation` | Minimum fractional deviation |
| `total_population` | Total population |

**Example:**
```python
graph.assign_districts(district_plan)
balance = graph.population_balance(n_districts=5)
print(f"Max deviation: {balance['max_deviation']:.2%}")
```

### check_contiguity

```python
def check_contiguity(self) -> list[int]
```

Check which precincts are disconnected from their district's main component using BFS flood-fill.

**Returns:** List of disconnected precinct indices (empty if all districts are contiguous).

---

## recom_proposal

ReCom-style spanning-tree recombination for adjacent districts. Merges two adjacent districts, builds a spanning tree over the merged region, and cuts a balanced edge to create a new district assignment.

```python
from electoral_sim.analysis.redistricting import recom_proposal

new_assignment = recom_proposal(
    graph=graph,
    dist_a=0,
    dist_b=1,
    rng=np.random.default_rng(42),
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `graph` | `PrecinctGraph` | Graph with current district assignments |
| `dist_a` | int | First district ID |
| `dist_b` | int | Second (adjacent) district ID |
| `rng` | `np.random.Generator \| None` | Random generator |

**Returns:** New assignment array, or `None` if recombination fails (e.g., districts not adjacent or spanning tree empty).

**Algorithm:**
1. Collect precincts from both districts
2. Build internal adjacency for the merged region
3. Generate random spanning tree via BFS with random neighbor ordering
4. Remove one random edge to split the tree
5. Reconstruct two new districts from the cut tree

**Example:**
```python
import numpy as np
from electoral_sim.analysis.redistricting import PrecinctGraph, recom_proposal

# Create a simple 4-precinct graph
adj = [[1], [0, 2], [1, 3], [2]]
pops = np.array([100, 200, 150, 180])
graph = PrecinctGraph(4, adj, pops)
graph.assign_districts(np.array([0, 0, 1, 1]))

# Try recombination
rng = np.random.default_rng(42)
new = recom_proposal(graph, 0, 1, rng)
if new is not None:
    graph.assign_districts(new)
    print(graph.assignment)
```

---

## ensemble_analysis

Compare an enacted district plan against a simulated ensemble of alternative plans.

```python
from electoral_sim.analysis._ensemble import ensemble_analysis

result = ensemble_analysis(
    graph=graph,
    enacted_assignment=enacted_plan,
    n_plans=100,
    rng=np.random.default_rng(42),
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `graph` | `PrecinctGraph` | Graph with population data |
| `enacted_assignment` | `np.ndarray` | The actual/enacted district assignment |
| `n_plans` | int | Number of simulated plans to generate (default `100`) |
| `rng` | `np.random.Generator \| None` | Random generator |

**Returns:** Dict with:
| Key | Description |
|-----|-------------|
| `enacted_max_deviation` | Max population deviation of enacted plan |
| `ensemble_mean` | Mean max deviation across ensemble |
| `ensemble_std` | Standard deviation of ensemble max deviations |
| `ensemble_min` | Minimum max deviation in ensemble |
| `ensemble_max` | Maximum max deviation in ensemble |
| `enacted_percentile` | Percentile rank of enacted plan within ensemble (0-1) |
| `n_plans` | Number of plans generated |

**Example:**
```python
result = ensemble_analysis(graph, enacted_plan, n_plans=500)
if result["enacted_percentile"] > 0.95:
    print("Warning: enacted plan is an outlier (>95th percentile)")
else:
    print(f"Enacted plan at {result['enacted_percentile']:.1%} — within ensemble range")
```
