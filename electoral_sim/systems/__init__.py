"""Electoral systems: seat allocation methods and alternative voting"""

from electoral_sim.systems.allocation import (
    dhondt_allocation,
    sainte_lague_allocation,
    hare_quota_allocation,
    droop_quota_allocation,
    fptp_allocation,
    allocate_seats,
    ALLOCATION_METHODS,
)

from electoral_sim.systems.alternative import (
    irv_election,
    stv_election,
    approval_voting,
    condorcet_winner,
    generate_rankings,
)

__all__ = [
    # PR allocation
    "dhondt_allocation",
    "sainte_lague_allocation",
    "hare_quota_allocation",
    "droop_quota_allocation",
    "fptp_allocation",
    "allocate_seats",
    "ALLOCATION_METHODS",
    # Alternative systems
    "irv_election",
    "stv_election",
    "approval_voting",
    "condorcet_winner",
    "generate_rankings",
]
