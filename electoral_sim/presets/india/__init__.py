"""India Lok Sabha election preset."""

from electoral_sim.presets.india.election import (
    INDIA_ELECTION_PHASES,
    INDIA_PARTIES,
    INDIA_STATES,
    IndiaElectionResult,
    get_phase_states,
    simulate_india_election,
)

__all__ = [
    "simulate_india_election",
    "IndiaElectionResult",
    "INDIA_STATES",
    "INDIA_PARTIES",
    "INDIA_ELECTION_PHASES",
    "get_phase_states",
]
