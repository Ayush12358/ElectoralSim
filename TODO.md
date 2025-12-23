# ElectoralSim - TODO

> Focused roadmap with high-impact features only. Research notes archived separately.

---

## 🧠 VOTER AGENT

### Core Attributes
- [ ] **Demographics** — age, gender, education, income, religion, location
- [ ] **Party ID (7-point)** — Strong D → Independent → Strong R
- [ ] **Ideology** — multi-dimensional issue positions
- [ ] **Affective Polarization** — in-group/out-group favorability gap

### Psychology (Choose ONE)
- [ ] **Big Five (OCEAN)** — Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- [ ] **Moral Foundations (Haidt)** — Care, Fairness, Loyalty, Authority, Sanctity, Liberty

### Information
- [ ] **Political Knowledge** (0-100)
- [ ] **Misinformation Susceptibility** — belief persistence, illusory truth
- [ ] **Media Diet** — sources, partisan slant

---

## 🎭 CANDIDATE/PARTY AGENT

- [ ] **Valence** — charisma, competence, integrity (0-100)
- [ ] **Policy Position** — N-dimensional issue space
- [ ] **Incumbent Status** — affects credibility, resources
- [ ] **Adaptive Strategy** — respond to polls, opponents

---

## 🗳️ VOTING MODELS

### Core (Implement These)
- [x] **Proximity Model** ✓ — vote for nearest in ideological space
- [ ] **Multinomial Logit** — P(j) = exp(V_j/τ) / Σexp(V_k/τ)
  - Temperature τ controls randomness

### Turnout
- [ ] **Calculus of Voting**: R = pB - C + D
  - p = pivotal probability, B = benefit, C = cost, D = duty
- [ ] **Alienation** — abstain if all candidates too far
- [ ] **Indifference** — abstain if candidates too similar

### Strategic
- [ ] Tactical voting to prevent worst outcome
- [ ] Wasted vote fear, spoiler effect

---

## 🗳️ ELECTORAL SYSTEMS

### Seat Allocation
- [x] **Sainte-Laguë** ✓
- [x] **D'Hondt** ✓
- [ ] **Droop Quota** — floor(votes/(seats+1)) + 1

### System Types
- [x] **Party-list PR** ✓
- [ ] **FPTP** — single-member plurality
- [ ] **MMP** — Germany model (constituency + list)
- [ ] **STV** — preference transfer
- [ ] **IRV/RCV** — eliminate lowest until majority

### Other Methods
- [ ] **Condorcet/Schulze** — pairwise winner
- [ ] **Approval Voting** — vote for all acceptable
- [ ] **STAR Voting** — Score Then Automatic Runoff

### Rules
- [x] **National Threshold** ✓ — 0%, 5%, 10%
- [ ] **Duverger's Law** — FPTP → 2-party system

---

## 📊 METRICS

- [x] **Gallagher Index** ✓ — disproportionality
- [ ] **ENP (Laakso-Taagepera)** — N = 1 / Σ(p_i)²
- [ ] **Efficiency Gap** — gerrymandering detection (>7% threshold)
- [ ] **VSE** — voting system efficiency (Jameson Quinn)

---

## 🌐 SOCIAL NETWORKS

### Topologies (Choose 1-2)
- [ ] **Barabási-Albert** — scale-free, hubs, realistic
- [ ] **Watts-Strogatz** — small-world (rewiring p=0.01-0.1)

### Opinion Dynamics
- [ ] **Noisy Voter Model** — copy neighbor + mutation rate ε
- [ ] **Zealots** — fixed-opinion agents that never change

### Media
- [ ] **Mass Media Bias** — probability of adopting media state
- [ ] **Key Finding**: Plurality MORE susceptible to propaganda than PR (Raducha 2023)

---

## 🤝 COALITION FORMATION

- [x] **MCW** ✓ — minimum connected winning
- [ ] **MWC** — minimum winning coalition (Riker)
- [ ] **Laver-Shepsle** — portfolio allocation
- [ ] **Policy vs Office-seeking** tradeoffs

### Dynamics
- [x] **Coalition Strain** ✓
- [ ] **Junior Partner Penalty**

---

## ⏱️ GOVERNMENT STABILITY

- [x] Sigmoid, Linear, Exponential collapse ✓
- [ ] **Survival Analysis** — Cox hazard model
- [ ] Economic shocks, Scandals as covariates

---

## 📈 EXTERNAL EFFECTS

### Economic Voting
- [ ] **Retrospective** — evaluate incumbent on past
- [ ] **Sociotropic** — national economy > personal
- [ ] **Incumbency Advantage**

### Campaign
- [ ] **Spending Effects** — 94% House winners outspent
- [ ] **Microtargeting** — 70% more effective single-attribute
- [ ] **Scandal Penalty** — 6-11% vote decrease

---

## 🇮🇳 INDIA-SPECIFIC

### NOTA
- [ ] Higher in reserved: ST (2.18%) > SC (1.1%) > General (0.95%)
- [ ] State-level fresh elections (Maharashtra, Haryana, Delhi local)

### Reserved Constituencies
- [ ] SC, ST reservations
- [ ] Delimitation-based rotation

### EVM & VVPAT
- [ ] Standalone, no network, one-time programmable
- [ ] 5 polling stations/constituency verified
- [ ] 5% microcontroller audit on request (2024)

### Ballot Effects
- [ ] **Ordering Bias** — first-listed gets ~1-2% advantage

---

## 🏛️ THEORY (Reference Only)

- **Arrow's Impossibility** — no perfect ranked system (≥3 options)
- **Median Voter Theorem** — median position wins (single-peaked)
- **Downs Convergence** — parties move to center

---

## 🔧 TECHNICAL

- [ ] Parallelization, GPU support
- [ ] 10M+ agent capacity
- [ ] Real voter/manifesto data integration
- [ ] **Validation** — hindcast on 2016, 2020

---

## 🏷️ LEGEND

- [x] = Implemented
- [ ] = To implement
- ✓ = Already done
