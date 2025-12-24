# mesa-frames Contribution Ideas

> Gaps and improvement suggestions identified while building ElectoralSim.
> Potential GSoC/contribution opportunities.

---

## 🔴 Missing Features (High Impact)

### 1. Network/Graph Space Support
- **Current:** mesa-frames lacks spatial/network support
- **Need:** Agents connected via NetworkX graph for opinion dynamics
- **Proposal:** `NetworkAgentSet` that tracks neighbor relationships in DataFrame
- **Complexity:** Medium-High

### 2. Lazy Evaluation Integration
- **Current:** Operations are eager (immediate execution)
- **Roadmap item:** Transition to LazyFrames
- **Benefit:** Query optimization, reduced memory for large models
- **Complexity:** High

### 3. Multi-AgentSet Interactions
- **Current:** Each AgentSet is independent
- **Need:** Voters interacting with Candidates, Media influencing Voters
- **Proposal:** Cross-set query methods, relationship tracking
- **Complexity:** Medium

---

## 🟡 API Improvements (Medium Impact)

### 4. Better Selection/Filtering API
- **Current:** `self.select()` is basic
- **Need:** Chained selections, constituency-based filtering
- **Proposal:** 
  ```python
  self.select(constituency=5).select(knowledge > 50).do("vote")
  ```

### 5. Batch Agent Creation
- **Current:** Add agents via DataFrame
- **Need:** Efficient batch creation with distributions
- **Proposal:**
  ```python
  agents.add_batch(n=1_000_000, 
                   ideology=Normal(0, 0.3),
                   constituency=Uniform(0, 543))
  ```

### 6. Time-Series Data Collection
- **Current:** Manual result tracking
- **Need:** Built-in data collection like Mesa's DataCollector
- **Proposal:** `model.datacollector.collect()` with Polars backend

---

## 🟢 Documentation & Examples (Community)

### 7. Real-World Examples
- **Current:** Only Boltzmann/Sugarscape examples
- **Need:** Voting models, epidemics, market simulations
- **Contribution:** Add electoral simulation as example

### 8. Performance Guide
- **Current:** Limited benchmarking docs
- **Need:** Best practices for 1M+ agent models
- **Topics:** Memory management, chunking, when to use lazy

### 9. Migration Guide
- **Current:** No classic Mesa → mesa-frames migration docs
- **Need:** Step-by-step porting guide with patterns

---

## 🔵 Advanced Features (Future)

### 10. GPU Acceleration
- **Roadmap item:** Already planned
- **Our use case:** 10M+ voters would benefit massively

### 11. Distributed Computing
- **Current:** Single-machine only
- **Need:** Dask/Ray integration for cluster computing
- **Use case:** Full India simulation (970M voters)

### 12. Visualization Integration  
- **Current:** No built-in viz for mesa-frames
- **Need:** SolaraViz adapter or Plotly integration
- **Proposal:** Real-time dashboard for large simulations

---

## 📋 Specific Issues We Encountered

| Issue | Description | Workaround |
|-------|-------------|------------|
| No neighbor access | Can't get network neighbors in AgentSet | Manual NetworkX integration |
| Sampling is slow | `df.sample()` for random interactions | Pre-compute random indices |
| No constituency grouping | Can't easily simulate per-district | Manual `group_by` |

---

## 🎯 Suggested Contribution Order

1. **Documentation** — Low barrier, high impact
2. **Electoral simulation example** — Showcase real use case
3. **NetworkAgentSet** — Core feature gap
4. **DataCollector for mesa-frames** — Essential for research

---

## 📚 Resources

- mesa-frames repo: https://github.com/mesa/mesa-frames
- mesa-frames roadmap: https://github.com/mesa/mesa-frames/blob/main/mesa-frames/roadmap
- Polars docs: https://docs.pola.rs/

---

*Last updated: 2024-12-24*
