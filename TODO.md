# ElectoralSim - Comprehensive TODO

> **Research Status:** 48 exhaustive web searches + analysis of 2 reference repositories (pcbouman-eur/es_simulations, endolith/elsim). Includes formulas, parameters, and academic references.

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

#### Big Five Personality (OCEAN) — each 0-100
- [ ] **Openness** → correlates with liberal/progressive views, curiosity, creativity
- [ ] **Conscientiousness** → correlates with conservative views, order, rule-following
- [ ] **Extraversion** → enables political engagement, may lean conservative
- [ ] **Agreeableness** → correlates with social safety net support, Labour voting (UK)
- [ ] **Neuroticism** → correlates with threat sensitivity, anxiety about economic future

#### Moral Foundations Theory (Haidt-Graham) — each 0-100
- [ ] **Care/Harm** — sensitivity to suffering, compassion
- [ ] **Fairness/Cheating** — justice, reciprocal altruism (liberals = equality, conservatives = proportionality)
- [ ] **Loyalty/Betrayal** — group cohesion, patriotism, in-group preference
- [ ] **Authority/Subversion** — respect for tradition, hierarchy, leadership
- [ ] **Sanctity/Degradation** — disgust, purity, contamination avoidance
- [ ] **Liberty/Oppression** — resistance to domination, autonomy
- **Pattern:** Liberals weight Care/Fairness heavily; conservatives weight all six

#### Right-Wing Authoritarianism (Altemeyer RWA Scale)
- [ ] **Authoritarian Submission** — deference to legitimate authority
- [ ] **Authoritarian Aggression** — aggression toward perceived out-groups
- [ ] **Conventionalism** — adherence to traditional social norms
- [ ] **Measurement:** 22-30 item Likert scale (1-9), α = 0.81-0.95

### Knowledge & Information
- [ ] **Political knowledge quiz score** (0-100)
- [ ] **Candidate position accuracy** (0-100) — how well voter knows actual positions
- [ ] **Media diet** — news sources, hours/week, partisan slant
- [ ] **Misinformation susceptibility** (0-100):
  - **Belief persistence** — misinformation shapes attitudes even after correction
  - **Belief echoes** — residual attitudinal effects persist
  - **Backfire effect** (Nyhan-Reifler) — corrections may strengthen false belief (worldview/familiarity types)
  - **Illusory truth** — repeated exposure increases perceived accuracy

---

## 🗳️ VOTING BEHAVIOR MODELS

### Spatial Voting Models

#### Proximity Model (current implementation)
- [x] Vote for nearest party in ideological space
- Uses Minkowski distance with configurable p parameter

#### Directional Model (Rabinowitz-Macdonald 1989)
- [ ] **Utility = voter_intensity × candidate_intensity × direction_sign**
  - direction_sign = +1 if same side of neutral point, -1 otherwise
- [ ] Voters prefer candidates on same side of issue
- [ ] More extreme candidates preferred if on correct side
- [ ] **Region of Acceptability** — penalty for too-extreme positions

#### Unified Model
- [ ] Combine proximity + directional with weights: U = α×(proximity) + (1-α)×(directional)

### Probabilistic Voting (McFadden)

#### Multinomial Logit (MNL)
- [x] Deterministic (argmax) — current implementation
- [ ] **P(vote for j) = exp(V_j / τ) / Σ exp(V_k / τ)**
  - V_j = systematic utility for party j
  - **τ = temperature parameter** — controls randomness (low = deterministic, high = random)
- [ ] **IIA property** — Independence of Irrelevant Alternatives (ratio of probabilities unchanged by adding alternative)

#### Advanced Logit Models
- [ ] **Mixed Multinomial Logit (MMNL)** — relaxes IIA, allows heterogeneous preferences
- [ ] **Nested Logit** — groups similar alternatives in "nests"

### Valence Voting
- [ ] **Non-policy competence attributes** (each 0-100):
  - Leadership quality, charisma
  - Character/integrity, honesty
  - Experience, legislative skill
  - Credibility (delivering on promises)
- [ ] **Combined utility:** U = α×(policy proximity) + (1-α)×(valence score)
- [ ] High-valence candidates can adopt more moderate positions

