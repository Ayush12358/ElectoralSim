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

"""EU Parliament Election Preset.

Data provenance: Synthetic/structural preset. Party positions are approximate.
EU Parliament elections use PR (proportional representation) across 27 member
states with degressive proportionality. This preset models 8 political groups
as a simplified single national PR list for demonstration purposes.

Sources: European Parliament (2024-2029 term), EU Political Groups.
"""

from electoral_sim.core.config import Config, PartyConfig


def eu_config(
    n_voters: int = 200_000,
    n_constituencies: int = 1,  # Simplified as national PR list
    **kwargs,
) -> Config:
    """
    Preset configuration for the European Parliament.

    8 political groups competing for 720 MEPs via PR (D'Hondt).

    Parameter rationale: Eight European Parliament political groups as of 2024.
    EPP (center-right), S&D (center-left), Renew (liberal/centrist),
    Greens/EFA (left/green), ECR (conservative/eurosceptic), ID (far-right),
    Left/GUE-NGL (far-left), NI (non-attached/far-right). Valence values are
    synthetic defaults for comparative simulation, not calibrated against
    actual election results.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("EPP", 0.3, -0.2, 65),
        PartyConfig("S&D", -0.3, -0.3, 60),
        PartyConfig("Renew", 0.1, -0.4, 55),
        PartyConfig("Greens/EFA", -0.4, -0.5, 50),
        PartyConfig("ECR", 0.5, 0.3, 45),
        PartyConfig("ID", 0.6, 0.6, 40),
        PartyConfig("Left", -0.6, -0.1, 40),
        PartyConfig("NI", 0.0, 0.5, 30),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="dhondt",
        **kwargs,
    )


EU_PARTIES = {
    "EPP": {"position_x": 0.3, "position_y": -0.2, "valence": 65},
    "S&D": {"position_x": -0.3, "position_y": -0.3, "valence": 60},
    "Renew": {"position_x": 0.1, "position_y": -0.4, "valence": 55},
    "Greens/EFA": {"position_x": -0.4, "position_y": -0.5, "valence": 50},
    "ECR": {"position_x": 0.5, "position_y": 0.3, "valence": 45},
    "ID": {"position_x": 0.6, "position_y": 0.6, "valence": 40},
    "Left": {"position_x": -0.6, "position_y": -0.1, "valence": 40},
    "NI": {"position_x": 0.0, "position_y": 0.5, "valence": 30},
}
