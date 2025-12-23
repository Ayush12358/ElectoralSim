# ElectoralSim - Comprehensive TODO

> **Reference:** See `election_abm_part1.md`, `election_abm_part2.md`, `election_abm_part3.md` for detailed specifications (~8,500 lines of documentation).

---

## 🧠 AGENT ARCHITECTURE - VOTER

### Core Voter Attributes
- [ ] **Immutable Demographics** — age, gender, race, citizenship, registration status
- [ ] **Mutable Demographics** — address, marital status, children, employment, education, religion
- [ ] **Socioeconomic Status** — income, wealth, debt, financial stress, credit score
- [ ] **Social Position** — family structure, social integration, loneliness, volunteer participation

### Political Identity
- [ ] **Party Identification** — registered party, party strength, switching history
- [ ] **Partisan Affects** — in-group favorability, out-group favorability, partisan animosity
- [ ] **Ideological Identity** — self-placement, issue-by-issue ideology, flexibility

### Psychological Profile (Big Five + More)
- [x] Basic ideology dimensions (implemented)
- [ ] **Openness** — correlates with progressive views
- [ ] **Conscientiousness** — correlates with rule-following
- [ ] **Extraversion** — enables political engagement
- [ ] **Agreeableness** — correlates with social safety net support
- [ ] **Neuroticism** — correlates with threat sensitivity
- [ ] **Authoritarianism** — preference for strong leadership
- [ ] **Moral Foundations** — Care, Fairness, Loyalty, Authority, Sanctity, Liberty
- [ ] **Cognitive Complexity** — simple vs. nuanced thinking
- [ ] **Motivated Reasoning** — directional bias, confirmation bias, accuracy motivation

### Voter Knowledge & Information
- [ ] **Candidate Knowledge** — recognition, position knowledge, character knowledge
- [ ] **Issue Knowledge** — economic facts, policy understanding
- [ ] **Information Sources** — news consumption patterns, media diet
- [ ] **Source Trust** — trust in mainstream media, social media, experts
- [ ] **Misinformation Susceptibility** — belief, exposure, resistance, conspiracy thinking

### Policy Preferences
- [ ] **Issue Positions** — economy, healthcare, immigration, crime, environment, education, social, foreign policy
- [ ] **Issue Salience** — importance rankings, personal vs. national, emotional engagement

### Emotional States
- [ ] **Baseline Emotions** — anger, fear, sadness, disgust, hope, pride, happiness
- [ ] **Emotional Targets** — anger at candidate/government/groups
- [ ] **Emotional Volatility** — stability, responsiveness, recovery
- [ ] **Candidate Affect** — warmth, enthusiasm, resentment toward candidates

### Behavior Patterns
- [ ] **Voting History** — past participation, vote choice, voting streak
- [ ] **Voting Method** — mail, early, election day preferences
- [ ] **Campaign Participation** — contact history, events, volunteering, donations, social media sharing

---

## 👥 VOTER SOCIAL NETWORKS

### Network Structure
- [ ] **Network Composition** — size, tie strength, geographic dispersion, homogeneity
- [ ] **Network Density** — clustering, small-world property, bridging
- [ ] **Information Flow** — percentage of political info from network, echo chamber effect

### Network Topologies (ABM)
- [ ] **Small-World (Watts-Strogatz)** — high clustering, short paths
- [ ] **Scale-Free (Barabási-Albert)** — power-law, influencer hubs
- [ ] Random networks (Erdős–Rényi)
- [ ] Real social network data import

### Contagion & Diffusion
- [ ] **SIR/SEIR Models** — information spread as epidemic
- [ ] **Independent Cascade** — viral spread
- [ ] **Linear Threshold** — threshold-based adoption
- [ ] **Complex Contagion** — require multiple exposures
- [ ] **Information Cascades** — herding, cascade failure, reversal

### Opinion Dynamics
- [ ] **Bounded Confidence** — only interact with similar
- [ ] **DeGroot Model** — weighted averaging
- [ ] **Memetic Evolution** — ideas mutate, replicate, selection
- [ ] **Social Laser Theory** — coherent mass actions

### Influencers
- [ ] **Opinion Leaders** — reach, trust, platform
- [ ] **Adoption Curves** — innovators, early adopters, majority, laggards

---

## 🎭 CANDIDATE ARCHITECTURE

### Candidate Identity
- [ ] **Demographics** — name, age, gender, race, religion, marital status, children
- [ ] **Background** — birthplace, education, occupation, military service, public positions

### Character & Traits
- [ ] **Big Five Personality**
- [ ] **Character Strengths** — honesty, integrity, competence, leadership, vision, empathy
- [ ] **Character Flaws** — dishonesty, incompetence, corruption, scandals, controversy