### Turnout Model (Riker-Ordeshook 1968)
- [ ] **Calculus of Voting: V = pB - C + D**
  - **p** = probability vote is decisive (very small, ~1/N)
  - **B** = benefit if preferred candidate wins (differential)
  - **C** = cost of voting (time, effort, information)
  - **D** = **civic duty / expressive benefit** (key to explaining turnout paradox)
- [ ] **Alienation** — don't vote if all candidates too far from ideal point
- [ ] **Indifference** — don't vote if candidates too similar

### Strategic Voting (Tactical Voting)
- [ ] Voting for non-preferred viable candidate to prevent worst outcome
- [ ] Driven by fear of **wasted vote** (votes for losing candidates)
- [ ] **Third-party squeeze** — minor parties suppressed in FPTP
- [ ] **Spoiler effect** — third party splits vote with ideologically similar major party

### Voter Models *(from elsim)*
- [ ] **Impartial Culture (IC)**:
  - Each voter ranking is **equally likely** (random permutation)
  - With n candidates, each of n! orderings has probability 1/n!
  - **Unrealistic but mathematically tractable** — worst-case analysis
  - Variants: Impartial Anonymous Culture (IAC), IANC
- [ ] **Random Utilities** — each voter-candidate utility drawn from distribution
- [ ] **Normal Electorate (Spatial)** — voters/candidates in N-dimensional Gaussian space
  - Distance → utility (normed_dist_utilities)

### Yee Diagrams *(Ka-Ping Yee)*
- [ ] **2D visualization of single-winner methods**:
  - Candidates as fixed points in 2D issue space
  - Voters distributed (usually Gaussian) around each grid point
  - Color each point by winner under given voting method
- [ ] **Reveals**:
  - IRV/Plurality bias toward extremes
  - Approval bias toward center
  - **Non-monotonicity** — shifting opinion TOWARD candidate can cause them to LOSE
- [ ] Implementations: voteline (1D), IEVS, Brian Olson Elections On The Plane

### Ballot Strategies *(from elsim)*
- [ ] **Honest Rankings** — rank by true utility
- [ ] **Honest Normed Scores** — score proportional to utility
- [ ] **Approval Optimal** — approve all candidates above mean utility
- [ ] **Vote for K** — approve top K candidates

### Heuristics
- [ ] **Party heuristic** — vote by party label alone
- [ ] **Incumbent heuristic** — default to status quo
- [ ] **Likability heuristic** — personality-based voting
- [ ] **Elite cues** — follow trusted opinion leaders
- [ ] **Appearance heuristic** — attractiveness bias

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

#### Proportional Representation
- [x] **Party-list PR** (current)
- [ ] **MMP (Mixed-Member Proportional)** — Germany model:
  - **Erststimme** (first vote) — constituency direct candidate (FPTP)
  - **Zweitstimme** (second vote) — party list (determines overall proportionality)
  - **Überhangmandate** — overhang seats when constituency > proportional entitlement
  - **Ausgleichsmandate** — leveling/compensatory seats to restore proportionality
  - 2023 Reform: fixed 630 seats, abolishes overhang/leveling
- [ ] **STV (Single Transferable Vote)**:
  - **Droop quota**: floor(votes/(seats+1)) + 1
  - Surplus transfer: fractional value = surplus / total_votes
  - **Gregory method** — transfer last parcel at fractional value
  - **Meek method** — keep factors, iterative recalculation
  - Elimination of lowest, votes transfer to next preference

#### Majoritarian/Plurality
- [ ] **FPTP** — single-member districts, plurality wins
- [ ] **Two-round runoff** — if no majority, top two compete in second round
- [ ] **RCV/IRV** — eliminate lowest, transfer votes until majority

#### Alternative Systems
- [ ] **Condorcet Methods**:
  - **Condorcet Winner** — beats all others in pairwise comparison
  - **Condorcet Paradox / Cycling** — A>B>C>A, no clear winner
  - **Condorcet-completion methods** — resolve cycles (Schulze, Ranked Pairs)
