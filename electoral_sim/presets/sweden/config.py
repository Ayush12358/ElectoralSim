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

"""Sweden Election Preset - Riksdag.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. PR with Sainte-Lague allocation and leveling seats in
29 multi-member constituencies matches the real Swedish electoral system.

Sources: Swedish Election Authority, Swedish Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def sweden_config(
    n_voters: int = 349_000,
    n_constituencies: int = 29,
    **kwargs,
) -> Config:
    """
    Preset configuration for Sweden (Riksdag).

    349 seats from 29 constituencies, Sainte-Lague PR with 4% threshold.

    Parameter rationale: Seven major Swedish parties. Social Democrats
    (center-left, dominant), Moderate (center-right), Sweden Democrats
    (far-right/nationalist), Centre (centrist/agrarian), Left (left/socialist),
    Liberals (center-right/liberal), Green (left/environmental). Valence
    values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Social Democrats", -0.3, -0.1, 55),
        PartyConfig("Moderate", 0.4, 0.1, 40),
        PartyConfig("Sweden Democrats", 0.7, 0.5, 35),
        PartyConfig("Centre", 0.1, 0.2, 30),
        PartyConfig("Left", -0.6, -0.3, 30),
        PartyConfig("Liberals", 0.2, -0.1, 25),
        PartyConfig("Green", -0.7, -0.4, 25),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="sainte_lague",
        threshold=0.04,
        **kwargs,
    )


SWEDEN_PARTIES = {
    "Social Democrats": {"position_x": -0.3, "position_y": -0.1, "valence": 55},
    "Moderate": {"position_x": 0.4, "position_y": 0.1, "valence": 40},
    "Sweden Democrats": {"position_x": 0.7, "position_y": 0.5, "valence": 35},
    "Centre": {"position_x": 0.1, "position_y": 0.2, "valence": 30},
    "Left": {"position_x": -0.6, "position_y": -0.3, "valence": 30},
    "Liberals": {"position_x": 0.2, "position_y": -0.1, "valence": 25},
    "Green": {"position_x": -0.7, "position_y": -0.4, "valence": 25},
}
