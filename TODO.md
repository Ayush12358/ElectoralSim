# ElectoralSim - TODO

> Priority: **P1** = Critical | **P2** = High | **P3** = Medium | **P4** = Low | **P5** = Nice-to-have

---

## 🧠 VOTER AGENT

### Core Attributes
- [x] **P1** Demographics — age, gender, education, income, religion, location ✓
- [x] **P1** Party ID (7-point) — Strong D → Independent → Strong R ✓
- [x] **P1** Ideology — multi-dimensional issue positions ✓
- [x] **P3** Affective Polarization ✓ — affective_polarization column (0-1)

### Psychology
- [x] **P3** Big Five (OCEAN) ✓ — openness, conscientiousness, extraversion, agreeableness, neuroticism columns
- [x] **P3** Moral Foundations (Haidt) ✓ — mf_care, mf_fairness, mf_loyalty, mf_authority, mf_sanctity columns

### Information
- [x] **P2** Political Knowledge (0-100) ✓
- [x] **P3** Misinformation Susceptibility ✓ — misinfo_susceptibility column (0-1)
- [x] **P3** Media Diet ✓ — media_source_id/media_bias columns + vectorized opinion dynamics

---

## 🎭 CANDIDATE/PARTY AGENT

- [x] **P1** Policy Position — N-dimensional issue space ✓
- [x] **P2** Valence — charisma, competence, integrity (0-100) ✓
- [x] **P2** Incumbent Status ✓ — with anti-incumbency modifier
- [x] **P4** Adaptive Strategy ✓ — Median Voter Theorem implementation (party_strategy.py)

---

## 🗳️ VOTING MODELS

### Core
- [x] **P1** Proximity Model ✓
- [x] **P1** Multinomial Logit — P(j) = exp(V_j/τ) / Σexp(V_k/τ) ✓

### Turnout
- [x] **P2** Calculus of Voting: R = pB - C + D ✓ (basic turnout_prob)
- [x] **P3** Alienation/Indifference abstention ✓ — alienation_threshold, indifference_threshold params

### Strategic
- [x] **P2** Strategic Voting Model ✓ — StrategicVotingModel class
- [x] **P3** Tactical voting, wasted vote fear (advanced) ✓ — WastedVoteModel class

---

## 🗳️ ELECTORAL SYSTEMS

### Seat Allocation
- [x] **P1** Sainte-Laguë ✓
- [x] **P1** D'Hondt ✓
- [x] **P2** Droop Quota ✓
- [x] **P2** Hare Quota ✓

### System Types
- [x] **P1** Party-list PR ✓
- [x] **P1** FPTP ✓
- [x] **P2** MMP — Germany model ✓ (via preset)
- [x] **P2** STV — Ireland, Australia ✓
- [x] **P2** IRV/RCV — growing adoption ✓

### Other Methods
- [x] **P3** Condorcet Winner ✓
- [x] **P3** Approval Voting ✓

### Rules
- [x] **P1** National Threshold ✓
- [ ] **P4** Duverger's Law simulation

---

## 📊 METRICS

- [x] **P1** Gallagher Index ✓
- [x] **P1** ENP (Laakso-Taagepera) ✓
- [x] **P2** Efficiency Gap ✓
- [x] **P2** Loosemore-Hanby Index ✓
- [x] **P2** Herfindahl-Hirschman Index ✓
- [x] **P4** VSE ✓ — voting system efficiency (vse.py)

---

## 🌐 SOCIAL NETWORKS

### Topologies
- [x] **P2** Barabási-Albert — scale-free, realistic ✓
- [x] **P2** Watts-Strogatz — small-world ✓
- [x] **P2** Erdős-Rényi — random graph ✓

### Opinion Dynamics
- [x] **P2** Noisy Voter Model — copy neighbor + mutation ✓
- [x] **P2** Zealots — fixed-opinion agents ✓
- [x] **P2** Bounded Confidence Model ✓

### Media
- [x] **P3** Mass Media Bias ✓ — media_bias, media_strength params in OpinionDynamics.step()
- [x] **P3** Plurality vs PR susceptibility (Raducha) ✓ — system parameter in OpinionDynamics.step()

---

## 🤝 COALITION FORMATION

