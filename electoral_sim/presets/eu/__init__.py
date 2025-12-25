"""EU Parliament Election Preset."""

from electoral_sim.presets.eu.election import (
    EU_MEMBER_STATES,
    EU_POLITICAL_GROUPS,
    EUElectionResult,
    simulate_eu_election,
)

__all__ = [
    "simulate_eu_election",
    "EUElectionResult",
    "EU_MEMBER_STATES",
    "EU_POLITICAL_GROUPS",
]
