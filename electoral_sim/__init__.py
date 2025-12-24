"""
ElectoralSim - Generic Electoral Simulation Toolkit
===================================================

A modular agent-based modeling toolkit for electoral systems, 
voter behavior, and political dynamics using mesa-frames.
"""

__version__ = "0.1.0"

# =============================================================================
# FACADE API (Backward Compatibility)
# =============================================================================

from electoral_sim.core.model import ElectionModel
from electoral_sim.core.config import (
    Config,
    PartyConfig,
    india_config,
    usa_config,
    uk_config,
    germany_config,
    australia_house_config,
    australia_senate_config,
    south_africa_config,
    PRESETS,
)

# Electoral Systems
from electoral_sim.systems.allocation import (
    dhondt_allocation,
    sainte_lague_allocation,
    hare_quota_allocation,
    droop_quota_allocation,
    allocate_seats,
)
from electoral_sim.systems.alternative import (
    irv_election,
    stv_election,
    approval_voting,
    condorcet_winner,
    generate_rankings,
)

# Metrics
from electoral_sim.metrics.indices import (
    gallagher_index,
    effective_number_of_parties,
    efficiency_gap,
)

# Behavior & Dynamics
from electoral_sim.behavior.voter_behavior import (
    BehaviorEngine,
    ProximityModel,
    ValenceModel,
    RetrospectiveModel,
    StrategicVotingModel,
    SociotropicPocketbookModel,
    WastedVoteModel,
)
from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

# Engine & Logic
from electoral_sim.engine.coalition import (
    minimum_winning_coalitions,
    minimum_connected_winning,
    coalition_strain,
    form_government,
    junior_partner_penalty,
    allocate_portfolios_laver_shepsle,
)
from electoral_sim.engine.government import (
    collapse_probability,
    simulate_government_survival,
    hazard_rate,
    cox_proportional_hazard,
    GovernmentSimulator,
)

# Presets
from electoral_sim.presets.india.election import (
    simulate_india_election,
    IndiaElectionResult,
    INDIA_STATES,
    INDIA_PARTIES,
)
from electoral_sim.presets.eu.election import (
    simulate_eu_election,
    EUElectionResult,
    EU_MEMBER_STATES,
    EU_POLITICAL_GROUPS,
)

# Visualization (optional - requires matplotlib)
try:
    from electoral_sim.visualization.charts import (
        plot_seat_distribution,
        plot_vote_shares,
        plot_seats_vs_votes,
        plot_election_summary,
    )
    _VIZ_AVAILABLE = True
except ImportError:
    _VIZ_AVAILABLE = False

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
]
