# mesa-frames Documentation Reference

> Saved from: https://github.com/mesa/mesa-frames
> Date: 2024-12-24

## Overview

mesa-frames reimagines Mesa agent storage using **Polars DataFrames**, so agents live in a columnar store rather than the Python heap. You keep the Mesa-style Model/AgentSet structure, but updates are vectorized and memory-efficient.

## Why mesa-frames?

- ⚡ **10× faster** bulk updates on 10k+ agents
- 📊 **Columnar execution** via Polars: SIMD ops, multi-core support
- 🔄 **Declarative logic**: agent rules as transformations, not Python loops
- 🚀 **Roadmap**: Lazy queries and GPU support

## Who is it for?

- Researchers needing to scale to tens or hundreds of thousands of agents
- Users whose agent logic can be written as vectorized, set-based operations

**❌ Not a good fit if**: your model depends on strict per-agent sequencing, complex non-vectorizable methods, or fine-grained identity tracking.

## Installation

```bash
pip install mesa-frames
```

## Quick Start Example

```python
from mesa_frames import AgentSet, Model
import polars as pl

class MoneyAgents(AgentSet):
    def __init__(self, n: int, model: Model):
        super().__init__(model)
        # Add agents via DataFrame
        self += pl.DataFrame({"wealth": pl.ones(n, eager=True)})

    def give_money(self):
        # Select agents with wealth > 0
        self.select(self.wealth > 0)
        
        # Sample random recipients
        other_agents = self.df.sample(n=len(self.active_agents), with_replacement=True)
        
        # Vectorized update: give $1 to random agent
        self["active", "wealth"] -= 1
        new_wealth = other_agents.group_by("unique_id").len()
        self[new_wealth, "wealth"] += new_wealth["len"]

    def step(self):
        self.do("give_money")


class MoneyModelDF(Model):
    def __init__(self, N: int):
        super().__init__()
        self.sets += MoneyAgents(N, self)

    def step(self):
        self.sets.do("step")
```

## Key Concepts

### AgentSet
- Stores agents as Polars DataFrame
- Supports vectorized operations via `self.df`
- Use `self.select()` to filter active agents
- Use `self["column"]` or `self["mask", "column"]` for updates

### Model
- Container for AgentSets
- Use `self.sets += AgentSet(...)` to add agent groups
- Use `self.sets.do("method")` to call methods on all sets

## Benchmarks

| Model | Classic Mesa | mesa-frames | Speedup |
|-------|-------------|-------------|---------|
| Boltzmann (10k agents) | ~10s | ~1s | **10×** |
| Sugarscape | 2× baseline | baseline | **2×** |

mesa-frames maintains near-constant runtimes even as agent count rises.

## Roadmap

- Transition to LazyFrames for optimization and GPU support
- Auto-vectorize existing Mesa models via decorator
- Increase possible Spaces (Network, Continuous...)
- Refine the API to align to Mesa

## Resources

- GitHub: https://github.com/mesa/mesa-frames
- Docs: https://mesa.github.io/mesa-frames
- Polars: https://docs.pola.rs/

## License

Apache License 2.0