- [ ] **Schulze Method** — strongest path through tournament graph
- [ ] **Borda Count** — points by rank (n-1, n-2, ..., 0)
- [ ] **Approval Voting** — vote for all acceptable candidates, most approvals wins
- [ ] **Score/Range Voting** — rate candidates 0-5, highest total wins
- [ ] **STAR Voting** — Score Then Automatic Runoff:
  - Rate 0-5, sum scores
  - Top 2 by score → automatic runoff by preferences

#### Additional Voting Methods *(from elsim)*
- [ ] **Black's Method** (Duncan Black 1958):
  - **Algorithm**: If Condorcet winner exists → elect them; else → Borda winner
  - Satisfies Condorcet criterion AND majority criterion
  - Does NOT satisfy Independence of Irrelevant Alternatives
- [ ] **Coombs Method** (Clyde Coombs):
  - **Algorithm**: Iteratively eliminate candidate with MOST last-place votes
  - Continue until a candidate has majority of first-place votes
  - **Key difference from IRV**: IRV eliminates fewest first-place; Coombs eliminates most last-place
  - Tends to elect broadly acceptable candidates
  - **Condorcet efficiency ~99%** (very high)
- [ ] **SNTV (Single Non-Transferable Vote)** — multi-winner plurality
- [ ] **Two-Round Runoff** — top 2 if no majority, then second round

### Electoral Rules

#### Thresholds
- [x] National threshold (implemented) — 0%, 5%, 10%
- [ ] **Natural/effective threshold** — 75% / (M + 1) where M = district magnitude
- [ ] **Regional thresholds**

#### Theoretical Laws
- [ ] **Duverger's Law** — FPTP → 2-party system
  - **Mechanical effect** — small parties don't win seats
  - **Psychological effect** — voters avoid "wasting" votes on small parties
- [ ] **M+1 Rule (Cox 1997)** — max viable parties ≈ district magnitude + 1

---

## 📊 METRICS & INDICES

### Disproportionality
- [x] **Gallagher Index (Least Squares)**: LSq = √(½ Σ(v_i - s_i)²)
- [ ] **Loosemore-Hanby**: D = ½ Σ|v_i - s_i|
- [ ] **Sainte-Laguë Index**: 1/2 Σ(v_i - s_i)² / v_i

### Fragmentation
- [ ] **Effective Number of Parties (Laakso-Taagepera 1979)**:
  - **N = 1 / Σ(p_i)²**
  - p_i = vote/seat share (as proportion, 0-1)
  - **ENEP** (by votes), **ENPP** (by seats)
  - Related: HHI = Σ(p_i)², N = 1/HHI (inverse Simpson index)

### Gerrymandering
- [ ] **Efficiency Gap (Stephanopoulos-McGhee 2014)**:
  - Wasted votes = losing votes + (winning votes - 50% - 1)
  - **EG = (Party A wasted - Party B wasted) / total votes**
  - **>7% threshold** suggests potential illegal gerrymandering
- [ ] **Polsby-Popper Compactness**: 4π × area / perimeter²
- [ ] **Seats-votes curve** — responsiveness and bias
- [ ] **Partisan bias** — seats deviation at 50% vote share

### Voting System Efficiency *(from elsim)*
- [ ] **Social Utility Efficiency (SUE) / Voter Satisfaction Efficiency (VSE)** (Jameson Quinn):
  - **VSE = 1 - [BR(method) / BR(Random)]**
  - **Bayesian Regret (BR)** = expected avoidable unhappiness
  - BR = average(Optimal_Utility - Elected_Utility) over many simulations
  - VSE 100% = always elects max-utility candidate; 0% = random selection
- [ ] **Condorcet Efficiency** — % elections electing Condorcet winner:
  - **Condorcet methods: 100%** (by definition)
  - **Coombs: ~99%** | **Borda: ~86%** | **IRV: ~60%** | **Plurality: ~33%**
  - RCV empirical (US since 2004): 99.6% when beats-all winner exists
- [ ] **Condorcet Cycle Likelihood** — ~3% in typical simulations
- [ ] **Utility Winner** — candidate maximizing total voter utility (benchmark)

---

## 🌐 SOCIAL NETWORKS & OPINION DYNAMICS

