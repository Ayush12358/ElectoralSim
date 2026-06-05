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

"""Core module - ElectionModel and configuration."""

from electoral_sim.core.config import PRESETS, Config, PartyConfig
from electoral_sim.core.counting import count_fptp, count_pr
from electoral_sim.core.model import ElectionModel
from electoral_sim.core.voter_generation import generate_party_frame, generate_voter_frame

__all__ = [
    "ElectionModel",
    "Config",
    "PartyConfig",
    "PRESETS",
    "generate_voter_frame",
    "generate_party_frame",
    "count_fptp",
    "count_pr",
]
