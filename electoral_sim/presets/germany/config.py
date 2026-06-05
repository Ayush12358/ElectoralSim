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

"""Germany Election Preset - Bundestag.

Data provenance: Synthetic/structural preset. Party positions are approximate.
The MMP system, 5% threshold, and Sainte-Laguë allocation match real rules.
299 direct mandates + compensatory list seats.

Calibration status: ❌ Not calibrated. For calibration, the German Longitudinal
Election Study (GLES, https://gles.eu) provides survey data, and the
Bundeswahlleiter provides official election returns.

Sources: Bundeswahlgesetz (Federal Election Act), Bundeswahlleiter.
"""

from electoral_sim.core.config import Config, PartyConfig


def germany_config(
    n_voters: int = 500_000,
    n_constituencies: int = 299,  # Direct mandates
    **kwargs,
) -> Config:
    """
    Preset configuration for Germany (Bundestag).

    MMP system with 5% threshold.

    Parameter rationale: Six major parties spanning the German political spectrum.
    CDU/CSU center-right, SPD center-left, Grüne left/progressive, FDP right/liberal,
    AfD far-right, Linke far-left. The 5% threshold is the real German hurdle.
    Valence values are synthetic defaults; party positions approximate the
    standard German party landscape for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("CDU/CSU", 0.2, 0.1, 50),
        PartyConfig("SPD", -0.2, -0.1, 48),
        PartyConfig("Grüne", -0.3, -0.4, 45),
        PartyConfig("FDP", 0.3, -0.2, 40),
        PartyConfig("AfD", 0.5, 0.5, 35),
        PartyConfig("Linke", -0.5, -0.2, 35),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="sainte_lague",
        threshold=0.05,
        **kwargs,
    )


# Party data for reference
GERMANY_PARTIES = {
    "CDU/CSU": {"position_x": 0.2, "position_y": 0.1, "valence": 50},
    "SPD": {"position_x": -0.2, "position_y": -0.1, "valence": 48},
    "Grüne": {"position_x": -0.3, "position_y": -0.4, "valence": 45},
    "FDP": {"position_x": 0.3, "position_y": -0.2, "valence": 40},
    "AfD": {"position_x": 0.5, "position_y": 0.5, "valence": 35},
    "Linke": {"position_x": -0.5, "position_y": -0.2, "valence": 35},
}
