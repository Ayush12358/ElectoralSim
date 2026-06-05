# Copyright 2025-2026 Ayush Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    pav_committee,
    score_voting,
)
from electoral_sim.systems._ranked import (
    irv_election,
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
