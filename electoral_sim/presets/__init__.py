"""Electoral Simulation Presets - Country-specific configurations."""

# India
# EU Parliament
from electoral_sim.presets.eu.election import (
    EU_MEMBER_STATES,
    EU_POLITICAL_GROUPS,
    EUElectionResult,
    simulate_eu_election,
)

# Germany
from electoral_sim.presets.germany.config import GERMANY_PARTIES, germany_config
from electoral_sim.presets.india.election import (
    INDIA_PARTIES,
    INDIA_STATES,
    IndiaElectionResult,
    simulate_india_election,
)

# UK
from electoral_sim.presets.uk.config import UK_PARTIES, uk_config

# USA
from electoral_sim.presets.usa.config import USA_PARTIES, usa_config

__all__ = [
    # India
    "simulate_india_election",
    "IndiaElectionResult",
    "INDIA_STATES",
    "INDIA_PARTIES",
    # EU
    "simulate_eu_election",
    "EUElectionResult",
    "EU_MEMBER_STATES",
    "EU_POLITICAL_GROUPS",
    # USA
    "usa_config",
    "USA_PARTIES",
    # UK
    "uk_config",
    "UK_PARTIES",
    # Germany
    "germany_config",
    "GERMANY_PARTIES",
]

# Preset mapping for ElectionModel.from_preset()
PRESETS = {
    "india": None,  # Use simulate_india_election() directly
    "usa": usa_config,
    "uk": uk_config,
    "germany": germany_config,
}
