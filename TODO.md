# ElectoralSim - TODO

> Priority: **P1** = Critical | **P2** = High | **P3** = Medium | **P4** = Low | **P5** = Nice-to-have

---

## 🧠 VOTER AGENT

### Core Attributes
- [x] **P1** Demographics — age, gender, education, income, religion, location ✓
- [x] **P1** Party ID (7-point) — Strong D → Independent → Strong R ✓
- [x] **P1** Ideology — multi-dimensional issue positions ✓
- [ ] **P3** Affective Polarization — in-group/out-group favorability gap

### Psychology (Choose ONE)
- [ ] **P2** Big Five (OCEAN) — correlates with political views
- [ ] **P3** Moral Foundations (Haidt) — Care, Fairness, Loyalty, Authority, Sanctity

### Information
- [ ] **P2** Political Knowledge (0-100)
- [ ] **P3** Misinformation Susceptibility
- [ ] **P3** Media Diet — sources, partisan slant

---

## 🎭 CANDIDATE/PARTY AGENT

- [x] **P1** Policy Position — N-dimensional issue space ✓
- [x] **P2** Valence — charisma, competence, integrity (0-100) ✓
- [ ] **P2** Incumbent Status
- [ ] **P4** Adaptive Strategy — respond to polls

---

## 🗳️ VOTING MODELS

### Core
- [x] **P1** Proximity Model ✓
- [x] **P1** Multinomial Logit — P(j) = exp(V_j/τ) / Σexp(V_k/τ) ✓

### Turnout
- [x] **P2** Calculus of Voting: R = pB - C + D ✓ (basic turnout_prob)
- [ ] **P3** Alienation/Indifference abstention

### Strategic
- [ ] **P3** Tactical voting, wasted vote fear

---

## 🗳️ ELECTORAL SYSTEMS

### Seat Allocation
- [x] **P1** Sainte-Laguë ✓
- [x] **P1** D'Hondt ✓
- [x] **P3** Droop Quota ✓
- [x] **P3** Hare Quota ✓

### System Types
- [x] **P1** Party-list PR ✓
- [x] **P1** FPTP ✓
- [x] **P2** MMP — Germany model ✓ (via preset)
- [x] **P2** STV — Ireland, Australia ✓
- [x] **P2** IRV/RCV — growing adoption ✓

### Other Methods
- [ ] **P3** Condorcet/Schulze
- [ ] **P3** Approval Voting
- [ ] **P4** STAR Voting

### Rules
- [x] **P1** National Threshold ✓
- [ ] **P4** Duverger's Law simulation

---

## 📊 METRICS

- [x] **P1** Gallagher Index ✓
- [x] **P1** ENP (Laakso-Taagepera) ✓
- [x] **P3** Efficiency Gap ✓
- [ ] **P4** VSE — voting system efficiency

---

## 🌐 SOCIAL NETWORKS

### Topologies
- [x] **P2** Barabási-Albert — scale-free, realistic ✓
- [ ] **P3** Watts-Strogatz — small-world

### Opinion Dynamics
- [x] **P2** Noisy Voter Model — copy neighbor + mutation ✓
- [x] **P2** Zealots — fixed-opinion agents ✓

### Media
- [ ] **P3** Mass Media Bias
- [ ] **P3** Plurality vs PR susceptibility (Raducha)

---

## 🤝 COALITION FORMATION

- [x] **P1** MCW ✓ — minimum connected winning
- [ ] **P2** MWC — minimum winning coalition
- [ ] **P3** Laver-Shepsle portfolio allocation
- [ ] **P4** Policy vs Office-seeking tradeoffs

### Dynamics
- [x] **P1** Coalition Strain ✓
- [ ] **P3** Junior Partner Penalty

---

## ⏱️ GOVERNMENT STABILITY

- [x] **P1** Collapse Models ✓ (Sigmoid, Linear, Exponential)
- [ ] **P3** Survival Analysis — Cox hazard
- [ ] **P4** Economic shocks, Scandals

