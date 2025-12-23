# ElectoralSim - TODO

> Priority: **P1** = Critical | **P2** = High | **P3** = Medium | **P4** = Low | **P5** = Nice-to-have

---

## 🧠 VOTER AGENT

### Core Attributes
- [ ] **P1** Demographics — age, gender, education, income, religion, location
- [ ] **P1** Party ID (7-point) — Strong D → Independent → Strong R
- [ ] **P1** Ideology — multi-dimensional issue positions
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

- [ ] **P1** Policy Position — N-dimensional issue space
- [ ] **P2** Valence — charisma, competence, integrity (0-100)
- [ ] **P2** Incumbent Status
- [ ] **P4** Adaptive Strategy — respond to polls

---

## 🗳️ VOTING MODELS

### Core
- [x] **P1** Proximity Model ✓
- [ ] **P1** Multinomial Logit — P(j) = exp(V_j/τ) / Σexp(V_k/τ)

### Turnout
- [ ] **P2** Calculus of Voting: R = pB - C + D
- [ ] **P3** Alienation/Indifference abstention

### Strategic
- [ ] **P3** Tactical voting, wasted vote fear

---

## 🗳️ ELECTORAL SYSTEMS

### Seat Allocation
- [x] **P1** Sainte-Laguë ✓
- [x] **P1** D'Hondt ✓
- [ ] **P3** Droop Quota

### System Types
- [x] **P1** Party-list PR ✓
- [ ] **P1** FPTP — most common worldwide
- [ ] **P2** MMP — Germany model
- [ ] **P2** STV — Ireland, Australia
- [ ] **P2** IRV/RCV — growing adoption

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
- [ ] **P1** ENP (Laakso-Taagepera) — party fragmentation
- [ ] **P3** Efficiency Gap — gerrymandering
- [ ] **P4** VSE — voting system efficiency

---

## 🌐 SOCIAL NETWORKS

### Topologies
- [ ] **P2** Barabási-Albert — scale-free, realistic
- [ ] **P3** Watts-Strogatz — small-world

### Opinion Dynamics
- [ ] **P2** Noisy Voter Model — copy neighbor + mutation
- [ ] **P2** Zealots — fixed-opinion agents

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

### NOTA
- [ ] **P2** NOTA implementation
- [ ] **P3** Reserved constituency differential

### Reserved Constituencies
- [ ] **P2** SC, ST reservations

### EVM & VVPAT
- [ ] **P4** EVM simulation
- [ ] **P5** VVPAT audit modeling

### Ballot Effects
- [ ] **P4** Ordering Bias (~1-2%)

---

## 🏛️ THEORY (Reference Only)

- Arrow's Impossibility, Median Voter Theorem, Downs Convergence

---

## 🔧 TECHNICAL

- [ ] **P2** Parallelization, GPU support
- [ ] **P3** 10M+ agent capacity
- [ ] **P3** Real data integration
- [ ] **P2** Validation — hindcast 2016, 2020

---

## 📋 PRIORITY SUMMARY

| Priority | Count | Description |
|----------|-------|-------------|
| **P1** | 12 | Must-have for MVP |
| **P2** | 15 | Core functionality |
| **P3** | 18 | Important extensions |
| **P4** | 10 | Nice additions |
| **P5** | 1 | Future scope |

### Recommended Implementation Order
1. **Phase 1 (P1)**: Demographics, Party ID, Ideology, MNL, FPTP, ENP
2. **Phase 2 (P2)**: Valence, Turnout, Networks, Coalition dynamics, Validation
3. **Phase 3 (P3)**: Opinion dynamics, Media, Economic voting, India features
4. **Phase 4 (P4+)**: Campaign effects, Advanced metrics, EVM simulation
