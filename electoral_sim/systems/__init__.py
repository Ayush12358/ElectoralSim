"""Electoral systems: seat allocation methods and alternative voting"""

from electoral_sim.systems.allocation import (
    ALLOCATION_METHODS,
    allocate_seats,
    closed_list_allocation,
    dhondt_allocation,
    droop_quota_allocation,
    fptp_allocation,
    hare_quota_allocation,
    mmp_allocation,
    open_list_allocation,
    sainte_lague_allocation,
)
from electoral_sim.systems.alternative import (
    approval_voting,
    borda_count,
    condorcet_winner,
    generate_rankings,
    irv_election,
    pav_committee,
    score_voting,
    stv_election,
)
from electoral_sim.systems.primary import (
    candidate_selection,
    closed_primary,
    open_primary,
)

__all__ = [
    # PR allocation
    "dhondt_allocation",
    "sainte_lague_allocation",
    "hare_quota_allocation",
    "droop_quota_allocation",
    "closed_list_allocation",
    "open_list_allocation",
    "fptp_allocation",
    "allocate_seats",
    "ALLOCATION_METHODS",
    # Alternative systems
    "irv_election",
    "stv_election",
    "approval_voting",
    "borda_count",
    "condorcet_winner",
    "generate_rankings",
    "pav_committee",
    "score_voting",
    # Primary elections
    "closed_primary",
    "open_primary",
    "candidate_selection",
]