### Positioning
- [ ] **Issue Positions** — same dimensions as voters
- [ ] **Position Clarity** — specificity, consistency, flip-flopping
- [ ] **Positioning Strategy** — base vs. swing, message modulation

### Campaign Resources
- [ ] **Staffing** — manager, communications, field, finance, digital, data directors
- [ ] **Organizational Capacity** — structure, decision-making, internal culture
- [ ] **Physical Infrastructure** — HQ, field offices, equipment, technology

### Financial Resources
- [ ] **Fundraising** — total raised, donor count, small/large donors, Super PAC, outside spending
- [ ] **Campaign Budget** — advertising, staff, field, digital, overhead allocation
- [ ] **Candidate Effort** — time commitment, stamina, health

---

## 🧠 DECISION-MAKING MODELS

### Rational Choice
- [x] Spatial voting / proximity (implemented)
- [ ] **Expected Utility Maximization** — calculate utility for each candidate
- [ ] **Cost-Benefit Voting** — time cost, effort cost, expected benefit

### Affective/Emotional
- [ ] **Feelings as Information** — gut feeling, mood effects
- [ ] **Enthusiasm Mobilization** — campaign enthusiasm increases turnout
- [ ] **Negative Emotion Effects** — anger, fear effects on turnout

### Heuristic-Based
- [ ] **Party Heuristic** — vote by party label
- [ ] **Incumbent Heuristic** — default to incumbent
- [ ] **Similarity Heuristic** — vote for similar candidate
- [ ] **Likeable Heuristic** — personality-driven voting
- [ ] **Appearance Heuristic** — attractiveness bias
- [ ] **Credential Heuristic** — assume expertise from credentials
- [ ] **Elite Heuristic** — follow trusted elites

### Identity-Based
- [ ] **Social Identity** — group identification strength, salience
- [ ] **In-Group Bias** — favor in-group candidates
- [ ] **Group Loyalty** — vote for group even if disagree

### Voting Logic
- [x] Deterministic (argmax) (implemented)
- [ ] **Probabilistic (softmax/logit)**
- [ ] **Retrospective Voting** — evaluate incumbents
- [ ] **Prospective Voting** — forecast future performance
- [ ] **Strategic Voting** — vote 2nd choice to block worst
- [ ] **Directional Voting** — vote for party in preferred direction

---

## � CAMPAIGN OPERATIONS

### Message Strategy
- [ ] **Economic Message** — jobs, wages, inflation, trade
- [ ] **Healthcare Message** — coverage, cost, quality
- [ ] **Safety/Crime Message** — policing, criminal justice
- [ ] **Democracy Message** — institutions, voting access
- [ ] **Cultural Message** — values, identity
- [ ] **Immigration Message** — border, pathway, economics
- [ ] **Climate Message** — green energy, jobs, independence

### Message Types
- [ ] **Positive Messages** — vision, accomplishments, hope
- [ ] **Negative Messages (Attack)** — opponent record, flaws, fear
- [ ] **Contrast Messages** — comparative ads

### Message Targeting
- [ ] **Demographic Targeting** — by age, gender, race, education, religion, geography
- [ ] **Issue Prioritization by Group**
- [ ] **Tone Adaptation** — aggressive vs. conciliatory

---

## 📺 MEDIA & INFORMATION

### Traditional Media
- [ ] **News Outlets** — broadcast, cable, newspapers, online, radio
- [ ] **Coverage Patterns** — amount, tone, focus (horse race vs. issues), balance
- [ ] **News Factors** — what gets covered (gaffes, scandals, debates)
- [ ] **Editorial Positions** — endorsements, op-eds

### Polling & Forecasting
- [ ] **Poll Methodology** — sample, questionnaire, margin of error, house effect
- [ ] **Poll Timing** — benchmark, tracking, post-event, pre-election
- [ ] **Poll Effects** — debate bumps, scandal drops, recovery time

---

## 🗳️ ELECTORAL SYSTEMS

### Seat Allocation Methods
- [x] Sainte-Laguë (implemented)
- [x] D'Hondt (implemented, unused)
- [ ] Hare quota + largest remainder
- [ ] Droop quota
- [ ] Huntington-Hill

### Electoral System Types
- [x] Party-list PR (current)
- [ ] **FPTP** (First Past The Post)
- [ ] **MMP** (Mixed-Member Proportional)
- [ ] **STV** (Single Transferable Vote)
- [ ] **RCV/IRV** (Ranked Choice)
- [ ] **Condorcet Methods**
- [ ] **Schulze Method**
- [ ] **Borda Count**
- [ ] **Two-round runoff**
- [ ] **Approval voting**
- [ ] **STAR voting**

### Voting Methods
- [ ] **In-person voting**
- [ ] **Early voting**
- [ ] **Mail/absentee voting**
- [ ] **Drop box**

