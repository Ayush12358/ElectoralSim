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

from electoral_sim.presets.south_africa.config import (
    SOUTH_AFRICA_PARTIES,
    south_africa_config,
)

__all__ = [
    "south_africa_config",
    "SOUTH_AFRICA_PARTIES",
]

# Deprecated alias for backward compatibility
SOUTH_AF_RICA_PARTIES = SOUTH_AFRICA_PARTIES
