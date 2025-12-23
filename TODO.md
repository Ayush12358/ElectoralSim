# ElectoralSim - TODO

> **Research:** 48 web searches + 2 repositories analyzed. Full research log in `/docs/research_notes.md`.

---

## 🧠 VOTER AGENT

### Demographics & Identity
- [ ] **Demographics** — age, gender, race, education, income, religion, location
- [ ] **Party ID (7-point)** — Strong D → Independent → Strong R
- [ ] **Ideology** — 7-point liberal-conservative + issue-by-issue positions
- [ ] **Affective Polarization** — in-group/out-group favorability gap

### Psychology (Pick 1-2 frameworks)
- [ ] **Big Five (OCEAN)** — each 0-100, correlates with political views
- [ ] **Moral Foundations (Haidt)** — Care, Fairness, Loyalty, Authority, Sanctity, Liberty
- [ ] **RWA Scale** — Authoritarianism (α=0.81-0.95)

### Information
- [ ] **Political Knowledge** (0-100)
- [ ] **Misinformation Susceptibility** — belief persistence, illusory truth effect
- [ ] **Media Diet** — sources, partisan slant

---

## 🎭 CANDIDATE/PARTY AGENT

### Attributes
- [ ] **Valence** — charisma, competence, integrity, experience (0-100 each)
- [ ] **Policy Position** — N-dimensional issue space
- [ ] **Party Affiliation** — incumbent/challenger status

### Strategy
- [ ] **Platform Selection** — policy positioning relative to median voter
- [ ] **Valence Investment** — campaign spending builds competence image
- [ ] **Adaptive Behavior** — respond to polls, opponents

---

## 🗳️ VOTING MODELS

### Spatial Voting
- [x] **Proximity Model** (implemented) — vote for nearest in ideological space
- [ ] **Directional Model** (Rabinowitz-Macdonald) — same-side + intensity matters
- [ ] **Unified Model** — α(proximity) + (1-α)(directional)

### Probabilistic
- [x] **Deterministic (argmax)** — current implementation
- [ ] **Multinomial Logit** — P(j) = exp(V_j/τ) / Σexp(V_k/τ), temperature τ
- [ ] **Mixed MNL** — relaxes IIA, heterogeneous preferences

### Turnout
- [ ] **Calculus of Voting** (Riker-Ordeshook): V = pB - C + D
- [ ] **Alienation** — don't vote if all candidates too far
- [ ] **Indifference** — don't vote if candidates too similar

### Strategic Voting
- [ ] Vote for viable non-preferred to prevent worst outcome
- [ ] **Wasted vote fear**, third-party squeeze, spoiler effect

### Heuristics
- [ ] Party label, incumbency, likability, elite cues

---

## 🗳️ ELECTORAL SYSTEMS

### Seat Allocation
- [x] **Sainte-Laguë** — divisors: 1, 3, 5, 7...
- [x] **D'Hondt** — divisors: 1, 2, 3, 4... (favors large parties)
- [ ] **Droop Quota** — floor(votes/(seats+1)) + 1

### System Types
- [x] **Party-list PR** (current)
- [ ] **FPTP** — single-member plurality
- [ ] **MMP** — Germany model (constituency + list)
- [ ] **STV** — preference transfer with Droop quota
- [ ] **IRV/RCV** — eliminate lowest, transfer until majority

### Alternative Methods
- [ ] **Condorcet** — pairwise winner (Schulze for cycles)
- [ ] **Borda** — points by rank
- [ ] **Approval** — vote for all acceptable
- [ ] **STAR** — Score Then Automatic Runoff
- [ ] **Black's** — Condorcet if exists, else Borda
- [ ] **Coombs** — eliminate most last-place (~99% Condorcet efficiency)

### Rules
- [x] **National Threshold** — 0%, 5%, 10%
- [ ] **Natural Threshold** — 75% / (M+1)
- [ ] **Duverger's Law** — FPTP → 2-party system
- [ ] **M+1 Rule** — max viable parties ≈ district magnitude + 1

### Novel Mechanisms
- [ ] **Quadratic Voting** — cost = votes², reveals preference intensity (Weyl)
- [ ] **Liquid Democracy** — transitive delegation, revocable
- [ ] **Cumulative Voting** — multiple votes, plumping strategy, semi-proportional

---

## 📊 METRICS

### Disproportionality
- [x] **Gallagher Index** — √(½ Σ(v_i - s_i)²)
- [ ] **Loosemore-Hanby** — ½ Σ|v_i - s_i|

### Fragmentation
- [ ] **ENP (Laakso-Taagepera)** — N = 1 / Σ(p_i)²

### Gerrymandering
- [ ] **Efficiency Gap** — >7% threshold for illegal gerrymandering
- [ ] **Polsby-Popper Compactness** — 4π × area / perimeter²

