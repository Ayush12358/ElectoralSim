# ElectoralSim - Comprehensive TODO

## 🗳️ ELECTORAL SYSTEMS

### Seat Allocation Methods
- [x] Sainte-Laguë (implemented)
- [x] D'Hondt (implemented, unused)
- [ ] Hare quota + largest remainder
- [ ] Droop quota
- [ ] Imperiali quota
- [ ] Modified Sainte-Laguë (first divisor 1.4)
- [ ] Huntington-Hill (US apportionment)

### Electoral System Types
- [x] Party-list PR (current)
- [ ] **FPTP** (First Past The Post) - single-member districts
- [ ] **MMP** (Mixed-Member Proportional) - Germany/NZ style
- [ ] **STV** (Single Transferable Vote) - ranked choice, multi-member
- [ ] **RCV/IRV** (Ranked Choice Voting) - single-winner
- [ ] **AV** (Alternative Vote) - Australia lower house
- [ ] **Two-round runoff** - France presidential
- [ ] **Parallel voting** - Japan style (no compensation)
- [ ] **Borda count** - points-based ranking
- [ ] **Approval voting** - vote for all acceptable candidates
- [ ] **STAR voting** - Score Then Automatic Runoff
- [ ] **Condorcet methods** - pairwise comparisons

### Thresholds & Barriers
- [x] National threshold (implemented)
- [ ] Regional thresholds
- [ ] Effective threshold (natural district barrier)
- [ ] Coalition thresholds (joint lists exempt)
- [ ] Apparentement (list alliances)

### District Structure
- [x] Single national district (current)
- [ ] **Multi-district** - regional constituencies
- [ ] **Variable magnitude** - different seats per district
- [ ] **Gerrymandering simulation** - biased boundaries
- [ ] **Malapportionment** - unequal population per seat

---

## 🧑‍🤝‍🧑 VOTER BEHAVIOR

### Spatial Voting Models
- [x] Proximity model (implemented) - vote for closest
- [ ] **Directional model** - vote for party in preferred direction
- [ ] **Discounting model** - discount extreme positions
- [ ] **Unified model** - combine proximity + directional
- [ ] **Proximity with intensity** - care more about some dimensions

### Vote Choice Mechanisms
- [x] Deterministic (argmax) (implemented)
- [ ] **Probabilistic (softmax/logit)** - stochastic choice
- [ ] **Satisficing** - vote for first "good enough" party
- [ ] **Lexicographic** - most important issue first
- [ ] **Compensatory** - trade-offs between issues

### Voter Heterogeneity
- [x] Uniform distribution (implemented)
- [x] Symmetric polarization (implemented)
- [x] Asymmetric polarization (implemented)
- [ ] **Multi-modal** - 3+ clusters
- [ ] **Empirical distributions** - real survey data
- [x] Patronage affinity (implemented)
- [ ] **Weighted dimensions** - issue salience per voter
- [ ] **Partisan attachment** - party ID beyond ideology
- [ ] **Demographic segments** - age, income, education, region

### Turnout & Abstention
- [ ] **Alienation** - don't vote if all parties too far
- [ ] **Indifference** - don't vote if parties too similar
- [ ] **Rational ignorance** - cost-benefit calculation
- [ ] **Civic duty** - vote regardless of outcome
- [ ] **Weather/convenience effects**
- [ ] **Compulsory voting**

### Information & Psychology
- [ ] **Imperfect information** - voters don't know party positions
- [ ] **Bandwagon effect** - vote for expected winner
- [ ] **Underdog effect** - vote for expected loser
- [ ] **Strategic voting** - avoid wasted votes
- [ ] **Expressive voting** - vote to express identity
- [ ] **Retrospective voting** - reward/punish incumbents
- [ ] **Economic voting** - based on economy

---

## 🏛️ PARTY BEHAVIOR

### Party Positioning
- [x] Random fixed positions (implemented)
- [ ] **Downsian convergence** - move to median voter
- [ ] **Policy-seeking** - maintain ideological integrity
- [ ] **Vote-maximizing** - adaptive repositioning
- [ ] **Niche party strategies** - target specific segments
- [ ] **Valence competition** - non-policy attributes

### Party Dynamics
- [ ] **Party entry/exit** - new parties form, old ones die
- [ ] **Party splits** - internal factions break away
- [ ] **Party mergers** - combine to win threshold
- [ ] **Coalition pre-announcements** - declare partners before election
- [ ] **Candidate selection** - primary elections

### Party Resources
- [x] Patronage score (implemented)
- [ ] **Campaign spending**
- [ ] **Media access**
- [ ] **Organizational strength**
- [ ] **Incumbency advantage**

---

## 🤝 COALITION FORMATION

### Formation Strategies
- [x] MCW - Minimum Connected Winning (implemented)
- [ ] **MWC** - Minimum Winning (size only)
- [ ] **Policy-seeking** - minimize policy distance
- [ ] **Office-seeking** - maximize portfolios
- [ ] **Bargaining model** - sequential negotiations
- [ ] **Formateur model** - largest party tries first
- [ ] **Minority government** - govern without majority
- [ ] **Grand coalition** - left + right

