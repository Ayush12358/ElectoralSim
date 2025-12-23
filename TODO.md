# ElectoralSim - Comprehensive TODO

> **Research Status:** Searches completed with detailed academic references. See `RESEARCH_NOTES.md` for sources.

---

## 🧠 AGENT ARCHITECTURE - VOTER

### Core Voter Attributes
- [ ] **Immutable Demographics** — age, gender, race, citizenship, registration status
- [ ] **Mutable Demographics** — address, marital status, children, employment, education, religion
- [ ] **Socioeconomic Status** — income (percentile), wealth, debt-to-income ratio, financial stress
- [ ] **Social Position** — family structure, social integration score (0-100), loneliness level

### Political Identity
- [ ] **Party Identification (7-point scale)** — Strong D, Weak D, Lean D, Independent, Lean R, Weak R, Strong R
- [ ] **Partisan Affects** — in-group favorability (0-100), out-group favorability (0-100), affective polarization gap
- [ ] **Ideological Identity** — 7-point liberal-conservative, issue-by-issue positions

### Psychological Profile
- [x] Basic ideology dimensions (implemented)
- [ ] **Big Five Personality** (each 0-100):
  - Openness → correlates with progressive views
  - Conscientiousness → correlates with rule-following
  - Extraversion → enables political engagement
  - Agreeableness → correlates with redistribution support
  - Neuroticism → correlates with threat sensitivity, conservatism
- [ ] **Authoritarianism scale** (0-100) — preference for order, hierarchy, tradition
- [ ] **Moral Foundations** (each 0-100):
  - Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, Liberty/Oppression
  - Liberals weight Care/Fairness; conservatives weight all six
- [ ] **Cognitive complexity** — simple (black/white) vs. nuanced thinking

### Knowledge & Information
- [ ] **Political knowledge quiz score** (0-100)
- [ ] **Candidate position accuracy** (0-100) — how well voter knows actual positions
- [ ] **Media diet** — news sources, hours/week, partisan slant
- [ ] **Misinformation susceptibility** (0-100) — conspiracy belief, fact-check receptiveness

---

## 🗳️ VOTING BEHAVIOR MODELS

### Spatial Voting Models
- [x] **Proximity Model** (current) — vote for nearest party in ideological space
- [ ] **Directional Model (Rabinowitz-Macdonald 1989)**:
  - Utility = voter_intensity × candidate_intensity × (same_side ? +1 : -1)
  - Voters prefer candidates on same side of neutral point
  - More extreme candidates preferred if on correct side
  - **Region of Acceptability** — penalty for too-extreme positions
- [ ] **Unified Model** — combine proximity + directional with weights
- [ ] **Discounting Model** — discount extreme promises as unrealistic

### Probabilistic Voting (McFadden)
- [x] Deterministic (argmax) — current
- [ ] **Multinomial Logit (MNL)**:
  - P(vote for j) = exp(V_j) / Σ exp(V_k)
  - V_j = systematic utility for party j
  - **Temperature parameter** — controls randomness (high = more random)
  - **IIA property** — independence of irrelevant alternatives
- [ ] **Mixed Multinomial Logit (MMNL)** — relaxes IIA, allows preference heterogeneity
- [ ] **Nested Logit** — groups similar alternatives

### Valence Voting
- [ ] **Non-policy competence attributes**:
  - Leadership quality (0-100)
  - Character/integrity (0-100)
  - Experience (0-100)
  - Charisma (0-100)
- [ ] Utility = α×(policy proximity) + (1-α)×(valence score)
- [ ] Candidates with high valence can adopt more moderate positions

### Turnout Model (Riker-Ordeshook)
- [ ] **Calculus of Voting: V = pB - C + D**
  - p = probability vote is decisive (very small)
  - B = benefit if preferred candidate wins
  - C = cost of voting (time, effort)
  - D = **civic duty** / expressive benefit (key to explaining turnout)
- [ ] **Alienation** — don't vote if all candidates too far
- [ ] **Indifference** — don't vote if candidates too similar

### Heuristics
- [ ] **Party heuristic** — vote by party label alone
- [ ] **Incumbent heuristic** — default to status quo
- [ ] **Likability heuristic** — personality-based voting
- [ ] **Elite cues** — follow trusted opinion leaders

---

## 🗳️ ELECTORAL SYSTEMS

### Seat Allocation Methods
- [x] **Sainte-Laguë** (implemented) — divisors: 1, 3, 5, 7...
- [x] **D'Hondt** (implemented) — divisors: 1, 2, 3, 4... (favors large parties)
- [ ] **Hare quota** — quota = votes / seats, largest remainder
- [ ] **Droop quota** — quota = floor(votes / (seats + 1)) + 1
- [ ] **Huntington-Hill** — geometric mean divisors (US apportionment)
- [ ] **Modified Sainte-Laguë** — first divisor 1.4 (Swedish method)

### Electoral System Types
- [x] **Party-list PR** (current)
- [ ] **FPTP** — single-member districts, plurality wins
- [ ] **MMP (Mixed-Member Proportional)** — constituency + list seats, compensatory
- [ ] **STV (Single Transferable Vote)**:
  - **Droop quota**: floor(votes / (seats + 1)) + 1
  - Surplus transfer: fractional value = surplus / total_votes
  - **Gregory method** — transfer last parcel at fractional value
  - **Meek method** — keep factors, iterative recalculation
- [ ] **RCV/IRV** — eliminate lowest, transfer votes until majority
- [ ] **Condorcet** — pairwise comparisons, Condorcet winner beats all
- [ ] **Schulze** — strongest path through tournament graph
- [ ] **Borda** — points by rank (n-1, n-2, ..., 0)
- [ ] **Approval** — vote for all acceptable candidates
- [ ] **STAR** — score 0-5, top two runoff by preferences

