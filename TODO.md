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

---

## 3. Foundational Citations Added (for academic rigor)
**Status:** ✅ Added to `references.bib`, ⚠️ Need integration into main text

| Citation | Topic | Where to Cite |
|----------|-------|---------------|
| **Warwick (1994)** | Government Survival | Justifies L=5.5 in MTTF formula |
| **Tsebelis (2002)** | Veto Players | Explains why fragmentation → instability |
| **Laver & Shepsle (1996)** | Cabinet Formation | Already cited, connects to Patronage |

**Paper sections to update:**
- [ ] Methodology: Cite Warwick for MTTF calibration rationale
- [ ] Discussion (Fragmentation): Frame as "Veto Player simulator" per Tsebelis
- [ ] Appendix (MTTF Constants): Add Warwick citation for L=5.5 justification

---

## 4. ABM Methodology Enhancement
**Status:** ❌ Not yet in paper

**What to add:**
- [ ] **ODD Protocol** (Overview, Design concepts, Details) — standard for ABM papers
- [ ] **Agent decision rules** — explicit pseudocode for voter behavior
- [ ] **Initialization** — how parties/voters are generated
- [ ] **Scheduling** — order of operations per simulation step
- [ ] **Calibration** — how parameters were chosen/validated
- [ ] **Sensitivity analysis** — already partly done with Minkowski/collapse

**Why it matters:**
- Reviewers expect ODD or similar structured ABM description
- Makes simulation reproducible without reading code
- Standard practice in JASSS, Computational Social Science journals

**References to cite:**
- Grimm et al. (2006, 2010): ODD Protocol papers
- Wilensky & Rand (2015): Agent-Based Modeling textbook
