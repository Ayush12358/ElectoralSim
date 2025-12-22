# TODO: Paper Updates

## Pending Experiments to Add to `main.tex`

### 1. Minkowski Distance Sensitivity Analysis
**Status:** ✅ Implemented in code, ❌ Not yet in paper

**What was added:**
- Minkowski distance with parameter `p` (1 to 5)
- p=1: Manhattan distance (L1 norm)
- p=2: Euclidean distance (L2 norm) — current default
- p=3,4,5: Higher-order norms

**Why it matters:**
- Tests whether ideological "distance" is best measured by:
  - Sum of differences (p=1)
  - Geometric distance (p=2)
  - Maximum disagreement (p→∞)

**Paper sections to update:**
- [ ] Methodology: Add description of Minkowski parameter
- [ ] Results: Add figure showing MTTF vs Minkowski p
- [ ] Discussion: Interpret which distance metric best predicts stability

---

### 2. Collapse Model Comparison
**Status:** ✅ Implemented in code, ❌ Not yet in paper

**What was added:**
- Three MTTF decay models:
  1. **Sigmoid** (current): Phase transition / tipping point
  2. **Linear**: Gradual proportional decay
  3. **Exponential**: Early risk is most damaging

**Why it matters:**
- Tests whether government collapse is:
  - A sudden phase transition (sigmoid)
  - A gradual erosion (linear)
  - Front-loaded risk (exponential)

**Paper sections to update:**
- [ ] Methodology: Add description of collapse models
- [ ] Results: Add figure comparing model predictions
- [ ] Discussion: Which model best matches empirical data?
- [ ] Appendix: Add formulas for all three models

---

## CSV Output Changes

The simulation now outputs:
```
dimensions,n_parties,threshold,patronage,polarization,minkowski_p,collapse_model,avg_mttf,avg_gallagher,std_mttf
```

Total configurations: 4 dims × 4 parties × 3 thresholds × 4 patronage × 3 polarization × 5 minkowski × 3 collapse = **8,640 configs**
With 30 trials each = **259,200 simulation runs**

---

## When to Add to Paper

After running the full simulation and analyzing results:
1. Generate new figures with `python visualize_results.py`
2. Update `main.tex` with new sections
3. Update `references.bib` if new citations needed
