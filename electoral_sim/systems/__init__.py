"""Electoral systems: seat allocation methods and alternative voting"""

from electoral_sim.systems.allocation import (
    ALLOCATION_METHODS,
    allocate_seats,
    dhondt_allocation,
    droop_quota_allocation,
    fptp_allocation,
    hare_quota_allocation,
    sainte_lague_allocation,
)
from electoral_sim.systems.alternative import (
    approval_voting,
    condorcet_winner,
    generate_rankings,
    irv_election,
    stv_election,
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
