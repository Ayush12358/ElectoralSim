"""
ElectoralSim - India Electoral Simulation
==========================================

Agent-based electoral simulation using mesa-frames.

Quick Start
-----------
    # Simple usage
    from electoral_sim import ElectionModel
    
    model = ElectionModel(n_voters=100_000)
    results = model.run_election()
    print(f"Turnout: {results['turnout']:.1%}")
    print(f"Gallagher Index: {results['gallagher']:.2f}")

    # Using preset
    model = ElectionModel.from_preset("india", n_voters=500_000)
    
    # Using Config
    from electoral_sim import Config
    
    config = Config(
        n_voters=100_000,
        electoral_system="PR",
        threshold=0.05,
    )
    model = ElectionModel.from_config(config)

    # Chainable API
    results = (
        ElectionModel(n_voters=100_000)
        .with_system("PR")
        .with_allocation("sainte_lague")
        .run_election()
    )

Available Presets
-----------------
    - india: 543 constituencies, BJP/INC/AAP/etc
    - usa: 435 districts, Democratic/Republican
    - uk: 650 constituencies, Conservative/Labour/LibDem/etc
    - germany: 299 districts, CDU/SPD/Grüne/etc with 5% threshold

Modules
-------
    - electoral_sim.model: ElectionModel, VoterAgents, PartyAgents
    - electoral_sim.config: Config, PartyConfig, presets
    - electoral_sim.systems: Seat allocation methods
    - electoral_sim.metrics: Gallagher, ENP, Efficiency Gap
    - electoral_sim.coalition: MCW, MWC, strain
    - electoral_sim.government: Collapse models, stability
"""

__version__ = "0.1.0"

# =============================================================================
# CORE API
# =============================================================================

from electoral_sim.model import ElectionModel
from electoral_sim.config import (
    Config,
    PartyConfig,
    india_config,
    usa_config,
    uk_config,
    germany_config,
    PRESETS,
)

# =============================================================================
# ELECTORAL SYSTEMS
# =============================================================================

from electoral_sim.systems.allocation import (
    dhondt_allocation,
    sainte_lague_allocation,
    hare_quota_allocation,
    droop_quota_allocation,
    allocate_seats,
)

# =============================================================================
# METRICS
# =============================================================================

from electoral_sim.metrics.indices import (
    gallagher_index,
    effective_number_of_parties,
    efficiency_gap,
)

# =============================================================================
# COALITION & GOVERNMENT
# =============================================================================

from electoral_sim.coalition import (
    minimum_winning_coalitions,
    minimum_connected_winning,
    coalition_strain,
    form_government,
)

from electoral_sim.government import (
    collapse_probability,
    simulate_government_survival,
    GovernmentSimulator,
)

# =============================================================================
# PUBLIC API
# =============================================================================

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
    "PRESETS",
    # Allocation
    "allocate_seats",
    "dhondt_allocation",
    "sainte_lague_allocation",
    "hare_quota_allocation",
    "droop_quota_allocation",
    # Metrics
    "gallagher_index",
    "effective_number_of_parties",
    "efficiency_gap",
    # Coalition
    "minimum_winning_coalitions",
    "minimum_connected_winning",
    "coalition_strain",
    "form_government",
    # Government
    "collapse_probability",
    "simulate_government_survival",
    "GovernmentSimulator",
]