### Ballot Design
- [ ] **Candidate order effects**
- [ ] **Ballot clarity**
- [ ] **Straight-ticket option**

### Voting Technology
- [ ] **Paper ballots**
- [ ] **Optical scan**
- [ ] **DRE touchscreen**
- [ ] **Accessibility**

### Thresholds
- [x] National threshold (implemented)
- [ ] Regional thresholds
- [ ] Effective threshold (natural barrier)

---

## 🗺️ ELECTORAL GEOGRAPHY

### District Structure
- [x] Single national district (current)
- [ ] Multi-district constituencies
- [ ] Variable magnitude districts
- [ ] **MCMC Redistricting** — Markov Chain Monte Carlo

### Gerrymandering Metrics
- [ ] **Efficiency Gap**
- [ ] **Compactness scores**
- [ ] **Polsby-Popper score**

---

## 🤝 COALITION FORMATION

### Formation Strategies
- [x] MCW - Minimum Connected Winning (implemented)
- [ ] MWC - Minimum Winning
- [ ] Policy-seeking coalitions
- [ ] Office-seeking coalitions
- [ ] Bargaining model
- [ ] Formateur model
- [ ] Minority government
- [ ] Grand coalition

### Coalition Dynamics
- [x] Coalition strain (implemented)
- [ ] Portfolio allocation
- [ ] Policy compromise

---

## ⏱️ STABILITY & SURVIVAL

### Collapse Models
- [x] Sigmoid (implemented)
- [x] Linear (implemented)
- [x] Exponential (implemented)
- [ ] **Hazard/survival analysis**
- [ ] Event-triggered collapse

### Stability Factors
- [x] Coalition strain (implemented)
- [x] Majority margin (implemented)
- [ ] Economic shocks
- [ ] Scandals

---

## ⚔️ EXTERNAL EVENTS & SHOCKS

### Economic Events
- [ ] **Macro Indicators** — GDP, unemployment, inflation, wages, stock market
- [ ] **Economic Shocks** — recession, financial crisis, inflation spike

### Security Events
- [ ] **Terrorism** — timing, severity, attribution, rally effect
- [ ] **War/Military Conflict** — casualties, duration, public support
- [ ] **Public Health Crisis** — pandemic, health emergency

### Scandals
- [ ] **Scandal Types** — corruption, immorality, incompetence, hypocrisy, discrimination
- [ ] **Scandal Dynamics** — breaks, coverage, response, narrative formation, decay

### October Surprises
- [ ] **Late-campaign events** — scandals, economic crashes, discoveries

---

## 📊 DATA & ANALYTICS

### Data Sources
- [ ] **First-Party Data** — voter contact, events, digital engagement, fundraising, volunteers, CRM
- [ ] **Voter File** — registration, address, party, voting history
- [ ] **Consumer Data** — demographics, lifestyle, propensity scores
- [ ] **Social Media Data** — posts, engagement, sentiment, influencer identification

### Analytics & Modeling
- [ ] **Voter Segmentation** — demographic, behavioral, psychographic
- [ ] **Predictive Models** — logistic regression, random forest, neural networks
- [ ] **Model Evaluation** — accuracy, AUC, cross-validation

---

## 📈 VISUALIZATION & DASHBOARDS

- [ ] **Real-time vote tracking**
- [ ] **State/county/precinct maps**
- [ ] **Demographic breakdowns**
- [ ] **Polling and forecast displays**
- [ ] **Confidence intervals and uncertainty**

---

## ⏰ TEMPORAL DYNAMICS

### Campaign Phases
- [ ] **Pre-Campaign** — consideration, informal fundraising
- [ ] **Announcement Phase** — initial coverage, staff hiring
- [ ] **Early Campaign** — grassroots organizing, initial ads
- [ ] **Mid-Campaign** — debates announced, polling movement
- [ ] **Late Campaign** — heavy advertising, GOTV
- [ ] **Final Stretch** — saturation, daily coverage
- [ ] **Election Day** — voting, exit polls
- [ ] **Post-Election** — transition, recount, litigation

### Attention Dynamics
- [ ] **Media attention cycles** — baseline, event spikes, decay
- [ ] **Voter attention ramp** — low early, accelerates
- [ ] **Polling volatility** — high early, stabilizes late
- [ ] **Undecided voter dynamics** — decreases over time

---

## 🎲 STOCHASTIC SYSTEMS

### Random Elements
- [ ] **Polling error** — sampling, systematic, house effects
- [ ] **Model error** — specification, parameter uncertainty
- [ ] **Event uncertainty** — when/if scandal breaks, severity

### Agent Stochasticity
- [ ] **Probabilistic vote choice** — P(vote A) = f(characteristics)
- [ ] **Probabilistic turnout**
- [ ] **Campaign effectiveness uncertainty**

