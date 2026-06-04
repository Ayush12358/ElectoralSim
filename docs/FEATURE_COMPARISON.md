# Feature Comparison with Other Electoral Simulators

> Research findings: features from other open-source electoral simulation projects that may inform ElectoralSim's roadmap.

---

## Johnh865/election_sim

- Electoral college simulation (US-focused)
- Interactive web-based exploration
- Swing state sensitivity analysis
- **Potential features to adopt**: Electoral college weight model, swing state analysis

## endolith/elsim

- Python-based electoral simulation
- Gerrymandering analysis focus
- District drawing and efficiency gap measurement
- **Potential features to adopt**: Advanced gerrymandering metrics, district-level efficiency gap

## ElectionSim (arXiv)

- Academic paper describing multi-agent electoral modeling
- Focus on emergent behavior in multi-party systems
- Uses agent-based approach similar to ElectoralSim
- **Potential features to adopt**: Enhanced multi-party dynamics, emergent party system formation

## es_simulations

- Lightweight electoral system comparison
- Web-based visualization
- **Potential features to adopt**: Side-by-side system comparison UI

## ALEX4

- Advanced legislative election modeling
- Seat allocation with multiple tiers
- **Potential features to adopt**: Multi-tier electoral systems (e.g., German MMP modeled more precisely)

---

## Features Already in ElectoralSim (no adoption needed)

| Feature | Johnh865 | endolith | ElectionSim | es_sim | ALEX4 | ES |
|---------|----------|----------|-------------|--------|-------|-----|
| Multi-country presets | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Numba JIT acceleration | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Coalition formation | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Government stability | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Opinion dynamics | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Voter psychology | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Batch parameter sweeps | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Streamlit dashboard | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| GPU acceleration | ❌ | ❌ | ❌ | ❌ | ❌ | 🔶 |
| 1M+ voter scale | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Recommended Adoption Priority

1. **[P2]** Gerrymandering analysis from endolith/elsim — aligns with redistricting P5 item
2. **[P2]** Swing state analysis from Johnh865 — useful for election forecasting presentations
3. **[P5]** Multi-tier electoral systems from ALEX4 — directly applicable to German MMP

---

*Last updated: 2026-06-04. To add findings from these projects, clone and explore each repo, then update this file with specific features worth adopting.*
