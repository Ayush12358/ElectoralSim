"""Electoral Simulation Presets - Country-specific configurations."""

# India
from electoral_sim.presets.india.election import (
    simulate_india_election,
    IndiaElectionResult,
    INDIA_STATES,
    INDIA_PARTIES,
)

# EU Parliament
from electoral_sim.presets.eu.election import (
    simulate_eu_election,
    EUElectionResult,
    EU_MEMBER_STATES,
    EU_POLITICAL_GROUPS,
)

# USA
from electoral_sim.presets.usa.config import usa_config, USA_PARTIES

# UK
from electoral_sim.presets.uk.config import uk_config, UK_PARTIES

# Germany
from electoral_sim.presets.germany.config import germany_config, GERMANY_PARTIES

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
