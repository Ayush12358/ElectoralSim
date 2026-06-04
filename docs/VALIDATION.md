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