### Coalition Dynamics
- [x] Coalition strain (implemented)
- [ ] **Portfolio allocation** - who gets which ministry
- [ ] **Policy compromise** - weighted average position
- [ ] **Junior partner discount** - smaller parties lose support
- [ ] **Coalition discipline** - voting together

### Government Types
- [ ] **Single-party majority**
- [ ] **Single-party minority**
- [ ] **Multi-party majority coalition**
- [ ] **Multi-party minority coalition**
- [ ] **Confidence and supply**
- [ ] **Technocratic government**

---

## ⏱️ STABILITY & SURVIVAL

### Collapse Models
- [x] Sigmoid (implemented)
- [x] Linear (implemented)
- [x] Exponential (implemented)
- [ ] **Hazard/survival analysis** - proper statistical model
- [ ] **Event-triggered** - specific crises cause collapse
- [ ] **Cumulative stress** - stress builds over time

### Stability Factors
- [x] Coalition strain (implemented)
- [x] Majority margin (implemented)
- [x] Coalition penalty (implemented)
- [ ] **Economic shocks** - GDP, unemployment
- [ ] **Scandals** - random corruption events
- [ ] **External crises** - war, pandemic
- [ ] **Public opinion polls** - approval ratings
- [ ] **Legislative defeats** - failed votes

---

## 📊 METRICS & OUTPUTS

### Disproportionality
- [x] Gallagher Index (implemented)
- [ ] Loosemore-Hanby Index
- [ ] Sainte-Laguë Index
- [ ] Rae Index

### Fragmentation
- [ ] **Effective Number of Parties (ENP)**
- [ ] **Fractionalization Index**
- [ ] **Concentration ratio** (top 2 parties share)

### Representation
- [ ] **Voter satisfaction** - how many voters got 1st choice
- [ ] **Wasted votes** - votes for losing candidates
- [ ] **Mandates per seat** - votes needed per seat

### Competitiveness
- [ ] **Margin of victory**
- [ ] **Swing ratio** - seats/votes elasticity
- [ ] **Safe seats** - uncompetitive districts

---

## 🔄 TIME EVOLUTION (True ABM)

### Dynamic Elements
- [ ] **Multiple election cycles** - simulate 10-20 elections
- [ ] **Voter preference drift** - gradual ideology change
- [ ] **Party repositioning** - parties adapt to results
- [ ] **Generational replacement** - old voters die, new enter
- [ ] **Issue evolution** - new dimensions emerge
- [ ] **Social influence** - voters influence neighbors

### Network Effects
- [ ] **Social networks** - voters on graph
- [ ] **Opinion dynamics** - DeGroot, bounded confidence
- [ ] **Echo chambers** - homophily in networks
- [ ] **Media influence** - broadcast effects
- [ ] **Misinformation spread**

---

## 🌍 GEOGRAPHY & DEMOGRAPHICS

### Spatial Structure
- [ ] **Geographic regions** - urban/rural/suburban
- [ ] **Regional parties** - only compete in some areas
- [ ] **Federalism** - state vs national elections
- [ ] **Population distribution** - density maps

### Demographics
- [ ] **Age cohorts** - young vs old voting patterns
- [ ] **Income distribution** - class voting
- [ ] **Education levels**
- [ ] **Ethnic/religious groups**
- [ ] **Urban-rural divide**

---

## 🔧 TECHNICAL INFRASTRUCTURE

### Performance
- [ ] **Parallelization** - multi-core simulation
- [ ] **GPU acceleration** - massive agent counts
- [ ] **Distributed computing** - cluster support

### User Interface
- [ ] **Web UI** - interactive parameter tuning
- [ ] **Real-time visualization** - watch simulation run
- [ ] **Configuration files** - YAML/JSON parameters
- [ ] **CLI interface** - command-line options

### Data & Validation
- [ ] **Real-world calibration** - fit to historical elections
- [ ] **Manifesto data integration** - real party positions
- [ ] **Survey data** - real voter distributions
- [ ] **Sensitivity analysis** - automated sweeps
- [ ] **Unit tests** - comprehensive test suite

### Output & Analysis
- [ ] **Interactive dashboards**
- [ ] **Automatic figure generation**
- [ ] **Statistical summaries**
- [ ] **Export to R/Python**

---

## 🎓 THEORETICAL FOUNDATIONS

### Classic Theorems to Test
- [ ] **Duverger's Law** - FPTP → 2 parties
- [ ] **Median Voter Theorem** - convergence to center
- [ ] **Arrow's Impossibility** - no perfect system
- [ ] **Gibbard-Satterthwaite** - strategic voting inevitable
- [ ] **May's Theorem** - majority rule uniqueness

### Research Questions
- [ ] Electoral system → party system mapping
- [ ] Threshold effects on fragmentation
- [ ] Clientelism vs accountability trade-off
- [ ] Coalition stability determinants
- [ ] Strategic voting under different systems

---

## 📝 DOCUMENTATION & COMMUNITY

- [ ] **API documentation**
- [ ] **Tutorial notebooks**
- [ ] **Example scenarios** - replicate real elections
- [ ] **Contribution guidelines**
- [ ] **Academic paper** - if ever needed

---

## 🏷️ PRIORITY LEGEND

- [x] = Implemented
- [ ] = Not implemented
- **Bold** = High priority / commonly requested
