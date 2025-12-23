# ELECTION ABM COMPLETE ENCYCLOPEDIA - PART 1
## Voter & Candidate Architecture, Psychological Models, Decision-Making

---

# 1. VOTER AGENT ARCHITECTURE

## 1.1 Core Voter Attributes

### 1.1.1 Identity & Demographics
- **Immutable Demographics:**
  - Age (continuous: 18-120 years old)
  - Date of birth (specific calendar date)
  - Gender identity (male, female, non-binary, other)
  - Race/ethnicity (White, Black, Hispanic, Asian, Native American, Middle Eastern, Mixed, Other)
  - Citizenship status (citizen, permanent resident, non-citizen)
  - Voter registration status (registered, unregistered)
  - Registration date (when registered to vote)
  - Party registration (Republican, Democrat, Independent, other, unaffiliated)
  - State of residence (which state)
  - County of residence (which county)
  - Precinct assignment (voting precinct)
  - Legislative district (state house, senate)
  - Congressional district (U.S. House)
  
- **Mutable Demographics:**
  - Address (current, updated when moves)
  - Marital status (single, married, divorced, widowed, domestic partnership)
  - Number of children (0, 1, 2, 3+)
  - Ages of children (if have children)
  - Employment status (employed, unemployed, retired, student, disabled)
  - Occupation (job title, industry)
  - Education level (high school, some college, college, graduate)
  - College major/field (if college degree)
  - Religious affiliation (Christian, Jewish, Muslim, Hindu, Buddhist, unaffiliated, atheist, agnostic, other)
  - Religious attendance (never, rarely, sometimes, regularly, very regularly)
  - Language(s) spoken (English, Spanish, Mandarin, etc.)
  - Nativity (native-born vs. immigrant, if immigrant: country of origin)
  - Years in country (if immigrant)
  - Military service (current, veteran, never served)
  - Health status (excellent, good, fair, poor)
  - Disability status (has disability, type)
  - Homeowner (yes/no, if yes: home value)
  - Urban/rural/suburban (type of area lived in)

### 1.1.2 Socioeconomic Status
- **Income Attributes:**
  - Household income (annual, $0-$500,000+)
  - Income percentile (10th, 25th, 50th, 75th, 90th)
  - Income trend (increasing, stable, decreasing)
  - Personal income (distinct from household)
  - Spouse income (if applicable)
  - Child support/alimony received
  - Government benefits received (SNAP, SSI, unemployment, etc.)
  - Number of income sources (one job, side gig, investments, etc.)
  
- **Wealth & Assets:**
  - Home equity (home value - mortgage)
  - Savings (liquid savings amount)
  - Investments (stocks, bonds, crypto, retirement accounts)
  - Debt (mortgage, student loans, credit card, car loans)
  - Net worth (total assets - total liabilities)
  - Credit score (300-850)
  - Bankruptcy history (ever filed, when)
  - Foreclosure history (ever foreclosed, when)
  
- **Financial Stress:**
  - Financial security level (very secure, secure, neutral, worried, very worried)
  - Can afford unexpected $1,000 expense (yes/no)
  - Paying bills on time (always, usually, sometimes, rarely)
  - Medical debt (has/no)
  - College debt (has/no, amount if yes)
  - Debt-to-income ratio (total debt / annual income)

### 1.1.3 Social Position
- **Family Structure:**
  - Living with partner (yes/no, gender, relationship length)
  - Number of dependents (people financially responsible for)
  - Caregiving responsibilities (children, elderly parents, others)
  - Household composition (solo, couple, family, roommates, multigenerational)
  - Multigenerational household (yes/no, who in household)
  
