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

"""Electoral Simulation Presets - Country-specific configurations."""

# India
# EU Parliament
from electoral_sim.presets.eu.election import (
    EU_MEMBER_STATES,
    EU_POLITICAL_GROUPS,
    EUElectionResult,
    simulate_eu_election,
)

# Germany
from electoral_sim.presets.germany.config import GERMANY_PARTIES, germany_config
from electoral_sim.presets.india.data import INDIA_PARTIES, INDIA_STATES
from electoral_sim.presets.india.election import IndiaElectionResult, simulate_india_election

# UK
from electoral_sim.presets.uk.config import UK_PARTIES, uk_config

# USA
from electoral_sim.presets.usa.config import USA_PARTIES, usa_config

__all__ = [
    # India
    "simulate_india_election",
    "IndiaElectionResult",
    "INDIA_STATES",
    "INDIA_PARTIES",
    # EU
    "simulate_eu_election",
    "EUElectionResult",
    "EU_MEMBER_STATES",
    "EU_POLITICAL_GROUPS",
    # USA
    "usa_config",
    "USA_PARTIES",
    # UK
    "uk_config",
    "UK_PARTIES",
    # Germany
    "germany_config",
    "GERMANY_PARTIES",
]
