# ElectoralSim - Future Roadmap

> All Phase 1-4 features are complete. See [README.md](README.md) for the full feature list.

---

## Future Development

### High Priority (P1) — Upcoming

- [ ] **P1** Test CuPy GPU implementations
- [x] **P1** Implement a batch runner suite for running several simulations with varying parameters
- [ ] **P1** Look into Adway Mitra's paper (Electoral Systems and Representation in India)
- [ ] **P1** Add citations for papers that have the concepts
- [x] **P1** Update man pages and help for CLI
- [x] **P1** Update documentation (API reference and guides)
- [ ] **P1** Test the API on a separate machine
- [ ] **P1** Check and add features from other electoral sims:
    - [ ] Johnh865/election_sim
    - [ ] endolith/elsim
    - [ ] ElectionSim on arxiv
    - [ ] es_simulations
- [x] **P1** Migrate Licence from MIT to Apache 2.0
- [ ] **P1** Upgrade to Mesa v3.4.0 and make changes accordingly. Analyse the new version and suggest and implement changes.

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

## Completed Features Summary

### Core (P1) — 17/17 [DONE]
- ElectionModel, Config, Voter/Party agents
- FPTP, PR (D'Hondt, Sainte-Laguë)
- Gallagher Index, ENP
- Coalition formation (MWC, MCW, strain)
- Numba acceleration

### High Priority (P2) — 31/31 [DONE]
- Valence model, incumbent status
- Hare/Droop quotas, IRV, STV
- Opinion dynamics (BA, WS, ER networks)
- Government stability simulation
- NOTA, reserved constituencies
- All visualization

### Medium Priority (P3) — 24/24 [DONE]
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

### Low Priority (P4) — 10/10 [DONE]
- Adaptive strategy (MVT)
- Event manager (scandals, shocks)
- VSE metric
- Policy vs office tradeoffs
- Duverger's Law simulation
- Australia, South Africa presets
- GPU acceleration (CuPy)
- Interactive Streamlit dashboard

### Nice-to-Have (P5) — 1/1 [DONE]
- EU Parliament (27 states, 720 MEPs)

---

## Version History

## Version History

### v0.0.2 (Current)
- Migrated from `mesa-frames` to `Mesa 3.0+` + `Polars`
- Comprehensive test suite (225 tests, ~70% coverage)
- Fixed Mesa 3.0 API compatibility
- Improved RNG consistency and performance

### v0.0.1
- Initial release with all P1-P4 features
- 11 country presets + EU Parliament
- Comprehensive documentation

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute new features.

Priority areas:
1. Additional country presets with real party data
2. Validation against historical elections
3. Performance optimizations
4. Documentation improvements