---

## 📈 EXTERNAL EFFECTS

### Economic Voting
- [ ] **P2** Retrospective voting
- [ ] **P3** Sociotropic vs Pocketbook
- [ ] **P3** Incumbency Advantage

### Campaign
- [ ] **P4** Spending Effects
- [ ] **P4** Microtargeting
- [ ] **P4** Scandal Penalty

---

## 🇮🇳 INDIA-SPECIFIC

### Core (Implemented)
- [x] **P1** Full Lok Sabha simulation ✓ — 543 constituencies, 30 states
- [x] **P1** State-wise party weights ✓ — Regional party strongholds
- [x] **P1** NDA/INDIA alliance tracking ✓

### NOTA
- [ ] **P2** NOTA vote option
- [ ] **P3** NOTA impact on close races

### Reserved Constituencies
- [ ] **P2** SC, ST reservation modeling
- [ ] **P3** Delimitation effects

### Electoral Features
- [ ] **P2** Phase-wise election simulation (7 phases)
- [ ] **P2** Anti-incumbency factor
- [ ] **P3** Wave elections (national mood)
- [ ] **P3** Alliance seat-sharing agreements
- [ ] **P3** Historical validation (2014, 2019, 2024)
- [ ] **P4** Opinion poll simulation
- [ ] **P4** Exit poll modeling
- [ ] **P4** EVM simulation
- [ ] **P5** VVPAT audit modeling

### Ballot Effects
- [ ] **P4** Ordering Bias (~1-2%)

---

## 🌍 COUNTRY SIMULATIONS

### Implemented
- [x] **P1** India ✓ — 543 constituencies, 17 parties
- [x] **P2** USA preset ✓
- [x] **P2** UK preset ✓
- [x] **P2** Germany preset ✓

### Planned
- [ ] **P3** Brazil — Largest PR system, 513 deputies
- [ ] **P3** France — Two-round system
- [ ] **P3** Japan — Mixed-member parallel
- [ ] **P4** Australia — STV for Senate, IRV for House
- [ ] **P4** South Africa — Pure PR
- [ ] **P5** EU Parliament — Multi-country simulation

---

## 🏛️ THEORY (Reference Only)

- Arrow's Impossibility, Median Voter Theorem, Downs Convergence

---

## � VISUALIZATION

- [ ] **P2** Seat distribution bar chart
- [ ] **P2** Vote share pie chart
- [ ] **P3** India constituency map (choropleth)
- [ ] **P3** Opinion dynamics animation
- [ ] **P3** Swing analysis dashboard
- [ ] **P4** Interactive election explorer (Streamlit/Dash)

---

## �🔧 TECHNICAL

### Performance (Implemented)
- [x] **P1** Numba JIT acceleration ✓ — 89x speedup
- [x] **P2** Batch elections ✓ — 30 elections/sec
- [x] **P2** Data caching ✓ — 26% improvement

### Remaining
- [ ] **P3** 10M+ agent capacity
- [ ] **P3** Real constituency data integration
- [ ] **P3** Historical election data loading
- [ ] **P4** GPU support (CuPy)

---

## 📋 PRIORITY SUMMARY

| Priority | Count | Done | Remaining |
|----------|-------|------|-----------|
| **P1** | 16 | 16 ✅ | 0 |
| **P2** | 20 | 14 | 6 |
| **P3** | 25 | 3 | 22 |
| **P4** | 15 | 0 | 15 |
| **P5** | 3 | 0 | 3 |

### Implementation Progress
- **Phase 1 (P1)**: ✅ COMPLETE — Core model, India election, Numba acceleration
- **Phase 2 (P2)**: 🔄 IN PROGRESS — Opinion dynamics, IRV/STV done; NOTA, visualization remaining
- **Phase 3 (P3)**: Country simulations, wave elections, real data
- **Phase 4 (P4+)**: Campaign effects, interactive dashboards

