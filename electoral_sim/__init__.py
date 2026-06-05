# Copyright 2025 Ayush Maurya
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
ElectoralSim - Generic Electoral Simulation Toolkit
===================================================

A modular agent-based modeling toolkit for electoral systems,
voter behavior, and political dynamics using Mesa + Polars.
"""

__version__ = "0.1.1"

# =============================================================================
# FACADE API (Backward Compatibility)
# =============================================================================

# =============================================================================
# STABLE API — core engine, always safe to import
# =============================================================================

from electoral_sim.core.model import ElectionModel
from electoral_sim.core.config import (
    PRESETS,
    CandidateConfig,
    Config,
    PartyConfig,
    australia_house_config,
    australia_senate_config,
    brazil_config,
    france_config,
    germany_config,
    india_config,
    japan_config,
    south_africa_config,
    uk_config,
    usa_config,
)

# Behavior
from electoral_sim.behavior.voter_behavior import (
    BehaviorEngine,
    ProximityModel,
    RetrospectiveModel,
    SociotropicPocketbookModel,
    StrategicVotingModel,
    ValenceModel,
    WastedVoteModel,
)

# Electoral Systems
from electoral_sim.systems.allocation import (
    allocate_seats,
    dhondt_allocation,
    droop_quota_allocation,
    hare_quota_allocation,
    sainte_lague_allocation,
)
from electoral_sim.systems.alternative import (
    approval_voting,
    borda_count,
    condorcet_winner,
    generate_rankings,
    pav_committee,
    score_voting,
)
from electoral_sim.systems._ranked import (
    irv_election,
    stv_election,
)

# Metrics
from electoral_sim.metrics.indices import (
    convex_hull_compactness,
    effective_number_of_parties,
    efficiency_gap,
    gallagher_index,
    mean_median_gap,
    partisan_bias,
    partisan_gini,
    polsby_popper,
    responsiveness,
    swing_ratio,
)

# Analysis
from electoral_sim.analysis import BatchRunner, ParameterSweep

# =============================================================================
# BETA API — tested but may have known caveats
# =============================================================================

# Coalition & Government
from electoral_sim.engine.coalition import (
    allocate_portfolios_laver_shepsle,
    coalition_strain,
    form_government,
    junior_partner_penalty,
    minimum_connected_winning,
    minimum_winning_coalitions,
)
from electoral_sim.engine.government import (
    GovernmentSimulator,
    collapse_probability,
    cox_proportional_hazard,
    hazard_rate,
    simulate_government_survival,
)

# Opinion Dynamics
from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

# Agents (BETA — internal API, useful for advanced customization)
from electoral_sim.agents.voter import VoterAgents
from electoral_sim.agents.party import PartyAgents

# Events (BETA — event management for scandal/shock simulation)
from electoral_sim.events.event_manager import EventManager

# Country-Specific Presets
from electoral_sim.presets.india.election import (
    INDIA_PARTIES,
    INDIA_STATES,
    IndiaElectionResult,
    simulate_india_election,
)
from electoral_sim.presets.eu.election import (
    EU_MEMBER_STATES,
    EU_POLITICAL_GROUPS,
    EUElectionResult,
    simulate_eu_election,
)

# Visualization (optional - requires matplotlib)
try:
    from electoral_sim.visualization import (
        plot_election_summary,
        plot_ideological_space,
        plot_seat_distribution,
        plot_seats_vs_votes,
        plot_vote_shares,
    )

    _VIZ_AVAILABLE = True
    _VIZ_IMPORT_ERROR = None
except ImportError as e:
    _VIZ_AVAILABLE = False
    _VIZ_IMPORT_ERROR = str(e)

__all__ = [
    # Core
    "ElectionModel",
    "Config",
    "PartyConfig",
    # Presets
    "india_config",
    "usa_config",
    "uk_config",
    "germany_config",
    "australia_house_config",
    "australia_senate_config",
    "south_africa_config",
    "brazil_config",
    "france_config",
    "japan_config",
    "PRESETS",
    # Allocation
    "allocate_seats",
    "dhondt_allocation",
    "sainte_lague_allocation",
    "hare_quota_allocation",
    "droop_quota_allocation",
    # Alternative Systems
    "irv_election",
    "stv_election",
    "approval_voting",
    "condorcet_winner",
    "generate_rankings",
    # Metrics
    "gallagher_index",
    "effective_number_of_parties",
    "efficiency_gap",
    # Behavior & Dynamics
    "BehaviorEngine",
    "ProximityModel",
    "ValenceModel",
    "RetrospectiveModel",
    "StrategicVotingModel",
    "SociotropicPocketbookModel",
    "WastedVoteModel",
    "OpinionDynamics",
    # Engine
    "minimum_winning_coalitions",
    "minimum_connected_winning",
    "coalition_strain",
    "form_government",
    "junior_partner_penalty",
    "allocate_portfolios_laver_shepsle",
    "collapse_probability",
    "simulate_government_survival",
    "hazard_rate",
    "cox_proportional_hazard",
    "GovernmentSimulator",
    # India Election
    "simulate_india_election",
    "IndiaElectionResult",
    "INDIA_STATES",
    "INDIA_PARTIES",
    # EU Parliament
    "simulate_eu_election",
    "EUElectionResult",
    "EU_MEMBER_STATES",
    "EU_POLITICAL_GROUPS",
    # Visualization
    "plot_seat_distribution",
    "plot_vote_shares",
    "plot_seats_vs_votes",
    "plot_election_summary",
    # Analysis
    "BatchRunner",
    "ParameterSweep",
]
