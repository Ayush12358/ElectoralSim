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

"""
India Election Data - Constants for the India Lok Sabha simulation.

Contains party configurations, state seat allocations, state-level party
strength weights, and election phase schedules.
"""

from dataclasses import dataclass, field


@dataclass
class StateConfig:
    """Per-state configuration for India Lok Sabha simulation.

    Attributes:
        name: State/UT name
        constituencies: Number of Lok Sabha seats
        party_weights: Per-party strength weights (default: DEFAULT_WEIGHTS)
        ideology_shift: (dx, dy) ideological lean shift (default: (0.0, 0.0))
    """

    name: str
    constituencies: int
    party_weights: dict[str, float] = field(default_factory=dict)
    ideology_shift: tuple[float, float] = (0.0, 0.0)


# States and their Lok Sabha seats
INDIA_STATES = {
    # Large states
    "Uttar Pradesh": 80,
    "Maharashtra": 48,
    "West Bengal": 42,
    "Bihar": 40,
    "Tamil Nadu": 39,
    "Madhya Pradesh": 29,
    "Karnataka": 28,
    "Gujarat": 26,
    "Rajasthan": 25,
    "Andhra Pradesh": 25,
    "Odisha": 21,
    "Kerala": 20,
    "Telangana": 17,
    "Jharkhand": 14,
    "Assam": 14,
    "Punjab": 13,
    "Chhattisgarh": 11,
    "Haryana": 10,
    "Delhi": 7,
    # Smaller states and UTs
    "Jammu & Kashmir": 5,
    "Uttarakhand": 5,
    "Himachal Pradesh": 4,
    "Tripura": 2,
    "Meghalaya": 2,
    "Manipur": 2,
    "Nagaland": 1,
    "Goa": 2,
    "Arunachal Pradesh": 2,
    "Mizoram": 1,
    "Sikkim": 1,
    "Puducherry": 1,
    "Chandigarh": 1,
    "Andaman & Nicobar": 1,
    "Dadra & Nagar Haveli": 1,
    "Daman & Diu": 1,
    "Lakshadweep": 1,
    "Ladakh": 1,
}

# Major parties with ideological positions
# position_x: economic (left=-1, right=+1)
# position_y: social (progressive=-1, conservative=+1)
INDIA_PARTIES = {
    # National parties
    "BJP": {"position_x": 0.4, "position_y": 0.6, "valence": 75, "color": "#FF9933"},
    "INC": {"position_x": -0.2, "position_y": -0.1, "valence": 55, "color": "#00BFFF"},
    "AAP": {"position_x": -0.3, "position_y": -0.3, "valence": 50, "color": "#0066FF"},
    # Regional parties
    "TMC": {"position_x": -0.1, "position_y": 0.1, "valence": 50, "color": "#20C20E"},  # WB
    "DMK": {"position_x": -0.4, "position_y": -0.4, "valence": 55, "color": "#FF0000"},  # TN
    "AIADMK": {"position_x": -0.2, "position_y": 0.0, "valence": 45, "color": "#FF0000"},  # TN
    "SP": {"position_x": -0.3, "position_y": 0.2, "valence": 45, "color": "#FF0000"},  # UP
    "BSP": {"position_x": -0.2, "position_y": 0.1, "valence": 40, "color": "#22409A"},  # UP
    "SS-UBT": {"position_x": 0.1, "position_y": 0.3, "valence": 45, "color": "#FF6600"},  # MH
    "NCP-SP": {"position_x": -0.1, "position_y": 0.0, "valence": 40, "color": "#00008B"},  # MH
    "JD(U)": {"position_x": 0.0, "position_y": 0.2, "valence": 45, "color": "#006400"},  # BR
    "TDP": {"position_x": 0.1, "position_y": 0.1, "valence": 50, "color": "#FFFF00"},  # AP
    "BJD": {"position_x": 0.0, "position_y": 0.0, "valence": 55, "color": "#006400"},  # OD
    "YSR-CP": {"position_x": -0.1, "position_y": 0.1, "valence": 50, "color": "#0000FF"},  # AP
    "BRS": {"position_x": 0.0, "position_y": 0.1, "valence": 45, "color": "#FFC0CB"},  # TG
    "RJD": {"position_x": -0.3, "position_y": 0.2, "valence": 45, "color": "#006400"},  # BR
    "JMM": {"position_x": -0.2, "position_y": 0.1, "valence": 40, "color": "#008000"},  # JH
    "SAD": {"position_x": 0.1, "position_y": 0.3, "valence": 35, "color": "#0000FF"},  # PB
    "Others": {"position_x": 0.0, "position_y": 0.0, "valence": 25, "color": "#808080"},
}

