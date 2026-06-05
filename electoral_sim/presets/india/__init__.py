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

"""India Lok Sabha election preset."""

from electoral_sim.presets.india.config import india_config
from electoral_sim.presets.india.data import (
    INDIA_ELECTION_PHASES,
    INDIA_PARTIES,
    INDIA_STATES,
    STATE_CONFIGS,
    StateConfig,
)
from electoral_sim.presets.india.election import (
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
    "STATE_CONFIGS",
    "StateConfig",
    "get_phase_states",
    "india_config",
]
