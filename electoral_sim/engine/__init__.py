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

"""
Electoral Engine Module

Contains core logic for coalition formation, government stability, and acceleration.
"""

from electoral_sim.engine.coalition import (
    allocate_portfolios_laver_shepsle,
    coalition_strain,
    form_coalition_with_utility,
    form_government,
    junior_partner_penalty,
    minimum_connected_winning,
    minimum_winning_coalitions,
)
from electoral_sim.engine.government import (
    GovernmentSimulator,
    collapse_probability,
    cox_proportional_hazard,
    hazard_rate,
    simulate_government_survival,
)
from electoral_sim.engine.numba_accel import (
    NUMBA_AVAILABLE,
    compute_utilities_numba,
    fptp_count_fast,
    vote_mnl_fast,
)

__all__ = [
    # Coalition
    "minimum_winning_coalitions",
    "minimum_connected_winning",
    "coalition_strain",
    "form_government",
    "junior_partner_penalty",
    "allocate_portfolios_laver_shepsle",
    "form_coalition_with_utility",
    # Government
    "collapse_probability",
    "simulate_government_survival",
    "hazard_rate",
    "cox_proportional_hazard",
    "GovernmentSimulator",
    # Acceleration
    "vote_mnl_fast",
    "fptp_count_fast",
    "compute_utilities_numba",
    "NUMBA_AVAILABLE",
]
