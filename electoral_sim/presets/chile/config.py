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

"""Chile Election Preset - Chamber of Deputies.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. D'Hondt PR in multi-member districts matches the real
Chilean electoral system (post-2015 reform).

Sources: Servicio Electoral de Chile (Servel), Chilean Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def chile_config(
    n_voters: int = 155_000,
    n_constituencies: int = 28,
    **kwargs,
) -> Config:
    """
    Preset configuration for Chile (Chamber of Deputies).

    155 seats from 28 multi-member districts, D'Hondt PR.

    Parameter rationale: Six major Chilean parties. Republican (far-right/
    conservative), Chile Vamos (center-right coalition), Christian Democrats
    (center), Socialist (center-left), Broad Front (left), Communist (far-left).
    Valence values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Republican", 0.7, 0.4, 45),
        PartyConfig("Chile Vamos", 0.4, 0.2, 40),
        PartyConfig("Christian Democrats", 0.1, 0.0, 35),
        PartyConfig("Socialist", -0.3, -0.2, 35),
        PartyConfig("Broad Front", -0.5, -0.3, 40),
        PartyConfig("Communist", -0.7, -0.4, 30),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="dhondt",
        **kwargs,
    )


CHILE_PARTIES = {
    "Republican": {"position_x": 0.7, "position_y": 0.4, "valence": 45},
    "Chile Vamos": {"position_x": 0.4, "position_y": 0.2, "valence": 40},
    "Christian Democrats": {"position_x": 0.1, "position_y": 0.0, "valence": 35},
    "Socialist": {"position_x": -0.3, "position_y": -0.2, "valence": 35},
    "Broad Front": {"position_x": -0.5, "position_y": -0.3, "valence": 40},
    "Communist": {"position_x": -0.7, "position_y": -0.4, "valence": 30},
}
