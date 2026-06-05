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

"""Switzerland Election Preset - National Council.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. PR (proportional representation) with 26 cantonal districts
matches the real Swiss electoral system.

Sources: Swiss Federal Statistical Office, Swiss Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def switzerland_config(
    n_voters: int = 200_000,
    n_constituencies: int = 26,
    **kwargs,
) -> Config:
    """
    Preset configuration for Switzerland (National Council).

    26 cantons, PR with multi-party system. Referendum/direct-democracy
    hooks are modeled as separate ballot events rather than party-seat
    contests.

    Parameter rationale: Five major Swiss parties. SVP (right/populist),
    SP (social democratic), FDP (liberal/center-right), Centre (Christian
    democrat/center), Greens (left/environmental). Valence values are
    synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("SVP", 0.5, 0.5, 50),
        PartyConfig("SP", -0.4, -0.3, 45),
        PartyConfig("FDP", 0.3, -0.1, 40),
        PartyConfig("Centre", 0.1, 0.2, 35),
        PartyConfig("Greens", -0.6, -0.4, 35),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="dhondt",
        **kwargs,
    )


SWITZERLAND_PARTIES = {
    "SVP": {"position_x": 0.5, "position_y": 0.5, "valence": 50},
    "SP": {"position_x": -0.4, "position_y": -0.3, "valence": 45},
    "FDP": {"position_x": 0.3, "position_y": -0.1, "valence": 40},
    "Centre": {"position_x": 0.1, "position_y": 0.2, "valence": 35},
    "Greens": {"position_x": -0.6, "position_y": -0.4, "valence": 35},
}
