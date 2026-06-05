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

"""New Zealand Election Preset - House of Representatives.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. MMP (Mixed-Member Proportional) with 72 electorate
(FPTP) seats and 48 list (PR) seats matches the real NZ system. A 5% threshold
or one electorate seat qualifies for list seats.

Sources: Electoral Commission of New Zealand, Electoral Act 1993.
"""

from electoral_sim.core.config import Config, PartyConfig


def nz_config(
    n_voters: int = 120_000,
    n_constituencies: int = 72,
    **kwargs,
) -> Config:
    """
    Preset configuration for New Zealand (House of Representatives).

    72 electorate seats + 48 list seats, MMP with 5% threshold.

    Parameter rationale: Five major NZ parties. Labour (center-left),
    National (center-right), Green (left/environmental), ACT (right/
    libertarian), NZ First (centrist/populist), Maori Party (indigenous
    rights). Valence values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Labour", -0.4, -0.2, 50),
        PartyConfig("National", 0.3, 0.1, 45),
        PartyConfig("Green", -0.6, -0.4, 35),
        PartyConfig("ACT", 0.6, 0.3, 30),
        PartyConfig("NZ First", 0.1, 0.4, 25),
        PartyConfig("Maori", -0.3, 0.5, 20),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        allocation_method="dhondt",
        threshold=0.05,
        **kwargs,
    )


NZ_PARTIES = {
    "Labour": {"position_x": -0.4, "position_y": -0.2, "valence": 50},
    "National": {"position_x": 0.3, "position_y": 0.1, "valence": 45},
    "Green": {"position_x": -0.6, "position_y": -0.4, "valence": 35},
    "ACT": {"position_x": 0.6, "position_y": 0.3, "valence": 30},
    "NZ First": {"position_x": 0.1, "position_y": 0.4, "valence": 25},
    "Maori": {"position_x": -0.3, "position_y": 0.5, "valence": 20},
}
