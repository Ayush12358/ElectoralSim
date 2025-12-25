# ElectoralSim - Future Roadmap

> All Phase 1-4 features are complete. See [README.md](README.md) for the full feature list.

---

## 🔮 Future Development

### Research Features

- [ ] **P5** Redistricting/Gerrymandering simulation
- [ ] **P5** Campaign finance modeling
- [ ] **P5** Primary election systems
- [ ] **P5** Compulsory voting effects
- [ ] **P5** Electoral college (weighted) systems

### Machine Learning Integration

- [ ] **P5** Train voter behavior models on real survey data
- [ ] **P5** Predict election outcomes from poll data
- [ ] **P5** Synthetic population generation from census data

### Additional Countries

- [ ] **P5** Canada (FPTP + STV Senate)
- [ ] **P5** Israel (Single nationwide PR)
- [ ] **P5** Netherlands (Pure PR, low threshold)
- [ ] **P5** Switzerland (Referendums + PR)
- [ ] **P5** Mexico (Mixed system)

### Advanced Modeling

- [ ] **P5** Multi-level elections (simultaneous national + regional)
- [ ] **P5** Time-series election dynamics
- [ ] **P5** Voter registration and eligibility
- [ ] **P5** Polling place accessibility

### Technical Improvements

- [ ] **P5** Distributed computing support (Dask/Ray)
- [ ] **P5** Real-time visualization dashboard
- [ ] **P5** REST API for web integration
- [ ] **P5** Docker containerization
- [ ] **P5** Jupyter notebook integration

### Data & Validation

- [ ] **P5** Historical election data for all countries
- [ ] **P5** Calibration against real election results
- [ ] **P5** Sensitivity analysis tools
- [ ] **P5** Uncertainty quantification

---

## ✅ Completed Features Summary

### Core (P1) — 17/17 ✅
- ElectionModel, Config, Voter/Party agents
- FPTP, PR (D'Hondt, Sainte-Laguë)
- Gallagher Index, ENP
- Coalition formation (MWC, MCW, strain)
- Numba acceleration

### High Priority (P2) — 31/31 ✅
- Valence model, incumbent status
- Hare/Droop quotas, IRV, STV
- Opinion dynamics (BA, WS, ER networks)
- Government stability simulation
- NOTA, reserved constituencies
- All visualization

### Medium Priority (P3) — 24/24 ✅
- Big Five personality, Moral Foundations
- Misinformation susceptibility, media diet
- Affective polarization
- Alienation/indifference abstention
- Wave elections (national mood)
- Junior partner penalty
- Country presets (Brazil, France, Japan)
- Cox proportional hazards
- Laver-Shepsle portfolio allocation
- 10M+ agent capacity

### Low Priority (P4) — 10/10 ✅
- Adaptive strategy (MVT)
- Event manager (scandals, shocks)
- VSE metric
- Policy vs office tradeoffs
- Duverger's Law simulation
- Australia, South Africa presets
- GPU acceleration (CuPy)
- Interactive Streamlit dashboard

### Nice-to-Have (P5) — 1/1 ✅
- EU Parliament (27 states, 720 MEPs)

---

## 📊 Version History

### v0.1.0 (Current)
- Initial release with all P1-P4 features
- 11 country presets + EU Parliament
- Comprehensive documentation

---

## 📝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute new features.

Priority areas:
1. Additional country presets with real party data
2. Validation against historical elections
3. Performance optimizations
4. Documentation improvements
