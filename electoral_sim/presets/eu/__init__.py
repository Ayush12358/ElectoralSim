"""EU Parliament Election Preset."""

from electoral_sim.presets.eu.config import eu_config, EU_PARTIES
from electoral_sim.presets.eu.election import (
    EU_MEMBER_STATES,
    EU_POLITICAL_GROUPS,
    EUElectionResult,
    simulate_eu_election,
)

__all__ = [
    "eu_config",
    "EU_PARTIES",
    "simulate_eu_election",
    "EUElectionResult",
    "EU_MEMBER_STATES",
    "EU_POLITICAL_GROUPS",
]