### Voting System Quality
- [ ] **VSE** (Jameson Quinn) — 1 - [BR(method) / BR(Random)]
- [ ] **Condorcet Efficiency** — % electing Condorcet winner

---

## 🌐 SOCIAL NETWORKS

### Topologies
- [ ] **Watts-Strogatz** — small-world (rewiring p=0.01-0.1)
- [ ] **Barabási-Albert** — scale-free, preferential attachment, hubs
- [ ] **Stochastic Block Model** — community structure, block matrix P_ij

### Opinion Dynamics
- [ ] **Bounded Confidence (Hegselmann-Krause)** — interact only if |δ| < ε
  - Large ε → consensus; Small ε → polarization
- [ ] **Noisy Voter Model** — copy neighbor + mutation rate ε
- [ ] **Zealots** — fixed-opinion agents, never change mind

### Media & Influence
- [ ] **Mass Media Bias** — probability of adopting media state
- [ ] **Raducha Finding**: Plurality MORE susceptible to propaganda than PR
- [ ] **Information Spread** — SIR model (β=transmission, γ=recovery, R₀=β/γ)

---

## 🤝 COALITION FORMATION

### Strategies
- [x] **MCW** (implemented) — closest ideologically
- [ ] **MWC** — smallest majority (Riker)
- [ ] **Laver-Shepsle** — portfolio allocation determines policy
- [ ] **Policy-seeking** vs **Office-seeking**

### Dynamics
- [x] **Coalition Strain** (implemented) — pairwise distance
- [ ] **Portfolio Allocation** — PM, Finance, Foreign weights
- [ ] **Junior Partner Penalty** — smaller parties lose votes

---

## ⏱️ GOVERNMENT STABILITY

### Collapse Models
- [x] Sigmoid, Linear, Exponential (implemented)
- [ ] **Survival Analysis (Warwick)** — Cox hazard: h(t|X) = h₀(t) × exp(β'X)

### Factors
- [x] Coalition strain, Majority margin (implemented)
- [ ] Economic shocks, Scandals

---

## 📈 EXTERNAL EFFECTS

### Economic Voting
- [ ] **Retrospective** — evaluate incumbent on past performance
- [ ] **Sociotropic** > Pocketbook — national economy matters more
- [ ] **Incumbency Advantage** — name recognition, credit-claiming

### Campaign Effects
- [ ] **Spending** — 94% House winners outspent, diminishing returns
- [ ] **Microtargeting** — 70% more effective on single-attribute (party)
- [ ] **Debate Effects** — minimal persuasion, ~10% decide based on debates
- [ ] **Scandal Penalty** — 6-11% vote share decrease for corruption

### Voter Suppression (US-specific)
- [ ] **Voter ID Laws** — 1.6-2.2pp turnout decline
- [ ] **Polling Closures** — 5.65pp decline from relocation
- [ ] **Wait Times** — 1% future voting decrease per hour

---

## 🇮🇳 INDIA-SPECIFIC

### NOTA
- [ ] Supreme Court mandated (2013)
- [ ] Higher in reserved constituencies: ST (2.18%) > SC (1.1%) > General (0.95%)
- [ ] State-level: fresh elections if NOTA wins (Maharashtra, Haryana, Delhi local)

### Reserved Constituencies
- [ ] Constitutional reservation for SC, ST
- [ ] Rotation policy via delimitation

### EVM & VVPAT
- [ ] Standalone, no network, one-time programmable
- [ ] 5 polling stations/constituency randomly verified
- [ ] 2024: losing candidates can request 5% microcontroller audit

### Ballot Effects
- [ ] **Ordering Bias** — first-listed gets ~1-2% advantage
- [ ] **Donkey Vote** — rank in ballot order (Australia)

---

## 🏛️ THEORETICAL FOUNDATIONS

### Social Choice Theorems
- [ ] **Arrow's Impossibility** — no system satisfies all 5 criteria (≥3 alternatives)
- [ ] **Gibbard-Satterthwaite** — dictatorial OR manipulable
- [ ] **Median Voter Theorem** — median position wins under single-peaked preferences

### Party Dynamics
- [ ] **Downs Convergence** — parties move to center
- [ ] **Critical Elections** — realignments (1896, 1932, 1968)

---

## 🔧 TECHNICAL

### Computational
- [ ] Parallelization, GPU support
- [ ] 10M+ agent capacity

### Data Integration
- [ ] Real voter files
- [ ] Manifesto project positions
- [ ] Survey data import

### Validation
- [ ] **Hindcast** — backtest on 2020, 2016, 2012
- [ ] **Calibration Curves** — predicted vs actual
- [ ] **Out-of-Sample CV**

---

## 🏷️ LEGEND

- [x] = Implemented
- [ ] = Not implemented