### Electoral Rules
- [x] National threshold (implemented) — 0%, 5%, 10%
- [ ] **Natural threshold** — 75% / (M + 1) where M = district magnitude
- [ ] **M+1 rule (Cox 1997)** — max viable parties ≈ M + 1
- [ ] **Duverger's Law** — FPTP → 2-party system (mechanical + psychological effects)

---

## 📊 METRICS & INDICES

### Disproportionality
- [x] **Gallagher Index** (implemented):
  - LSq = √(½ Σ(v_i - s_i)²)
- [ ] **Loosemore-Hanby**: D = ½ Σ|v_i - s_i|
- [ ] **Sainte-Laguë Index**: 1/2 Σ(v_i - s_i)² / v_i

### Fragmentation
- [ ] **Effective Number of Parties (Laakso-Taagepera 1979)**:
  - **N = 1 / Σ(p_i)²**
  - p_i = vote/seat share (as proportion, not %)
  - ENEP (by votes), ENPP (by seats)
  - Related to Herfindahl-Hirschman Index: HHI = Σ(p_i)², N = 1/HHI

### Gerrymandering
- [ ] **Efficiency Gap (Stephanopoulos-McGhee 2014)**:
  - Wasted votes = losing votes + (winning votes - 50% - 1)
  - EG = (Party A wasted - Party B wasted) / total votes
  - **>7% suggests illegal gerrymandering**
- [ ] **Polsby-Popper Compactness**: 4π × area / perimeter²
- [ ] **Seats-votes curve** — responsiveness and bias
- [ ] **Partisan bias** — seats deviation at 50% vote share

---

## 🤝 COALITION FORMATION

### Formation Strategies
- [x] **MCW (Minimum Connected Winning)** (implemented) — closest ideologically
- [ ] **MWC (Minimum Winning Coalition)** — smallest majority (Riker 1962)
- [ ] **Laver-Shepsle Portfolio Allocation Model**:
  - Parties prefer specific policy departments
  - Policy = function of who controls which ministry
  - Credible commitments via portfolio assignment
  - Central parties more likely in government
- [ ] **Policy-seeking** — minimize ideological distance
- [ ] **Office-seeking** — maximize cabinet seats/portfolios
- [ ] **Bargaining/War of Attrition** — sequential negotiation with delays
- [ ] **Minority government** — govern without majority (confidence & supply)

### Coalition Dynamics
- [x] Coalition strain — average pairwise distance (implemented)
- [ ] **Portfolio allocation** — weight by importance (PM, Finance, Foreign, etc.)
- [ ] **Coalition agreement** — policy compromise document
- [ ] **Junior partner penalty** — smaller parties lose votes to senior partner

---

## 🌐 OPINION DYNAMICS

### Bounded Confidence (Hegselmann-Krause)
- [ ] **Model parameters**:
  - n = number of agents
  - ε (epsilon) = **confidence bound** — only interact if |opinion_i - opinion_j| < ε
  - Initial distribution (uniform, normal, bimodal)
- [ ] **Dynamics**: x_i(t+1) = average of all x_j where |x_i - x_j| < ε
- [ ] **Outcomes**:
  - Large ε → consensus
  - Small ε → multiple clusters (polarization)
  - **Finite-time convergence** guaranteed
- [ ] **Variations**:
  - Asymmetric ε (different left/right bounds)
  - Heterogeneous ε (open-minded vs. closed-minded agents)
  - Noise/perturbations

### Other Opinion Models
- [ ] **DeGroot** — weighted averaging from network neighbors
- [ ] **Voter Model** — randomly copy neighbor's opinion
- [ ] **Deffuant-Weisbuch** — pairwise bounded confidence

---

## 🗺️ ELECTORAL GEOGRAPHY

### District Structure
- [x] Single national district (current)
- [ ] Multi-district with variable magnitude
- [ ] **MCMC redistricting** — Markov Chain Monte Carlo for fair maps

### Gerrymandering Metrics (see Metrics section)
- [ ] Efficiency gap, compactness scores, partisan bias

---

## 📈 TEMPORAL DYNAMICS

### Campaign Phases
- [ ] Pre-campaign → Announcement → Early → Mid → Late → Final stretch → Election day → Post

### Attention & Volatility
- [ ] Early campaign: high volatility, many undecided
- [ ] Late campaign: stabilization, last-minute deciders
- [ ] Debate bumps, scandal drops, recovery time

---

## ⚔️ EXTERNAL SHOCKS & ADVERSARIAL

### Economic Events
- [ ] GDP growth, unemployment, inflation → incumbent penalty/reward
- [ ] **Retrospective voting** — did economy improve?

### Scandals
- [ ] Break → coverage → support drop → response → narrative → fade

### October Surprises
- [ ] Late-breaking events, scandals, discoveries

### Voter Suppression
- [ ] ID laws, purges, polling place closures, wait times

---

## 🔧 TECHNICAL INFRASTRUCTURE

### Computational
- [ ] Parallelization, GPU, distributed computing
- [ ] 10M+ agents

### Data
- [ ] Real voter file integration
- [ ] Manifesto project party positions
- [ ] Survey data import

### Validation
- [ ] Backtest on historical elections
- [ ] Calibration curves
- [ ] Out-of-sample cross-validation

---

## 📚 RESEARCH NOTES (Failed Searches to Retry)

None in latest batch. Previous failed searches:
- *(None tracked)*

---

## 🏷️ LEGEND

- [x] = Implemented
- [ ] = Not implemented
- **Bold** = High priority / has detailed specification
