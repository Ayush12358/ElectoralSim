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

"""Spain Election Preset - Congress of Deputies.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. D'Hondt PR in multi-member provinces matches the real
Spanish electoral system.

Sources: Junta Electoral Central, Spanish Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def spain_config(
    n_voters: int = 350_000,
    n_constituencies: int = 52,
    **kwargs,
) -> Config:
    """
    Preset configuration for Spain (Congress of Deputies).

    350 seats from 52 multi-member provinces, D'Hondt PR with 3% threshold.

    Parameter rationale: Six major Spanish parties. PP (center-right/
    conservative), PSOE (center-left/social democratic), Vox (far-right),
    Sumar (left coalition), Podemos (left/populist), Ciudadanos (center/
    liberal). Valence values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("PP", 0.4, 0.2, 45),
        PartyConfig("PSOE", -0.3, -0.1, 50),
        PartyConfig("Vox", 0.7, 0.5, 35),
        PartyConfig("Sumar", -0.5, -0.3, 30),
        PartyConfig("Podemos", -0.6, -0.2, 25),
        PartyConfig("Ciudadanos", 0.1, -0.1, 25),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="dhondt",
        threshold=0.03,
        **kwargs,
    )


SPAIN_PARTIES = {
    "PP": {"position_x": 0.4, "position_y": 0.2, "valence": 45},
    "PSOE": {"position_x": -0.3, "position_y": -0.1, "valence": 50},
    "Vox": {"position_x": 0.7, "position_y": 0.5, "valence": 35},
    "Sumar": {"position_x": -0.5, "position_y": -0.3, "valence": 30},
    "Podemos": {"position_x": -0.6, "position_y": -0.2, "valence": 25},
    "Ciudadanos": {"position_x": 0.1, "position_y": -0.1, "valence": 25},
}