- [x] **P1** MCW ✓ — minimum connected winning
- [x] **P1** MWC ✓ — minimum winning coalition
- [x] **P3** Laver-Shepsle portfolio allocation ✓ — allocate_portfolios_laver_shepsle()
- [ ] **P4** Policy vs Office-seeking tradeoffs

### Dynamics
- [x] **P1** Coalition Strain ✓
- [x] **P3** Junior Partner Penalty ✓ — junior_partner_penalty function

---

## ⏱️ GOVERNMENT STABILITY

- [x] **P1** Collapse Models ✓ (Sigmoid, Linear, Exponential)
- [x] **P2** Government Simulator ✓ — Monte Carlo survival
- [x] **P3** Survival Analysis — Cox hazard ✓ — cox_proportional_hazard() function
- [x] **P4** Economic shocks, Scandals ✓ — EventManager module (event_manager.py)

---

## 📈 EXTERNAL EFFECTS

### Economic Voting
- [x] **P2** Retrospective voting ✓ — RetrospectiveModel + economic_growth param
- [x] **P3** Sociotropic vs Pocketbook ✓ — SociotropicPocketbookModel + economic_perception column
- [x] **P2** Anti-incumbency ✓ — anti_incumbency parameter

### Campaign
- [x] **P4** Scandal Penalty ✓ — via EventManager


---

## 🇮🇳 INDIA-SPECIFIC

### Core
- [x] **P1** Full Lok Sabha simulation ✓ — 543 constituencies, 30 states
- [x] **P1** State-wise party weights ✓ — Regional party strongholds
- [x] **P1** NDA/INDIA alliance tracking ✓

### NOTA
- [x] **P2** NOTA vote option ✓ — include_nota parameter
- [x] **P3** NOTA impact on close races ✓ — nota_contested_seats, nota_contested_list fields

### Reserved Constituencies
- [x] **P2** SC, ST reservation modeling ✓ — constituency_constraints parameter

### Electoral Features
- [x] **P2** Phase-wise election configuration ✓ (7 phases defined)
- [x] **P2** Anti-incumbency factor ✓
- [x] **P3** Wave elections (national mood) ✓ — national_mood parameter

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
- [x] **P5** EU Parliament ✓ — 27 member states, 720 MEPs, 8 political groups

---

## 📊 VISUALIZATION

- [x] **P2** Seat distribution bar chart ✓ — plot_seat_distribution()
- [x] **P2** Vote share pie chart ✓ — plot_vote_shares()
- [x] **P2** Seats vs Votes comparison ✓ — plot_seats_vs_votes()
- [x] **P2** Election summary panel ✓ — plot_election_summary()
- [ ] **P3** India constituency map (choropleth)
- [ ] **P3** Opinion dynamics animation
- [ ] **P3** Swing analysis dashboard
- [ ] **P4** Interactive election explorer (Streamlit/Dash)

---

## 🔧 TECHNICAL

### Performance
- [x] **P1** Numba JIT acceleration ✓ — 89x speedup
- [x] **P2** Batch elections ✓ — 30 elections/sec
- [x] **P2** Data caching ✓ — 26% improvement
- [x] **P2** Repository restructuring ✓ — Modular package layout

### Remaining
- [ ] **P3** 10M+ agent capacity
- [ ] **P3** Real constituency data integration
- [ ] **P3** Historical election data loading
- [ ] **P4** GPU support (CuPy)

---

## 📋 PRIORITY SUMMARY

| Priority | Total | Done | Remaining |
|----------|-------|------|-----------|
| **P1** | 17 | 17 ✅ | 0 |
| **P2** | 31 | 31 ✅ | 0 |
| **P3** | 18 | 17 | 1 |
| **P4** | 6 | 3 | 3 |
| **P5** | 1 | 1 ✅ | 0 |

### Implementation Progress
- **Phase 1 (P1)**: ✅ COMPLETE — Core model, India election, Coalition, Numba
- **Phase 2 (P2)**: ✅ COMPLETE — Opinion dynamics, all voting systems, NOTA, visualization
- **Phase 3 (P3)**: 🔄 94% — 17/18 done, 1 remaining (Maps)
- **Phase 4 (P4)**: 🔄 50% — 3/6 done
```