- **Social Integration:**
  - Social connections (number of close friends)
  - Volunteer participation (hours/month, type)
  - Community involvement (civic group membership)
  - Social isolation level (very isolated, isolated, average, connected, very connected)
  - Loneliness level (very lonely, lonely, average, connected, not lonely)
  - Social media usage (none, minimal, moderate, heavy, very heavy)
  - In-person social activity (frequency)
  - Sense of community (feels part of community, doesn't)
  
- **Occupational Status:**
  - Employment type (full-time, part-time, self-employed, unemployed, retired, student, stay-at-home, disabled)
  - Job stability (very stable, stable, uncertain, unstable, very unstable)
  - Job satisfaction (very unsatisfied, unsatisfied, neutral, satisfied, very satisfied)
  - Union membership (yes/no)
  - Professional status (blue-collar, white-collar, service, agricultural)
  - Work location (office, home, field, retail/service, other)
  - Work schedule (fixed, flexible, shift work, variable)

---

# 2. VOTER POLITICAL ATTRIBUTES

## 2.1 Political Identity

### 2.1.1 Partisan Identity
- **Party Identification:**
  - Registered party (Republican, Democrat, Independent, Green, Libertarian, other, unregistered)
  - Party strength (pure independent, lean R, weak R, strong R, pure Democrat, lean D, weak D, strong D)
  - Party switching history (has voter changed party registration, when)
  - Partisan identity consistency (party registration = self-identification = voting behavior)
  - Switching propensity (likely to switch parties in future, yes/no/maybe)
  
- **Partisan Affects:**
  - In-group favorability (how favorable toward own party, 0-100 scale)
  - Out-group favorability (how favorable toward opposing party, 0-100 scale)
  - Partisan animosity (intensity of dislike for other party, 0-100 scale)
  - Partisan affective polarization (gap between in-group and out-group favorability)
  - Straight-ticket voting tendency (votes for entire party ticket, 0-100% probability)

### 2.1.2 Ideological Identity
- **Ideology Self-Placement:**
  - Self-identified ideology (very liberal, liberal, moderate, conservative, very conservative)
  - Consistency across issues (all views liberal, or mixed liberal/conservative)
  - Ideological strength (weak ideology, strong ideology)
  - Ideological flexibility (willing to consider other views, rigid)
  - Ideological purity (must all views align, or flexible)
  
- **Issue-by-Issue Ideology:**
  - Economic ideology (beliefs about capitalism, regulation, redistribution)
  - Social ideology (beliefs about LGBTQ rights, abortion, religion, drugs)
  - Immigration ideology (beliefs about immigration policy, border security)
  - Foreign policy ideology (interventionism, isolationism, military spending)
  - Environmental ideology (environmental regulation, climate action)
  - Criminal justice ideology (police, prisons, rehabilitation)
  - Education ideology (public vs. private, standardized testing, curriculum)

---

# 3. VOTER PSYCHOLOGICAL PROFILE

## 3.1 Personality Traits

### 3.1.1 Big Five Personality Dimensions
- **Openness to Experience:**
  - Trait level (0-100 scale, 0=closed, 100=very open)
  - Manifestations: curiosity, creativity, willingness to try new things
  - Political relevance: openness correlates with progressive policy support
  - Subtraits: imagination, interest in diversity, adventurousness
  
- **Conscientiousness:**
  - Trait level (0-100 scale)
  - Manifestations: organization, discipline, responsibility, planning
  - Political relevance: conscientiousness correlates with rule-following, law-and-order
  - Subtraits: self-discipline, orderliness, sense of duty
  
- **Extraversion:**
  - Trait level (0-100 scale)
  - Manifestations: sociability, talkativeness, assertiveness
  - Political relevance: extraversion enables political engagement, social persuasion
  - Subtraits: sociability, gregariousness, assertiveness
  
- **Agreeableness:**
  - Trait level (0-100 scale)
  - Manifestations: cooperation, empathy, compassion, trust
  - Political relevance: agreeableness correlates with social safety net support
  - Subtraits: trust, morality, altruism, cooperation
  
- **Neuroticism/Emotional Stability:**
  - Trait level (0-100 scale, 0=emotionally stable, 100=neurotic)
  - Manifestations: anxiety, sadness, anger, self-consciousness
  - Political relevance: neuroticism correlates with threat sensitivity, conservatism
  - Subtraits: anxiety, anger, depression, vulnerability

### 3.1.2 Other Personality Dimensions
- **Authoritarianism:**
  - Trait level (0-100 scale, 0=libertarian, 100=authoritarian)
  - Manifestations: preference for strong leadership, obedience, tradition, order
  - Political relevance: correlates with conservative ideology
  - Subtraits: respect for authority, preference for clear rules
  
- **Moral Foundation Weights:**
  - Care/Harm foundation (0-100, how much values compassion)
  - Fairness/Cheating foundation (0-100, how much values equal treatment)
  - Loyalty/Betrayal foundation (0-100, how much values group loyalty)
  - Authority/Subversion foundation (0-100, how much values tradition/respect)
  - Sanctity/Degradation foundation (0-100, how much values sacred/pure things)
  - Liberty/Oppression foundation (0-100, how much values freedom)
  - Political relevance: progressive emphasizes Care/Fairness, conservative emphasizes Loyalty/Authority/Sanctity
  
- **Cognitive Complexity:**
  - Simple (thinks in black/white, either/or)
  - Moderate (appreciates nuance but can be extreme)
  - Complex (sees multiple perspectives, appreciates nuance)
  - Political relevance: affects how process information, openness to changing views

### 3.1.3 Motivated Reasoning
- **Directional Bias:**
  - Strength of directional bias (0-100, how much want particular outcome)
  - Motivated reasoning strength (how hard try to reach desired conclusion)
  - Confirmation bias strength (how much seek confirming evidence)
  - Discounting bias strength (how much dismiss opposing evidence)
  - Political relevance: bias affects evaluation of candidates, policies, facts
  
- **Accuracy Motivation:**
  - Desire to be accurate (0-100 scale)
  - Willingness to change mind based on evidence (0-100 scale)
  - Intellectual humility (acknowledge uncertainty, 0-100 scale)
  - Political relevance: affects persuadability, openness to new information

---

# 4. VOTER KNOWLEDGE & INFORMATION

## 4.1 Political Knowledge

### 4.1.1 Candidate Knowledge
- **Recognition:**
  - Knows candidate exists (yes/no)
  - Recognizes candidate by name (yes/no)
  - Recognizes candidate by face (yes/no)
  - Candidate awareness score (0-100, how well know candidate)
  
- **Position Knowledge:**
  - Knows position on economy (yes/no, accuracy if knows)
  - Knows position on healthcare (yes/no, accuracy)
  - Knows position on immigration (yes/no, accuracy)
  - Knows position on environment (yes/no, accuracy)
  - Knows position on education (yes/no, accuracy)
  - Knows position on crime (yes/no, accuracy)
  - Knows position on foreign policy (yes/no, accuracy)
  - Position knowledge accuracy (0-100, how accurate what knows)
  - Position knowledge completeness (how many positions know about)
  
- **Character Knowledge:**
  - Knows candidate's age (yes/no)
  - Knows candidate's occupation (yes/no)
  - Knows candidate's education (yes/no)
  - Knows candidate's party (yes/no)
  - Knows candidate's experience (yes/no, accuracy)
  - Knows candidate's personal background (yes/no)
  - Character knowledge accuracy (0-100)
  
- **Candidate Trait Perception:**
  - Perceives as honest (0-100 scale)
  - Perceives as intelligent (0-100 scale)
  - Perceives as strong (0-100 scale)
  - Perceives as caring (0-100 scale)
  - Perceives as trustworthy (0-100 scale)
  - Perceives as shares values (0-100 scale)
  - Trait perception accuracy (how accurate)

### 4.1.2 Issue Knowledge
- **General Issue Knowledge:**
  - Knows unemployment rate (yes/no, accuracy if knows)
  - Knows inflation rate (yes/no, accuracy)
  - Knows GDP growth (yes/no, accuracy)
  - Knows status of war/conflict (yes/no, accuracy)
  - Knows healthcare statistics (yes/no, accuracy)
  - General knowledge score (0-100)
  
- **Issue Position Knowledge:**
  - Knows own position on economy (yes/no)
  - Knows own position on healthcare (yes/no)
  - Knows own position on immigration (yes/no)
  - Knows own position on environment (yes/no)
  - Knows own position on crime (yes/no)
  - Position self-knowledge accuracy (how clear on own positions)
  
- **Policy Knowledge:**
  - Understands how policy works (yes/no, depth)
  - Knows policy history (yes/no)
  - Knows policy trade-offs (yes/no)
  - Knows who benefits from policy (yes/no)
  - Knows who pays for policy (yes/no)
  - Policy knowledge depth (1-10 scale)

### 4.1.3 Information Sources & Trust
- **News Consumption Patterns:**
  - Primary news source (TV, newspaper, radio, online, social media, podcasts, other)
  - News outlet types (mainstream, cable, online, partisan, community, international)
  - Specific outlets consumed (Fox News, MSNBC, NY Times, Wall Street Journal, etc.)
  - Time spent on news (hours/week)
  - Frequency of news consumption (daily, several times week, weekly, rarely)
  - News consumption recency (current, recent, outdated)
  - News attention (closely follows, somewhat follows, barely follows)
  
- **Source Trust:**
  - Trust in mainstream media (0-100 scale)
  - Trust in specific outlets (Fox, MSNBC, NY Times, etc., 0-100 each)
  - Trust in social media for news (0-100)
  - Trust in political figures (0-100 by specific politician)
  - Trust in scientists/experts (0-100)
  - Trust in academic institutions (0-100)
  - Trust by subject (trust sources on economy? healthcare? crime?)
  
- **Misinformation Susceptibility:**
  - Misinformation belief (0-100, how much believe false claims)
  - Misinformation exposure (how much false info encounter)
  - Misinformation resistance (how resistant to false info, 0-100)
  - Fact-check receptiveness (0-100, willing to change mind with facts)
  - Conspiracy thinking (0-100, how much believe conspiracy theories)
  - Specific conspiracy beliefs (QAnon, election fraud, vaccines, etc., yes/no)

---

# 5. VOTER PREFERENCES & VALUES

## 5.1 Policy Preferences

### 5.1.1 Issue Positions
- **Economy:**
  - Taxes on wealthy (should increase, stay same, decrease)
  - Progressive taxation (support, neutral, oppose)
  - Corporate regulation (more regulation, current level, less regulation)
  - Minimum wage (should increase, stay same, decrease)
  - Trade policy (support free trade, protectionist, neutral)
  - Healthcare system (single-payer, public option, current system, free market)
  - Social safety net (strengthen, current level, reduce)
  - Government spending (increase, current level, decrease)
  - Inflation concern (very concerned, concerned, neutral, unconcerned)
  - Unemployment concern (very concerned, concerned, neutral, unconcerned)
  
- **Healthcare:**
  - Healthcare coverage (everyone should have, individuals responsible, mixed)
  - Government role (government provide, subsidize, regulate, none)
  - Abortion (should be legal always, most cases, few cases, never)
  - Drug legalization (marijuana, harder drugs, neither, all)
  - Gun rights (strong gun rights, regulated guns, strong gun control)
  
- **Immigration:**
  - Immigration level (should increase, current level, decrease)
  - Path to citizenship (support, neutral, oppose)
  - Border security (increase spending, current level, decrease)
  - Deportations (support deportations, oppose)
  - Refugee admission (increase, current level, decrease)
  
- **Crime & Justice:**
  - Police funding (increase, current level, decrease)
  - Prison reform (punitive focus, rehabilitation focus)
  - Death penalty (support, oppose)
  - Drug criminalization (criminal justice approach, public health approach)
  - Sentencing (harsher, current, lighter)
  
- **Environment:**
  - Climate change concern (very concerned, concerned, neutral, unconcerned)
  - Climate action support (strong support, support, neutral, oppose)
  - Environmental regulation (increase, current level, decrease)
  - Renewable energy (strong support, support, neutral, oppose)
  - Oil/coal (phase out, regulated, embrace)
  
- **Education:**
  - Education spending (increase, current level, decrease)
  - Student debt relief (support, neutral, oppose)
  - Public vs. private (public schools best, charter schools good, private schools best)
  - Curriculum issues (specific contentions like CRT, sex ed, etc.)
  - School choice (support, neutral, oppose)
  
- **Social Issues:**
  - Same-sex marriage (support, neutral, oppose)
  - Transgender rights (support, neutral, oppose)
  - Racial justice (urgent priority, important, neutral, overblown)
  - Police reform (urgent priority, important, neutral, not needed)
  - Religious freedom (prioritize religious freedom, prioritize non-discrimination)
  
- **Foreign Policy:**
  - U.S. military spending (increase, current level, decrease)
  - Interventionism (should intervene, case by case, should not intervene)
  - Russia/China relations (confront, cooperate, neutral)
  - Israel-Palestine (support Israel, support Palestine, neutral)
  - UN support (support, neutral, oppose)
  
- **Other Issues:**
  - Voting access (expand voting access, current level, restrict)
  - Campaign finance reform (strict limits, current level, no limits)
  - Electoral college (abolish, keep, reform)

### 5.1.2 Issue Salience
- **Issue Importance Rankings:**
  - Which issues matter to voter (ranking of 10-20 top issues)
  - Importance weights (how much relative importance)
  - Personal salience (issue affects me personally, 0-100)
  - National salience (issue important to country, 0-100)
  - Emotional engagement (emotional engagement level, 0-100)
  - Issue stability (changes over time, yes/no)
  - Life event triggers (did personal event change salience)

---

# 6. VOTER EMOTIONS & ATTITUDES

## 6.1 Emotional States

### 6.1.1 Current Emotional State
- **Baseline Emotions (current emotional state):**
  - Anger (0-100 scale)
  - Fear/Anxiety (0-100 scale)
  - Sadness (0-100 scale)
  - Disgust (0-100 scale)
  - Hope (0-100 scale)
  - Pride (0-100 scale)
  - Shame (0-100 scale)
  - Guilt (0-100 scale)
  - Happiness (0-100 scale)
  
- **Emotional Targets:**
  - Anger at: candidate A, candidate B, government, economy, specific group, etc.
  - Fear of: candidate winning, election outcome, state of world, change, etc.
  - Hope for: candidate winning, policy change, future improvement, etc.
  - Disgust toward: candidate, policy, group, system, etc.

### 6.1.2 Emotional Volatility
- **Emotional Stability:**
  - Emotional volatility (0-100, how much emotions fluctuate)
  - Emotional responsiveness (0-100, how much respond to events)
  - Emotional recovery (how quickly return to baseline)
  - Emotional extremes (how extreme emotions get)
  - Mood cycling (regular mood cycling, yes/no)

### 6.1.3 Candidate Affect
- **Affective Response to Candidates:**
  - Candidate A affect (0-100 scale, 0=very negative, 100=very positive)
  - Candidate B affect (0-100 scale)
  - Affect warmth (emotional closeness to candidate, 0-100)
  - Affect enthusiasm (emotional energy/excitement, 0-100)
  - Affect anger/resentment toward opposing candidate (0-100)
  - Affect volatility (changes over time, yes/no)

---

# 7. VOTER BEHAVIOR PATTERNS

## 7.1 Electoral Behavior

### 7.1.1 Voting History
- **Past Election Participation:**
  - Registered (yes/no, when registered)
  - Voted in 2008 (yes/no/can't remember)
  - Voted in 2012 (yes/no/can't remember)
  - Voted in 2016 (yes/no/can't remember)
  - Voted in 2020 (yes/no/can't remember)
  - Voting frequency (always votes, sometimes, rarely, never)
  - Voting streak (number of consecutive elections voted)
  
- **Vote Choice History:**
  - 2008 vote choice (Obama, McCain, other, didn't vote)
  - 2012 vote choice (Obama, Romney, other, didn't vote)
  - 2016 vote choice (Trump, Clinton, other, didn't vote)
  - 2020 vote choice (Trump, Biden, other, didn't vote)
  - Party consistency (always votes same party, sometimes switches, frequently switches)
  
- **Voting Method:**
  - Mail voting history (mail voted, yes/no/sometimes)
  - Early voting history (early voted, yes/no/sometimes)
  - Election day voting history (voted on election day, yes/no/always)
  - Voting method preference (preferred voting method)
  - Voting convenience sensitivity (how much voting method affects participation)

### 7.1.2 Campaign Participation
- **Contact History:**
  - Contacted by campaign (yes/no)
  - Contact method (door knock, phone call, text, email, social media)
  - Contact frequency (how many times contacted)
  - Contact response (responded, didn't respond)
  - Contact impact (did contact persuade, reinforce, or no effect)
  
- **Event Participation:**
  - Attended candidate event (yes/no)
  - Event attendance frequency (never, rare, occasional, frequent)
  - Event types attended (rally, town hall, meet-and-greet, fundraiser)
  - Event engagement (engaged, observing, reluctant)
  
- **Volunteering:**
  - Volunteered for campaign (yes/no)
  - Volunteering frequency (hours per week)
  - Volunteer tasks (phone banking, door knocking, event setup, other)
  - Volunteer persistence (volunteered once, several times, ongoing)
  
- **Fundraising:**
  - Donated to campaign (yes/no)
  - Donation amount (total, frequency)
  - Fundraiser attendance (yes/no)
  - Online donation (yes/no)
  - Recurring donation (yes/no)
  
- **Social Media & Sharing:**
  - Shared candidate content (yes/no, frequency)
  - Shared negative content about opponent (yes/no)
  - Posted about campaign (yes/no, frequency)
  - Engaged with candidate social media (liked, commented, shared)

---

# 8. VOTER NETWORKS & INFLUENCE

## 8.1 Social Networks

### 8.1.1 Network Structure
- **Network Composition:**
  - Network size (number of people in network)
  - Tie strength distribution (strong ties, weak ties, ratio)
  - Geographic dispersion (local, dispersed, mixed)
  - Demographic homogeneity (similar to me, diverse, mixed)
  - Political homogeneity (agree politically, disagree, mixed)
  - Family members in network (yes/no, how many)
  - Coworkers in network (yes/no, how many)
  - Friends in network (yes/no, how many)
  
- **Network Density:**
  - How connected network members are (0-100, 0=sparse, 100=fully connected)
  - Clustering coefficient (tendency to form cliques)
  - Small-world property (few degrees of separation)
  - Network bridging (are there bridges between groups)

### 8.1.2 Information & Influence Flow
- **Information Sources from Network:**
  - Percentage of political info from network (0-100%)
  - Info types from network (endorsements, facts, opinions, emotions)
  - Trust in network info (0-100)
  - Info diversity (diverse political views in network, yes/no)
  - Echo chamber effect (mostly hear own views, yes/no)
  
- **Network Influence on Voting:**
  - Network influences vote choice (yes/no, how much 0-100)
  - Network influences turnout (yes/no, how much)
  - Network influences issue positions (yes/no, how much)
  - Conformity to network (yes/no, how much)
  - Network pressure (feels pressure to vote with network, yes/no)
  
- **Information Cascades:**
  - Believes something because network believes it (yes/no, how much)
  - Herding behavior (follows others without independent judgment, yes/no)
  - Adoption lag (how quickly adopts network views)

---

# 9. CANDIDATE AGENT ARCHITECTURE

## 9.1 Candidate Identity

### 9.1.1 Demographic Characteristics
- **Basic Identity:**
  - Name (first, middle, last)
  - Age (continuous years)
  - Date of birth
  - Gender identity
  - Race/ethnicity
  - Religion
  - Marital status
  - Number of children
  - Children's ages
  
- **Background:**
  - Birthplace (state, country if not born in U.S.)
  - Residence address (current residence)
  - Years in district/state (how long lived in area)
  - Education (high school, college, graduate, specific schools)
  - College major
  - Advanced degrees (law degree, MBA, PhD, etc.)
  - Occupational background (previous jobs, industries)
  - Military service (service type, rank, years)
  - Public positions held (mayor, state legislator, governor, etc.)
  - Private sector experience
  - Non-profit experience

### 9.1.2 Character & Traits
- **Personality:**
  - Big Five traits (openness, conscientiousness, extraversion, agreeableness, neuroticism)
  - Intelligence (high, above-average, average, below-average)
  - Charisma (highly charismatic, charismatic, average, low)
  - Authenticity perceived (authentic, somewhat authentic, inauthentic)
  - Likeability (highly likeable, likeable, average, dislikeable)
  
- **Character Strengths:**
  - Honesty (very honest, mostly honest, somewhat honest, dishonest)
  - Integrity (strong integrity, integrity, some issues, questionable)
  - Competence (highly competent, competent, average, incompetent)
  - Leadership (strong leader, leader, average, weak)
  - Vision (clear vision, some vision, unclear, no vision)
  - Courage (politically courageous, cautious)
  - Empathy (high empathy, average, low empathy)
  - Judgment (good judgment, average, poor judgment)
  
- **Character Flaws:**
  - Dishonesty (yes/no, degree)
  - Incompetence (yes/no, degree)
  - Corruption (yes/no, degree)
  - Scandal history (yes/no, what scandals, when)
  - Controversy (yes/no, what controversies)
  - Divisiveness (yes/no, degree)
  - Extreme views (yes/no, which views)

---

# 10. CANDIDATE POSITIONING

## 10.1 Policy Positions

### 10.1.1 Issue Positions (Same as Voter Positions Above)
- Economy, Healthcare, Immigration, Crime, Environment, Education, Social Issues, Foreign Policy, Etc.
- Positions on each issue (more extreme/centrist, clear/ambiguous, etc.)

### 10.1.2 Position Clarity
- **Position Specificity:**
  - How specific are positions (very specific, general, vague, unclear)
  - Policy details provided (yes/no)
  - Implementation plan provided (yes/no)
  - Costings provided (yes/no)
  - Feasibility assessed (realistic, somewhat realistic, unrealistic)
  
- **Position Consistency:**
  - Consistency over time (consistent, some changes, frequent shifts)
  - Consistency across issues (all positions related, scattered, mixed)
  - Internal contradictions (no contradictions, some, many)
  - Candidate flip-flopping (none, some, frequent)

### 10.1.3 Positioning Strategy
- **Base vs. Swing Strategy:**
  - Focus on base (mobilizing base vs. persuading swing voters)
  - Message modulation (same message everywhere vs. tailored to audience)
  - Position modulation (same positions everywhere vs. different by location)
  
- **Ideological Positioning:**
  - Ideological distance from party center (extreme, moderate, centrist)
  - Ideological distance from district/state (aligned, moderate difference, large difference)
  - Ideological positioning stability (stable, shifting, flip-flopping)

---

# 11. CANDIDATE RESOURCES & CAPACITY

## 11.1 Campaign Infrastructure

### 11.1.1 Campaign Organization
- **Staffing:**
  - Campaign manager (name, experience)
  - Deputy campaign manager(s)
  - Communications director
  - Field director
  - Finance director
  - Digital director
  - Volunteer coordinator
  - Data director
  - Total staff size
  - Staff experience (first time, experienced)
  - Staff turnover (stable, changing)
  
- **Organizational Capacity:**
  - Campaign structure (centralized, distributed, disorganized)
  - Decision-making process (hierarchical, collaborative, chaotic)
  - Conflict resolution (effective, some issues, dysfunctional)
  - Internal culture (cohesive, factious)
  
- **Physical Infrastructure:**
  - Campaign headquarters location
  - Field office locations (how many, where)
  - Equipment (computers, phones, databases, etc.)
  - Technology (voter database, CRM, social media tools, etc.)

### 11.1.2 Financial Resources
- **Fundraising:**
  - Total raised (year-to-date, trend)
  - Individual donations (number of donors, average donation)
  - Large donors (number with $2,700+ contributions)
  - Small donors (number with <$200 contributions)
  - Small donor percentage (% of funds from small donors)
  - Bundlers (use of bundlers, how many)
  - Small dollar online (raised online, % total)
  - Personal wealth (candidate's own money, amount loaned/given)
  - Super PAC support (official super PAC, amount raised)
  - Outside spending for (groups spending for candidate, amounts)
  - Fundraising trend (increasing, stable, declining)
  - Fundraising velocity (rate of fundraising)
  - Cash on hand (money available to spend)
  - Burn rate (spending speed)
  
- **Campaign Budget:**
  - Total budget (total planned spending)
  - Advertising budget (TV, digital, radio, print, billboards)
  - Staff budget (payroll)
  - Field budget (field operations)
  - Voter contact budget (phones, mail, etc.)
  - Digital budget (online ads, social media)
  - Overhead (rent, utilities, etc.)
  - Contingency reserve
  - Budget flexibility (fixed vs. flexible)

### 11.1.3 Candidate Effort & Capacity
- **Time Commitment:**
  - Hours per week campaigning
  - Days per week campaigning
  - Campaign start date
  - Campaign intensity (part-time vs. full-time)
  - Current job status (maintain current job, full-time campaign)
  
- **Stamina & Health:**
  - Physical health (excellent, good, fair, poor)
  - Mental health (excellent, good, fair, poor)
  - Energy level (high, average, low)
  - Campaign stress level (handling well, some stress, very stressed)
  - Substance use issues (none, some, significant)

---

# 12. VOTER DECISION-MAKING MODELS

## 12.1 Rational Choice Model

### 12.1.1 Expected Utility Maximization
- **Voter Calculus:**
  - Voter evaluates each candidate on key dimensions
  - Assigns utility to each candidate (0-100 score)
  - Assigns probability each candidate will deliver on promises
  - Calculates expected utility for each candidate
  - Compares expected utilities
  - Votes for candidate with highest expected utility
  
- **Key Dimensions in Evaluation:**
  - Issue positions (does candidate match my positions)
  - Candidate traits (is candidate honest, competent, etc.)
  - Incumbent performance (how well did incumbent perform)
  - Party record (how well has party performed)
  - Personal importance (how much do policies affect me personally)
  - Economic evaluation (has economy improved under current party)

### 12.1.2 Cost-Benefit Analysis
- **Voting Cost:**
  - Time cost (how long takes to vote)
  - Effort cost (how much effort to research, get to polls)
  - Stress cost (stress of political decision)
  - Value of vote (probability vote will determine outcome)
  - Expected benefit from voting (difference between candidates × probability win)
  - Cost-benefit ratio (benefit must exceed cost to vote)

---

# 13. AFFECTIVE/EMOTIONAL DECISION MODELS

## 13.1 Affect-Based Decisions

### 13.1.1 Feelings as Information
- **Emotional Heuristic:**
  - Voter feels positive/negative affect toward candidate
  - Uses feeling as information (gut feeling accurate, yes/no)
  - Asks: "How do I feel about this candidate?"
  - Votes based on feeling (emotional appeal wins)
  - Rational justification (voter finds reasons to support feeling)
  
- **Mood Effects:**
  - Voter in good mood (more optimistic, likes incumbent more, votes yes on measures)
  - Voter in bad mood (more pessimistic, blames incumbent, votes no on measures)
  - Mood congruence (feeling affects what information processes)
  - Mood regulation (does voter try to improve mood, accept mood)

### 13.1.2 Enthusiasm & Mobilization
- **Campaign Enthusiasm:**
  - Enthusiasm for candidate A (0-100)
  - Enthusiasm for voting (0-100)
  - Enthusiasm for campaign participation (0-100)
  - Enthusiasm volatility (changes over time, yes/no)
  
- **Mobilization Effects:**
  - Campaign enthusiasm increases turnout (yes/no)
  - Negative emotion (anger) increases turnout (yes/no)
  - Fear affects turnout (increases, decreases, no effect)
  - Hope affects turnout (increases, decreases, no effect)

---

# 14. HEURISTIC-BASED DECISION MODELS

## 14.1 Mental Shortcuts

### 14.1.1 Common Heuristics
- **Party Heuristic:**
  - Voter uses party as shortcut (assume party candidate good)
  - Party cue sufficient (doesn't need more info)
  - Party voting (straight-ticket voting likely)
  
- **Incumbent Heuristic:**
  - Voter supports incumbent by default (yes-no)
  - Performance evaluation (if good, vote incumbent; if bad, vote challenger)
  - Incumbent bias (preference for status quo)
  
- **Similarity Heuristic:**
  - Voter supports candidate similar to self (yes/no)
  - Demographic similarity (race, gender, religion, etc.)
  - Values similarity
  - Background similarity
  
- **Likeable Heuristic:**
  - Voter supports likeable candidate (personality-driven voting)
  - Likeability more important than policy (yes/no)
  - Trait-based voting (supports based on traits, not policy)
  
- **Appearance Heuristic:**
  - Voter affected by candidate appearance (yes/no, how much)
  - Attractiveness bias (more attractive candidate favored)
  - Trustworthiness from appearance (does appear trustworthy)
  
- **Credential Heuristic:**
  - Voter uses credentials as shortcut (assume Harvard graduate good)
  - Expertise assumption (credential means expertise)
  - Credential importance (credentials matter, or don't care)
  
- **Elite Heuristic:**
  - Voter follows trusted elites (what do trusted leaders support)
  - Elite cue effectiveness (voter changes opinion based on elite)
  - Elite reliance (how much voter relies on elites)

### 14.1.2 Heuristic Efficiency
- **Cognitive Load Effect:**
  - When busy/tired: uses more heuristics (yes/no)
  - When lots of info: uses more heuristics or less (depends on person)
  - Heuristic reliability: are heuristics accurate (yes/no)
  - Heuristic awareness: aware using shortcuts (yes/no)

---

# 15. IDENTITY-BASED DECISION MODELS

## 15.1 Group-Based Voting

### 15.1.1 Social Identity
- **Group Identification:**
  - Identifies as Republican/Democrat (yes/no, strength)
  - Group identity strength (weak, moderate, strong)
  - Group identity salience (always thinking about group membership, sometimes, never)
  - Multiple group identification (identifies with multiple groups)
  
- **In-Group Bias:**
  - Favors in-group members for candidacy (yes/no)
  - Assumes in-group members share values (yes/no)
  - Gives in-group members benefit of doubt (yes/no)
  - Out-group bias (negative bias against other party candidates)
  
- **Group Loyalty:**
  - Votes for in-group candidate even if disagree (yes/no)
  - Party loyalty overrides policy (yes/no)
  - Willing to switch groups (yes/no)
  - Group switching history (has switched parties, when)

### 15.1.2 Coalition Concerns
- **Coalition Membership:**
  - Identifies with political coalition (yes/no, which)
  - Coalition identity strength
  - Coalition alignment (candidate aligned with coalition)
  - Coalition concerns (important to maintain coalition)
  
- **Coalition Candidate:**
  - Is candidate from my coalition (yes/no)
  - Candidate represents coalition interests (yes/no)
  - Willing to support coalition candidate (yes/no)
  - Coalition voting patterns (strong group voting, yes/no)

---

This is Part 1. Ready for Parts 2 and 3?
