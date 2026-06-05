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

"""Electoral metrics and indices"""

from electoral_sim.metrics.indices import (
    effective_number_of_parties,
    efficiency_gap,
    gallagher_index,
    herfindahl_hirschman_index,
    loosemore_hanby_index,
    seat_share,
    seats_votes_ratio,
    turnout_rate,
    vote_share,
)

__all__ = [
    "gallagher_index",
    "loosemore_hanby_index",
    "effective_number_of_parties",
    "herfindahl_hirschman_index",
    "efficiency_gap",
    "turnout_rate",
    "vote_share",
    "seat_share",
    "seats_votes_ratio",
]