### Network Topologies

#### Small-World (Watts-Strogatz 1998)
- [ ] Start with ring lattice, K nearest neighbors
- [ ] **Rewiring probability p**:
  - p=0: regular lattice (high clustering, high path length)
  - p≈0.01-0.1: small-world (high clustering, short paths)
  - p=1: random graph (low clustering, short paths)
- [ ] **Clustering coefficient** — probability neighbors are connected

#### Scale-Free (Barabási-Albert 1998)
- [ ] **Preferential attachment** — "rich get richer"
- [ ] **Power-law degree distribution**: P(k) ~ k^(-γ), γ ≈ 2-3
- [ ] **Hubs** — highly connected nodes (influencers)
- [ ] Robust to random failure, vulnerable to targeted hub removal

#### Stochastic Block Model (SBM) *(from es_simulations)*
- [ ] **Community-based network generation** — topological communities
- [ ] **Core Parameters**:
  - `n` (N) = total vertices/nodes
  - `k` (K) = number of communities/blocks
  - `P` or `B` = **block matrix** (k×k): P_ij = probability of edge between community i and j
  - `z` or `C` = community assignment vector for each node
- [ ] **Electoral Parameters** (es_simulations):
  - `q` = number of districts | `qn` = sizes per district | `qs` = seats per district
  - `avg_deg` = average degree | `ra` = within/between connection ratio
- [ ] **Degree-Corrected SBM (DC-SBM)** — handles heterogeneous node degrees within communities
- [ ] **Polarization ratio q** — q=0: disconnected communities, q=1: bipartite

#### Distance-Based Planar Model *(from es_simulations)*
- [ ] **Geographic network** — connection probability based on distance
- [ ] **planar_c parameter** — fit to real commuting data using `fit_planar_c.py`
- [ ] More realistic spatial voter distribution

### Contagion & Diffusion

#### Epidemic Models for Information Spread
- [ ] **SIR (Susceptible-Infected-Recovered)**:
  - **β** = transmission rate (S→I)
  - **γ** = recovery rate (I→R)
  - **R₀ = β/γ** (basic reproduction number)
- [ ] **SEIR** — adds Exposed state:
  - **σ** = incubation rate (E→I)
- [ ] **SIS** — recovered can become susceptible again
- [ ] **SIRS** — temporary immunity before re-susceptibility
- [ ] **SVFR** — Susceptible-View-Forward-Removed (social media)

### Opinion Dynamics

#### Bounded Confidence (Hegselmann-Krause)
- [ ] **Key parameter: ε (epsilon) = confidence bound**
- [ ] Only interact if |opinion_i - opinion_j| < ε
- [ ] **Dynamics**: x_i(t+1) = average of all x_j within ε neighborhood
- [ ] **Outcomes**:
  - Large ε → consensus
  - Small ε → multiple clusters (polarization)
  - **Finite-time convergence** guaranteed
- [ ] Variants: asymmetric ε, heterogeneous ε, noise

#### Other Models
- [ ] **DeGroot** — weighted averaging from network neighbors
- [ ] **Voter Model** — randomly copy neighbor's opinion
- [ ] **Deffuant-Weisbuch** — pairwise bounded confidence

#### Noisy Voter Model *(from es_simulations)*
- [ ] **Opinion propagation** — copy neighbor's state (social influence/herding)
- [ ] **Mutation/noise parameter `ε`** — probability of spontaneous opinion change
  - High ε → more diversity, harder for single opinion to dominate
  - Low ε → social influence dominates, approaches consensus
  - **Prevents complete consensus** unlike standard voter model
- [ ] **Majority Rule** — adopt local majority opinion
- [ ] **Minority Rule** — adopt local minority (experimental, less empirically supported)

### Zealots & Media Influence *(from es_simulations, Raducha et al. 2023)*

#### Zealots
- [ ] **Fixed-opinion agents** — never change mind regardless of social pressure
- [ ] Other agents are **susceptible** — can adopt neighbors' opinions
- [ ] **Parameters**:
  - `zn` = number of zealots
  - Zealot state/party affiliation
  - Zealot connectivity/placement in network
