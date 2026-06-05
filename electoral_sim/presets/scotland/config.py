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

"""Scotland Election Preset - Scottish Parliament.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. Additional Member System (AMS) with 73 constituency (FPTP)
seats and 56 regional list (PR) seats matches the real Scottish Parliament.

Sources: Scottish Parliament, Scotland Act 1998.
"""

from electoral_sim.core.config import Config, PartyConfig


def scotland_config(
    n_voters: int = 130_000,
    n_constituencies: int = 73,
    **kwargs,
) -> Config:
    """
    Preset configuration for Scotland (Scottish Parliament).

    73 constituency seats + 56 regional list seats, AMS.

    Parameter rationale: Five major Scottish parties. SNP (center-left/
    nationalist), Labour (center-left), Conservative (center-right),
    Liberal Democrats (centrist/liberal), Green (left/environmental).
    Valence values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("SNP", -0.2, -0.3, 55),
        PartyConfig("Labour", -0.3, -0.1, 40),
        PartyConfig("Conservative", 0.4, 0.2, 35),
        PartyConfig("Liberal Democrat", 0.0, -0.2, 30),
        PartyConfig("Green", -0.6, -0.4, 25),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        allocation_method="dhondt",
        **kwargs,
    )


SCOTLAND_PARTIES = {
    "SNP": {"position_x": -0.2, "position_y": -0.3, "valence": 55},
    "Labour": {"position_x": -0.3, "position_y": -0.1, "valence": 40},
    "Conservative": {"position_x": 0.4, "position_y": 0.2, "valence": 35},
    "Liberal Democrat": {"position_x": 0.0, "position_y": -0.2, "valence": 30},
    "Green": {"position_x": -0.6, "position_y": -0.4, "valence": 25},
}
