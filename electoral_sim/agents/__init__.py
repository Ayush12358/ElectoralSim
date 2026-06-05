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

"""Agent classes for electoral simulation"""

from electoral_sim.agents.party import INDIA_PARTIES, UK_PARTIES, US_PARTIES, PartyAgents
from electoral_sim.agents.voter import VoterAgents

__all__ = ["VoterAgents", "PartyAgents", "INDIA_PARTIES", "US_PARTIES", "UK_PARTIES"]