- [ ] **Zealot susceptibility metric** — how vulnerable is electoral system to zealots?

#### Mass Media Bias
- [ ] **Media influence probability** `mm` — probability of adopting "media state" during mutation
- [ ] **Media susceptibility metric** — how vulnerable is electoral system to media bias?
- [ ] **Media vs Zealots cross-analysis** — interaction effects
- [ ] **Key finding (Raducha 2023)**: Plurality voting MORE susceptible to agitators/propaganda than PR

### Simulation Dynamics *(from es_simulations)*
- [ ] **Thermalization** — equilibration period before data collection
- [ ] **Sampling** — elections after every N steps
- [ ] **Animation** — visualize state changes over time on network

---

## 🤝 COALITION FORMATION

### Formation Strategies
- [x] **MCW (Minimum Connected Winning)** (implemented) — closest ideologically
- [ ] **MWC (Minimum Winning Coalition)** — smallest majority (Riker 1962)
- [ ] **Laver-Shepsle Portfolio Allocation Model**:
  - Parties prefer specific policy departments
  - **Policy = f(who controls which ministry)**
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

## ⏱️ GOVERNMENT STABILITY & SURVIVAL

### Collapse Models
- [x] Sigmoid (implemented)
- [x] Linear (implemented)
- [x] Exponential (implemented)
- [ ] **Survival Analysis / Duration Modeling (Warwick)**:
  - **Hazard rate h(t)** — instantaneous failure probability at time t
  - **Survival function S(t)** — probability government survives past t
  - **Cox Proportional Hazards** — h(t|X) = h₀(t) × exp(β'X)
  - Covariates: party count, ideology spread, economic conditions

### Stability Factors
- [x] Coalition strain (implemented)
- [x] Majority margin (implemented)
- [ ] Economic shocks (GDP, unemployment, inflation)
- [ ] Scandals

---

## 📈 EXTERNAL EFFECTS & SHOCKS

### Economic Voting
- [ ] **Retrospective Voting** — evaluate incumbent on past performance
- [ ] **Pocketbook voting** — based on personal financial situation
- [ ] **Sociotropic voting** — based on national economy perception (stronger effect)
- [ ] **VP Function** — Vote/Popularity as f(economic conditions)
- [ ] **Incumbency advantage** — name recognition, resources, credit-claiming

### Debate Effects
- [ ] **Minimal effects hypothesis** — campaigns mostly reinforce existing views
- [ ] ~10% of voters decide based on debates
- [ ] 72% decide >2 months before election
- [ ] **Debate bumps often temporary** — "sample artifacts"
- [ ] Primary debates more persuasive (~60% mind changes) than general election debates
- [ ] Post-debate media framing may matter more than debate content

### Scandal Effects
- [ ] **Vote penalty** — 6-11% vote share decrease for corruption
- [ ] **Corruption-voting puzzle** — some scandals have mild electoral consequences
- [ ] **Moderators**: partisanship, media coverage, scandal type (financial > moral)
- [ ] Long-term trust erosion, especially for first-time voters during scandal

### Voter Suppression
- [ ] **Voter ID laws** — 1.6-2.2 percentage point turnout decline
- [ ] **Polling place closures** — 5.65pp decline from relocation, 1,688 closures (2012-2018)
- [ ] **Wait times** — 1% decrease in future voting per hour waited, 500-700k lost votes (2012)
- [ ] Disproportionate impact: minorities, poor, elderly, young

### Poll Aggregation (538 Methodology)
- [ ] **Poll weighting** by: pollster track record, sample size, recency
- [ ] **House effects** correction for pollster bias
- [ ] **Probabilistic forecasts** — Monte Carlo simulations
- [ ] **Challenges**: 2016 state-level misses, 2020 largest error in decades (R+4.6)

---

## 🏛️ THEORETICAL FOUNDATIONS

### Social Choice Theorems

#### Arrow's Impossibility Theorem
- [ ] No ranked-choice voting system (≥3 alternatives) can satisfy all:
  1. **Unrestricted Domain** — any preference ordering allowed
  2. **Non-dictatorship** — no single voter determines outcome
  3. **Pareto Efficiency** — if all prefer A>B, society prefers A>B
  4. **Independence of Irrelevant Alternatives** — A vs B unaffected by C
  5. **Social Ordering / Transitivity** — no A>B>C>A cycles

#### Gibbard-Satterthwaite Theorem
- [ ] Any deterministic voting rule (≥3 alternatives) must be either:
  - **Dictatorial**, OR
  - **Manipulable** (strategic voting beneficial)
- [ ] Related to Arrow via IIA ↔ strategy-proofness connection
- [ ] **Pivotal voter** argument in proof

#### Median Voter Theorem (Black-Downs)
- [ ] Under majority rule + single-peaked preferences:
  - **Median voter's preferred position wins**
- [ ] **Downs Convergence** — parties move toward center in two-party systems
- [ ] **Assumptions**: single dimension, full information, two candidates
- [ ] Relaxations lead to divergence, polarization

### Party Behavior
- [ ] **Mainstream parties** track median voter, adapt to shifts
- [ ] **Niche parties** prioritize policy/ideology over median voter
- [ ] **Critical elections** — realignments from major events
- [ ] Voters may shift preferences to match preferred party (elite cue-taking)

---

## 🔧 TECHNICAL INFRASTRUCTURE

### Computational
- [ ] Parallelization, GPU, distributed computing
- [ ] 10M+ agents capacity

### Data
- [ ] Real voter file integration
- [ ] Manifesto project party positions
- [ ] Survey data import

### Validation
- [ ] **Hindcast validation** — backtest on 2020, 2016, 2012
- [ ] **Calibration curves** — predicted 70% → actual 70%?
- [ ] **Out-of-sample cross-validation**
- [ ] **Bias detection** — systematic over/under prediction

---

## 🎭 AGENT ARCHITECTURE - CANDIDATE/PARTY

### Candidate Attributes
- [ ] **Charisma** (0-100) — personal appeal, motivates constituents, can be measured via "charismometer"
- [ ] **Valence** — non-policy competence: integrity, experience, leadership, credibility
  - Accumulation is costly (campaign spending)
  - Higher impact when platforms are similar
- [ ] **Policy Position** — N-dimensional issue space (spatial model)
- [ ] **Party Affiliation** — major/minor, incumbent/challenger

### Candidate Strategy
- [ ] **Platform selection** — how candidate chooses policy positions
- [ ] **Valence investment** — allocating resources to build competence image
- [ ] **Strategic experimentation** — policy learning, reelection incentives
- [ ] **Adaptive behavior** — respond to polls, opponents, voter feedback

---

## � CAMPAIGN DYNAMICS

### Campaign Spending
- [ ] **Spending effects on vote share**:
  - **94% of House candidates** who outspent opponents won
  - **82% of Senate** winners outspent
  - 2020 cycle: **$14.4 billion** (most expensive ever)
- [ ] **Incumbent vs challenger asymmetry** — challenger spending more effective
- [ ] **Low-information voter sensitivity** — more responsive to spending
- [ ] **Diminishing returns** — marginal effect decreases at high spending

### Microtargeting
- [ ] **Psychological profiling** — Big Five from online behavior (Cambridge Analytica)
- [ ] **Single-attribute targeting** — 70% more effective than generic ads (party-based)
- [ ] **Multi-attribute targeting** — diminishing returns on complexity
- [ ] **AI-generated personalization** — generative AI scales microtargeting
- [ ] **Polarization risk** — reinforces existing beliefs, echo chambers

---

## 🇮🇳 INDIA-SPECIFIC FEATURES

### NOTA (None of the Above)
- [ ] **Supreme Court mandated (2013)** — PUCL v. Union of India
- [ ] **Current legal status**: NOTA votes counted but don't affect result
  - Candidate with next-highest votes wins even if NOTA > all candidates
- [ ] **Higher in reserved constituencies**:
  - General: **0.95%** | SC-reserved: **1.1%** | ST-reserved: **2.18%**
  - May indicate voter dissatisfaction or caste-bias
- [ ] **State-level exceptions**: Maharashtra, Haryana, Delhi (local body) — fresh elections if NOTA wins

### Reserved Constituencies
- [ ] **Constitutional reservation** — seats reserved for SC, ST, Anglo-Indian
- [ ] **Rotation policy** — delimitation-based rotation
- [ ] **Representation dynamics** — higher NOTA, different candidate pools

### Electronic Voting Machines (EVMs) & VVPAT
- [ ] **EVM security features**:
  - Standalone, battery-powered, **no network connectivity**
  - One-time programmable microcontrollers (write-once)
  - M3 model: tamper detection, self-diagnostics
  - Double randomization for EVM allocation
- [ ] **VVPAT (Voter Verifiable Paper Audit Trail)**:
  - Paper slip visible for 7 seconds, drops into sealed box
  - VVPAT slips authoritative over electronic tally
  - **5 polling stations per constituency** randomly verified (Supreme Court mandate)
- [ ] **2024 ECI protocol**: Losing candidates can request 5% microcontroller audit

---

## 🗺️ ELECTORAL GEOGRAPHY

### Redistricting Algorithms
- [ ] **Shortest Splitline** (rangevoting.org):
  - Recursively divide with shortest straight line
  - Politically/demographically blind
  - Ignores communities of interest
- [ ] **Compactness metrics** — Polsby-Popper, Reock, Convex Hull
  - **Compactness ≠ fairness** — can be compact and gerrymandered
- [ ] **Multi-objective optimization** — balance compactness + fairness criteria

### Fairness Criteria
- [ ] **Neutral process** — draw without partisan data
- [ ] **Vote-seat proportionality** — minimize efficiency gap
- [ ] **Partisan symmetry** — equal gains/losses for vote shifts
- [ ] **Competitiveness** — create more competitive districts

---

## 🗳️ NOVEL VOTING MECHANISMS

### Quadratic Voting (Weyl)
- [ ] **Cost function**: cost = votes² (1 vote = 1 credit, 2 votes = 4 credits)
- [ ] **Intensity revelation** — voters spend more on issues they care about
- [ ] **Anti-tyranny mechanism** — minorities with strong preferences can outweigh apathetic majority
- [ ] **Applications**: Colorado legislature pilot, corporate governance, blockchain DAOs
- [ ] **Book**: "Radical Markets" (Weyl & Posner)

### Liquid Democracy
- [ ] **Transitive delegation** — A delegates to B, B delegates to C, C gets A's vote
- [ ] **Direct + representative hybrid** — vote directly OR delegate
- [ ] **Revocable at any time** — promotes accountability
- [ ] **Issue-specific delegation** — different delegates for different topics
- [ ] **Blockchain implementation** — immutable, transparent, dynamic updates

### Cumulative Voting
- [ ] **Multiple votes per voter** — equal to seats being filled
- [ ] **Plumping strategy** — concentrate all votes on one candidate
- [ ] **Semi-proportional representation** — minority groups can elect representatives
- [ ] **Multi-seat districts required** — not effective in single-member
- [ ] **Used in**: Illinois (1870-1980), corporate boards, local governments

---

## 📋 BALLOT DESIGN & ADMINISTRATION

### Ballot Effects
- [ ] **Ordering bias** — first-listed candidate gets ~1-2% advantage
- [ ] **Butterfly ballot (2000)** — Palm Beach County, ~2,000 mistaken Buchanan votes
- [ ] **Donkey vote** — rank in ballot order without consideration (Australia)
- [ ] **Overvotes/undervotes** — design causes voter error

### Election Timing
- [ ] **Concurrent elections** — federal + state + local simultaneously
- [ ] **Off-cycle elections** — lower turnout, different voter composition
- [ ] **Weekend vs weekday voting** — affects working-class turnout

---

## 📜 POLITICAL REALIGNMENT THEORY

### Critical Elections (V.O. Key 1955)
- [ ] **Definition**: Sharp, durable alteration of electoral divisions
- [ ] **Characteristics**:
  - High voter concern/intensity
  - Profound readjustment of power
  - New durable electoral groupings
- [ ] **Examples**: 1896 (McKinley), 1932 (FDR New Deal), 1968 (Southern Strategy)

### Types of Realignment
- [ ] **Critical election realignment** — sudden, within 1-2 cycles
- [ ] **Secular realignment** — gradual separation over decades
- [ ] **Dealignment** — voters abandon parties, become independent

### Key's Party Components
- [ ] **Party-in-electorate** — voters who identify with party
- [ ] **Party organization** — committees, staff, infrastructure
- [ ] **Party-in-government** — elected officials, officeholders

---

## �📚 RESEARCH NOTES

### Searches Completed (48 total, 0 failed)

#### Session 1: Core Models (28)
1. ✅ Spatial voting (proximity vs directional, Rabinowitz-Macdonald 1989)
2. ✅ Probabilistic voting (MNL, random utility, McFadden)
3. ✅ Coalition formation (Laver-Shepsle portfolio allocation)
4. ✅ Turnout calculus (Riker-Ordeshook V=pB-C+D)
5. ✅ STV algorithm (Droop quota, Gregory/Meek methods)
6. ✅ Hegselmann-Krause bounded confidence (ε, clusters)
7. ✅ Duverger's Law, M+1 rule (Cox 1997)
8. ✅ Big Five personality-politics
9. ✅ Moral Foundations Theory (Haidt)
10. ✅ RWA scale (Altemeyer)
11. ✅ Watts-Strogatz small-world
12. ✅ Barabási-Albert scale-free
13. ✅ SIR/SEIR epidemic models
14. ✅ MMP electoral system (Germany)
15. ✅ Approval/STAR/Score voting
16. ✅ Condorcet winner, cycling paradox
17. ✅ Retrospective/economic voting
18. ✅ Strategic voting, wasted vote
19. ✅ Scandal effects
20. ✅ Debate effects, minimal persuasion
21. ✅ Misinformation, backfire effect
22. ✅ Poll aggregation (538 methodology)
23. ✅ Voter suppression (ID, closures, wait times)
24. ✅ Government survival analysis (Warwick)
25. ✅ Arrow Impossibility Theorem
26. ✅ Gibbard-Satterthwaite Theorem
27. ✅ Median Voter Theorem (Downs convergence)
28. ✅ Party adaptive behavior

#### Session 2: Repository Features (10)
29. ✅ Stochastic Block Model (SBM, block matrix P_ij, DC-SBM)
30. ✅ Zealot voter model (fixed agents, susceptibility metrics)
31. ✅ Noisy voter model (mutation rate ε, consensus prevention)
32. ✅ Voter Satisfaction Efficiency (VSE, Bayesian Regret, Jameson Quinn)
33. ✅ Impartial Culture (n! orderings, IAC/IANC variants)
34. ✅ Yee diagrams (Ka-Ping Yee, non-monotonicity visualization)
35. ✅ Black's method (Condorcet→Borda hybrid, Duncan Black 1958)
36. ✅ Coombs method (eliminate most last-place, ~99% Condorcet efficiency)
37. ✅ Condorcet efficiency (Coombs 99%, Borda 86%, IRV 60%, FPTP 33%)
38. ✅ Media susceptibility (Raducha 2023, plurality > PR vulnerability)

#### Session 3: Gap Research (10)
39. ✅ Candidate agent model (charisma, valence, position, strategy, ABM)
40. ✅ Campaign spending (94% outspent win, $14.4B cycle, microtargeting 70% lift)
41. ✅ India NOTA (2.18% ST vs 0.95% general, no re-election trigger)
42. ✅ Redistricting algorithms (shortest splitline, compactness ≠ fairness)
43. ✅ Quadratic Voting (cost=votes², Weyl, tyranny counter)
44. ✅ Liquid Democracy (transitive delegation, blockchain implementation)
45. ✅ Cumulative Voting (plumping, semi-proportional, minorities)
46. ✅ Political Realignment (V.O. Key 1955, critical elections, 1896/1932)
47. ✅ Ballot design effects (butterfly 2000, ordering bias, donkey vote)
48. ✅ India EVM/VVPAT (standalone, 5-station audit, microcontroller verification)

---

## 🏷️ LEGEND

- [x] = Implemented
- [ ] = Not implemented
- **Bold** = Has detailed specification with formula/parameters