# State-wise party strength (probability weights influencing vote utility)
STATE_PARTY_WEIGHTS = {
    "Uttar Pradesh": {"BJP": 0.35, "SP": 0.25, "BSP": 0.15, "INC": 0.15, "Others": 0.10},
    "Maharashtra": {"BJP": 0.25, "SS-UBT": 0.15, "NCP-SP": 0.15, "INC": 0.20, "Others": 0.25},
    "West Bengal": {"TMC": 0.45, "BJP": 0.35, "INC": 0.05, "Others": 0.15},
    "Bihar": {"BJP": 0.25, "JD(U)": 0.20, "RJD": 0.25, "INC": 0.10, "Others": 0.20},
    "Tamil Nadu": {"DMK": 0.40, "AIADMK": 0.30, "BJP": 0.10, "INC": 0.10, "Others": 0.10},
    "Gujarat": {"BJP": 0.55, "INC": 0.35, "AAP": 0.05, "Others": 0.05},
    "Rajasthan": {"BJP": 0.45, "INC": 0.45, "Others": 0.10},
    "Madhya Pradesh": {"BJP": 0.50, "INC": 0.40, "Others": 0.10},
    "Karnataka": {"BJP": 0.40, "INC": 0.40, "JD(U)": 0.10, "Others": 0.10},
    "Andhra Pradesh": {"YSR-CP": 0.40, "TDP": 0.35, "BJP": 0.15, "Others": 0.10},
    "Telangana": {"BRS": 0.35, "INC": 0.30, "BJP": 0.25, "Others": 0.10},
    "Odisha": {"BJD": 0.45, "BJP": 0.35, "INC": 0.10, "Others": 0.10},
    "Kerala": {"INC": 0.35, "BJP": 0.20, "Others": 0.45},
    "Jharkhand": {"BJP": 0.35, "JMM": 0.30, "INC": 0.15, "Others": 0.20},
    "Assam": {"BJP": 0.45, "INC": 0.35, "Others": 0.20},
    "Punjab": {"INC": 0.30, "AAP": 0.30, "SAD": 0.15, "BJP": 0.15, "Others": 0.10},
    "Delhi": {"BJP": 0.40, "AAP": 0.35, "INC": 0.20, "Others": 0.05},
    "Haryana": {"BJP": 0.45, "INC": 0.40, "Others": 0.15},
    "Chhattisgarh": {"BJP": 0.45, "INC": 0.45, "Others": 0.10},
    "Uttarakhand": {"BJP": 0.55, "INC": 0.35, "Others": 0.10},
    "Himachal Pradesh": {"BJP": 0.50, "INC": 0.45, "Others": 0.05},
}

# Default weights for states not specified
DEFAULT_WEIGHTS = {"BJP": 0.40, "INC": 0.35, "Others": 0.25}

# State-specific ideology shifts (economic x, social y)
STATE_IDEOLOGY_SHIFTS = {
    "Gujarat": (0.1, 0.1),
    "Rajasthan": (0.1, 0.1),
    "Madhya Pradesh": (0.1, 0.1),
    "Uttar Pradesh": (0.1, 0.1),
    "Kerala": (-0.1, 0.0),
    "West Bengal": (-0.1, 0.0),
    "Tamil Nadu": (-0.1, 0.0),
}

# Phase-wise election schedule (2024 pattern, 7 phases)
INDIA_ELECTION_PHASES = {
    1: [
        "Assam",
        "Arunachal Pradesh",
        "Meghalaya",
        "Manipur",
        "Mizoram",
        "Nagaland",
        "Tripura",
        "Sikkim",
        "Uttarakhand",
        "Jammu & Kashmir",
        "Rajasthan",
    ],
    2: ["Kerala", "Karnataka", "Madhya Pradesh", "Chhattisgarh", "Maharashtra"],
    3: ["Gujarat", "Bihar", "Jharkhand", "Odisha", "West Bengal"],
    4: ["Andhra Pradesh", "Telangana", "Tamil Nadu", "Puducherry"],
    5: ["Uttar Pradesh", "Punjab", "Haryana", "Delhi", "Chandigarh", "Himachal Pradesh", "Ladakh"],
    6: ["Uttar Pradesh"],
    7: ["Bihar", "Uttar Pradesh", "West Bengal"],
}

# Alliance definitions
NDA_PARTIES = {"BJP", "JD(U)", "TDP", "SAD"}
INDIA_BLOC_PARTIES = {"INC", "AAP", "TMC", "DMK", "SP", "RJD", "SS-UBT", "NCP-SP", "JMM"}

# Per-state Config registry — unified access to seats, weights, and ideology shifts.
STATE_CONFIGS: dict[str, StateConfig] = {}
for state_name, n_constituencies in INDIA_STATES.items():
    STATE_CONFIGS[state_name] = StateConfig(
        name=state_name,
        constituencies=n_constituencies,
        party_weights=STATE_PARTY_WEIGHTS.get(state_name, DEFAULT_WEIGHTS),
        ideology_shift=STATE_IDEOLOGY_SHIFTS.get(state_name, (0.0, 0.0)),
    )
