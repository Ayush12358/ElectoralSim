"""Electoral systems: seat allocation methods"""

from electoral_sim.systems.allocation import (
    dhondt_allocation,
    sainte_lague_allocation,
    hare_quota_allocation,
    droop_quota_allocation,
    fptp_allocation,
    allocate_seats,
    ALLOCATION_METHODS,
)

__all__ = [
    "dhondt_allocation",
    "sainte_lague_allocation", 
    "hare_quota_allocation",
    "droop_quota_allocation",
    "fptp_allocation",
    "allocate_seats",
    "ALLOCATION_METHODS",
]
