# API Reference

Complete API documentation for ElectoralSim.

## Core

| Class/Function | Description |
|----------------|-------------|
| [ElectionModel](election_model.md) | Main simulation model |
| [Config](election_model.md#config) | Configuration dataclass |
| [PartyConfig](election_model.md#partyconfig) | Party configuration |

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

## Metrics

| Function | Description |
|----------|-------------|
| [gallagher_index](metrics.md#gallagher-index) | Disproportionality measure |
| [effective_number_of_parties](metrics.md#enp) | Laakso-Taagepera ENP |
| [efficiency_gap](metrics.md#efficiency-gap) | Gerrymandering metric |

## Coalition & Government

| Function/Class | Description |
|----------------|-------------|
| [form_government](coalition.md#form_government) | Coalition formation |
| [minimum_winning_coalitions](coalition.md#mwc) | Find MWCs |
| [minimum_connected_winning](coalition.md#mcw) | Find MCWs |
| [coalition_strain](coalition.md#strain) | Calculate strain |
| [GovernmentSimulator](coalition.md#governmentsimulator) | Stability simulation |

## Opinion Dynamics

| Class | Description |
|-------|-------------|
| [OpinionDynamics](opinion_dynamics.md) | Social network opinion evolution |
