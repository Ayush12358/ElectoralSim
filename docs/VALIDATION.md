# Real-World Validation Cases

> Comparison of ElectoralSim outputs against actual election results for calibration purposes.

---

## Germany 2021 Bundestag

### Status
🔶 **Framework ready — needs real election data to populate.** The simulation can be run with the `germany` preset and produces plausible outputs, but party positions and valence are synthetic defaults, not calibrated.

### How to validate
1. **Source data**: Official results from [Bundeswahlleiter](https://www.bundeswahlleiter.de/bundestagswahlen/2021.html)
2. **What to compare**: 
   - Vote shares by party
   - Seat shares by party (after Sainte-Laguë allocation)
   - Gallagher disproportionality index
   - Effective Number of Parties (ENP votes, ENP seats)
   - Turnout rate
3. **Simulation setup**:
```python
from electoral_sim import ElectionModel

model = ElectionModel.from_preset("germany", n_voters=50_000, seed=2021)
results = model.run_election()
print(f"Gallagher: {results['gallagher']:.2f}")
print(f"ENP votes: {results['enp_votes']:.2f}")
print(f"ENP seats: {results['enp_seats']:.2f}")
print(f"Turnout: {results['turnout']:.1%}")

# Compare with actual 2021 results:
# SPD: 25.7% → ENP ~4.5
# CDU/CSU: 24.1%
# Greens: 14.8%
# FDP: 11.5%
# AfD: 10.3%
# Linke: 4.9%
```
4. **Metric**: Mean Absolute Error (MAE) in vote shares, seat shares
5. **Calibration**: Adjust party positions, valence values, and regional weights to minimize MAE

### Template for results
```markdown
| Party | Actual Vote % | Simulated Vote % | Error |
|-------|--------------|-----------------|-------|
| SPD | 25.7 | - | - |
| CDU/CSU | 24.1 | - | - |
| Grüne | 14.8 | - | - |
| FDP | 11.5 | - | - |
| AfD | 10.3 | - | - |
| Linke | 4.9 | - | - |

MAE: -%
Gallagher (actual): - | Gallagher (simulated): -
```

---

## UK 2019 House of Commons

### Status
🔶 **Framework ready — needs real election data.**

### Source
[UK Electoral Commission](https://www.electoralcommission.org.uk/) or [House of Commons Library](https://commonslibrary.parliament.uk/).

---

## USA 2024 House of Representatives

### Status
🔶 **Framework ready — needs real election data.**

### Source
[MIT Election Data + Science Lab](https://electionlab.mit.edu/data) or [Dave Leip's Atlas](https://uselectionatlas.org/).

---

## 2024 India Lok Sabha

### Status
🔶 **Framework ready — needs real election data.**

### Source
[Election Commission of India](https://results.eci.gov.in/)

---

## Notes
- ElectoralSim is a **simulation toolkit**, not a forecasting model
- Presets currently use **synthetic defaults** for party positions and valence
- Calibration requires: (1) real election results, (2) survey data for party positioning, (3) iterative parameter adjustment
- Contributions of calibrated presets are welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## Posterior Predictive Validation & "Not a Forecast" Positioning

### What Can Be Inferred

| Preset Type | Valid Inferences |
|-------------|-----------------|
| **Structural demo** | Electoral system mechanics (FPTP vs PR effects), Duverger tendencies, coalition formation patterns, system-level comparisons |
| **Partially calibrated** | Directional effects of parameter changes, sensitivity analysis, "what-if" scenario exploration |
| **Historically calibrated** | Retrospective fit quality, model adequacy for specific elections, within-sample validation |
| **Validation-only** | Out-of-sample prediction assessment, generalization to unseen elections, calibrated uncertainty bounds |

### What Cannot Be Inferred

- ❌ ElectoralSim is **not an election forecasting model** — it does not predict future outcomes
- ❌ **Structural demos cannot** be used to claim accuracy for any specific country
- ❌ **Synthetic party positions and valence** are for demonstration — not derived from surveys or expert coding
- ❌ **Calibrated presets** are retrospective fits, not predictive models

### Acceptance Criteria for Calibration Status Upgrade

**From structural demo → partially calibrated:**
- [ ] Party positions sourced from expert surveys (e.g., Chapel Hill Expert Survey, Manifesto Project) OR voter perception data
- [ ] Valence parameters informed by candidate/party approval data
- [ ] Turnout calibrated to within ±5pp of historical turnout
- [ ] At least one metric (Gallagher, ENP) validated against known election results

**From partially calibrated → historically calibrated:**
- [ ] Multiple metrics validated against historical election results
- [ ] Parameter sensitivity analysis performed and documented
- [ ] Calibration methodology documented (loss function, optimization method, parameter bounds)
- [ ] Reproducibility: same seed, same config → same results (deterministic)

**From historically calibrated → validation-only:**
- [ ] Out-of-sample validation on at least one held-out election
- [ ] Uncertainty quantification (confidence intervals, Monte Carlo SE) reported
- [ ] Predictive distribution compared to actual results with proper scoring rules

---

## Calibration Procedure

ElectoralSim provides a `grid_search_calibration` function for systematic parameter tuning.
To calibrate a preset against real election results:

```python
from electoral_sim.analysis import grid_search_calibration
from electoral_sim import ElectionModel

# grid_search_calibration passes param_grid dict keys as **kwargs to model_class()
# so parameters like n_voters and temperature go inside param_grid
results = grid_search_calibration(
    model_class=ElectionModel,
    param_grid={
        "n_voters": [50000],
        "temperature": [0.1, 0.3, 0.5, 0.7],
        "threshold": [0.0, 0.03, 0.05],
    },
    targets={
        "gallagher": 3.5,       # From real election results
        "enp_votes": 4.5,
        "turnout": 0.76,
    },
    metric_weights={"gallagher": 1.0, "enp_votes": 0.5, "turnout": 0.5},
    n_runs=3,
    seed=2021,
)
print(f"Best params: {results[0]['params']}")
print(f"Best loss: {results[0]['loss']:.4f}")

# Note: grid_search_calibration does not use from_preset().
# For preset-based calibration, create the config manually:
# config = ElectionModel.from_preset("germany").config
# Then pass config fields through param_grid.
```

### Workflow
1. Choose a preset and find real election reference data (vote shares, turnout, Gallagher)
2. Define a parameter grid around plausible values (temperature, threshold, party positions)
3. Run `grid_search_calibration` to find best-fitting parameters
4. Update the preset's `config.py` with calibrated positions and valence
5. Update preset provenance in `PRESET_PROVENANCE` to track calibration status
6. Populate the validation tables above with actual vs simulated comparisons