### Probability Distributions
- [ ] Normal, Binomial, Poisson, Multinomial, Beta, Dirichlet

---

## 🔄 FEEDBACK LOOPS

### Positive Feedback (Amplifying)
- [ ] **Success Spiral** — ahead in polls → more coverage → more support → bigger lead
- [ ] **Momentum Loop** — momentum → more volunteers → more contact → more support
- [ ] **Funding Spiral** — more money → more ads → more support → more donors

### Negative Feedback (Dampening)
- [ ] **Defeat Spiral** — losing → skeptical coverage → less support → less funding
- [ ] **Scandal Dampening** — scandal → coverage → support drops → coverage fades → possible recovery

### Interaction Effects
- [ ] **Message × Susceptibility** — fear message effective on threat-sensitive voters
- [ ] **Candidate × Context** — experienced candidate performs well in crisis
- [ ] **Spending × Awareness** — diminishing returns as awareness increases
- [ ] **Network × Ideology** — echo chamber amplifies

---

## ✅ VALIDATION & CALIBRATION

### Historical Backtesting
- [ ] **Hindcast Validation** — test on 2020, 2016, 2012 elections
- [ ] **Error Analysis** — understand why wrong
- [ ] **Bias Detection** — systematic over/under prediction

### Model Calibration
- [ ] **Probability Calibration** — predicted 70% → actually won 70%?
- [ ] **Calibration Curves** — 45-degree line = perfect
- [ ] **Confidence Interval Coverage**

---

## 🏛️ INSTITUTIONS

### Election Administration
- [ ] **Registration Systems** — deadlines, purging, verification
- [ ] **Polling Place Management** — number, location, hours, wait times
- [ ] **Vote Counting** — transparency, audits, certification, recounts

### Campaign Finance
- [ ] **Contribution Limits** — individual, corporate, Super PAC, disclosure
- [ ] **Spending Restrictions** — legal vs. illegal, FEC enforcement
- [ ] **Dark Money** — non-disclosed spending

---

## 🤖 AI & ADVANCED METHODS

### LLM Integration
- [ ] **LLM as Voter Agent** — personality prompting, behavior consistency
- [ ] **Content Generation** — speeches, messages, attack ads
- [ ] **Sentiment Analysis** — social media, trigger identification
- [ ] **Misinformation Detection/Generation**

### Machine Learning
- [ ] **Reinforcement Learning** — campaign learns optimal strategy
- [ ] **Causal Inference** — causal effect estimation, counterfactuals
- [ ] **Transfer Learning** — apply model to new elections

---

## 🏗️ IMPLEMENTATION

### Data Architecture
- [ ] **Data Warehouse** — star schema, fact/dimension tables
- [ ] **Data Quality** — duplicate detection, validation, audit trail
- [ ] **Privacy & Security** — encryption, access control, anonymization

### Computational Infrastructure
- [ ] **Distributed Computing** — parallel processing, GPU, cloud
- [ ] **Simulation Execution** — 10M+ agents, checkpointing, random seeds
- [ ] **Containerization & Orchestration**

### Challenges
- [ ] **Missing Data** — imputation methods
- [ ] **Model Specification** — complexity vs. accuracy tradeoff
- [ ] **Generalizability** — does 2020 model work on 2024?

### Ethical Considerations
- [ ] **Informed Consent** — privacy, transparency
- [ ] **Manipulation Risk** — exploit biases, misinformation targeting
- [ ] **Equity & Fairness** — model bias, differential impact
- [ ] **Transparency & Accountability** — explainability, audit

---

## 📊 METRICS & OUTPUTS

### Disproportionality
- [x] Gallagher Index (implemented)
- [ ] Loosemore-Hanby Index
- [ ] Sainte-Laguë Index

### Fragmentation
- [ ] **Effective Number of Parties (ENP)**
- [ ] Fractionalization Index

### Other Metrics
- [ ] Voter satisfaction
- [ ] Wasted votes
- [ ] Swing ratio
- [ ] Margin of victory

---

## 🎓 THEORETICAL FOUNDATIONS

- [ ] **Duverger's Law** — FPTP → 2 parties
- [ ] **Median Voter Theorem** — convergence
- [ ] **Arrow's Impossibility**
- [ ] **Gibbard-Satterthwaite**
- [ ] May's Theorem

---

## 🔮 ESOTERIC & FRONTIER

- [ ] **Panarchism** — non-territorial governance
- [ ] **Psychohistory** — mass populations as fluid dynamics
- [ ] **Quantum Cognition** — superposition, interference in decisions
- [ ] **Cliodynamics** — secular cycles, Political Stress Indicator (Ψ)

---

## 🏷️ LEGEND

- [x] = Implemented
- [ ] = Not implemented
- **Bold** = High priority / interesting
