# API Reference

Complete API documentation for ElectoralSim.

## Core

| Class/Function | Description |
|----------------|-------------|
| [ElectionModel](election_model.md) | Main simulation model |
| [Config](election_model.md#config) | Configuration dataclass |
| [PartyConfig](election_model.md#partyconfig) | Party configuration |

## Agents

| Class/Function | Description |
|----------------|-------------|
| [VoterAgents](agents.md#voteragents) | Vectorized voter agent storage |
| [PartyAgents](agents.md#partyagents) | Vectorized party agent storage |
| [adaptive_strategy_step](agents.md#adaptive_strategy_step) | Dynamic party position updates |

## Behavior Models

| Class | Description |
|-------|-------------|
| [BehaviorEngine](behavior_models.md#behaviorengine) | Combines multiple behavior models |
| [ProximityModel](behavior_models.md#proximitymodel) | Spatial/ideological voting |
| [ValenceModel](behavior_models.md#valencemodel) | Non-policy candidate appeal |
| [RetrospectiveModel](behavior_models.md#retrospectivemodel) | Economic/incumbent voting |
| [StrategicVotingModel](behavior_models.md#strategicvotingmodel) | Duverger's Law effects |
| [WastedVoteModel](behavior_models.md#wastedvotemodel) | Tactical voting |
| [SociotropicPocketbookModel](behavior_models.md#sociotropicpocketbookmodel) | Economic perception |

## Campaign Models

| Class | Description |
|-------|-------------|
| [CampaignFinance](campaign.md#campaignfinance) | Finance-to-valence conversion |
| [MediaEnvironment](campaign.md#mediaenvironment) | Media exposure & sentiment |
| [VoterRegistration](campaign.md#voterregistration) | Eligibility & registration |
| [CampaignTargeting](campaign.md#campaigntargeting) | Constituency resource allocation |
| [TurnoutMobilization](campaign.md#turnoutmobilization) | Canvassing & GOTV effects |
| [PollingAccess](campaign.md#pollingaccess) | Distance & wait-time barriers |

## Constituency & Counting

| Class/Function | Description |
|----------------|-------------|
| [ConstituencyMetadata](constituency.md#constituencymetadata) | District metadata dataclass |
| [ConstituencyManager](constituency.md#constituencymanager) | Constituency collection management |
| [is_candidate_eligible](constituency.md#is_candidate_eligible) | Reserved-seat eligibility check |
| [count_fptp](counting.md#count_fptp) | FPTP vote counting |
| [count_pr](counting.md#count_pr) | PR vote counting with allocation |

## Electoral Systems

| Function | Description |
|----------|-------------|
| [dhondt_allocation](electoral_systems.md#dhondt) | D'Hondt seat allocation |
| [sainte_lague_allocation](electoral_systems.md#sainte-lague) | Sainte-Laguë allocation |
| [hare_quota_allocation](electoral_systems.md#hare-quota) | Hare quota (LR) |
| [droop_quota_allocation](electoral_systems.md#droop-quota) | Droop quota |
| [irv_election](electoral_systems.md#irv) | Instant Runoff Voting |
| [stv_election](electoral_systems.md#stv) | Single Transferable Vote |
| [approval_voting](electoral_systems.md#approval-voting) | Approval voting |
| [condorcet_winner](electoral_systems.md#condorcet) | Condorcet winner detection |
| [borda_count](electoral_systems.md#borda-count) | Borda count rank voting |
| [score_voting](electoral_systems.md#score-range-voting) | Score (range) voting |
| [pav_committee](electoral_systems.md#pav) | Proportional Approval Voting |
| [generate_rankings](electoral_systems.md#generate-rankings) | Utility-to-ranking conversion |
| [allocate_seats](electoral_systems.md#allocate-seats) | Universal seat allocation |

## Primary Elections

| Function | Description |
|----------|-------------|
| [closed_primary](primary.md#closed_primary) | Party-members-only primary |
| [open_primary](primary.md#open_primary) | Open primary election |
| [candidate_selection](primary.md#candidate_selection) | Candidate field generation |

## Events & Timeline

| Class/Function | Description |
|----------------|-------------|
| [Event](events.md#event) | Dynamic event dataclass |
| [EventManager](events.md#eventmanager) | Event generation & tracking |
| [ElectionTimeline](events.md#electiontimeline) | Campaign/election scheduling |
| [PollGenerator](events.md#pollgenerator) | Synthetic poll generation |

## Metrics

| Function | Description |
|----------|-------------|
| [gallagher_index](metrics.md#gallagher-index) | Disproportionality measure |
| [effective_number_of_parties](metrics.md#enp) | Laakso-Taagepera ENP |
| [efficiency_gap](metrics.md#efficiency-gap) | Gerrymandering metric |
| [loosemore_hanby_index](metrics.md#loosemore-hanby) | Disproportionality measure |
| [herfindahl_hirschman_index](metrics.md#hhi) | Market concentration index |
| [partisan_bias](metrics.md#partisan-bias) | Tilt toward one party |
| [mean_median_gap](metrics.md#mean-median-gap) | Vote distribution skew |
| [partisan_gini](metrics.md#partisan-gini) | Inequality measure |
| [polsby_popper](metrics.md#polsby-popper) | District compactness |
| [convex_hull_compactness](metrics.md#convex-hull) | Geometric compactness |

## Coalition & Government

| Function/Class | Description |
|----------------|-------------|
| [form_government](coalition.md#form_government) | Coalition formation |
| [minimum_winning_coalitions](coalition.md#mwc) | Find MWCs |
| [minimum_connected_winning](coalition.md#mcw) | Find MCWs |
| [coalition_strain](coalition.md#strain) | Calculate strain |
| [GovernmentSimulator](coalition.md#governmentsimulator) | Stability simulation |

## Analysis

| Function | Description |
|----------|-------------|
| [one_at_a_time](sensitivity.md#one_at_a_time) | OAT parameter sensitivity |
| [grid_sensitivity](sensitivity.md#grid_sensitivity) | Grid-based sensitivity |
| [swing_analysis](sensitivity.md#swing_analysis) | Swing parameter analysis |
| [mse_loss](calibration.md#mse_loss) | Calibration loss function |
| [grid_search_calibration](calibration.md#grid_search_calibration) | Grid-search calibration |
| [generate_calibration_report](calibration.md#generate_calibration_report) | Calibration report |
| [run_duverger_experiment](duverger.md#run_duverger_experiment) | FPTP vs PR convergence |
| [calculate_vse](vse.md#calculate_vse) | Voting System Efficiency |
| [calculate_welfare](vse.md#calculate_welfare) | Social welfare |

## Redistricting

| Class/Function | Description |
|----------------|-------------|
| [PrecinctGraph](redistricting.md#precinctgraph) | Precinct adjacency graph |
| [recom_proposal](redistricting.md#recom_proposal) | ReCom spanning-tree recombination |
| [ensemble_analysis](redistricting.md#ensemble_analysis) | Ensemble comparison |

## GPU Acceleration

| Function | Description |
|----------|-------------|
| [is_gpu_available](gpu.md#is_gpu_available) | GPU availability check |
| [compute_utilities_gpu](gpu.md#compute_utilities_gpu) | GPU utility computation |
| [mnl_sample_gpu](gpu.md#mnl_sample_gpu) | GPU MNL sampling |

## Visualization

| Function | Description |
|----------|-------------|
| [plot_seat_distribution](visualization.md#plot_seat_distribution) | Seat bar chart |
| [plot_vote_shares](visualization.md#plot_vote_shares) | Vote share pie chart |
| [plot_seats_vs_votes](visualization.md#plot_seats_vs_votes) | Seats vs votes comparison |
| [plot_election_summary](visualization.md#plot_election_summary) | 2-panel summary |
| [plot_ideological_space](visualization.md#plot_ideological_space) | Ideological space scatter |

## Opinion Dynamics

| Class | Description |
|-------|-------------|
| [OpinionDynamics](opinion_dynamics.md) | Social network opinion evolution |
