"""
Configuration classes for ElectoralSim

Provides dataclass-based configuration for clean model setup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

VALID_ELECTORAL_SYSTEMS = frozenset({"FPTP", "PR"})
VALID_ALLOCATION_METHODS = frozenset({"dhondt", "sainte_lague", "hare", "droop"})


@dataclass
class PartyConfig:
    """Configuration for a single party."""

    name: str
    position_x: float = 0.0
    position_y: float = 0.0
    valence: float = 50.0
    incumbent: bool = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "valence": self.valence,
            "incumbent": self.incumbent,
        }


@dataclass
class Config:
    """
    Main configuration for ElectionModel.

    Example:
        config = Config(
            n_voters=100_000,
            n_constituencies=10,
            electoral_system="FPTP",
        )
        model = ElectionModel(config)

    Attributes:
        n_voters: Total number of voter agents
        n_constituencies: Number of electoral districts
        parties: List of PartyConfig or dicts
        electoral_system: 'FPTP' or 'PR'
        allocation_method: 'dhondt' or 'sainte_lague'
        threshold: Electoral threshold (0-1)
        temperature: MNL temperature (lower = more deterministic)
        seed: Random seed for reproducibility
    """

    # Scale
    n_voters: int = 100_000
    n_constituencies: int = 10

    # Parties (can be list of PartyConfig or dicts)
    parties: list[PartyConfig | dict] = field(default_factory=list)

    # Electoral system
    electoral_system: Literal["FPTP", "PR"] = "FPTP"
    allocation_method: Literal["dhondt", "sainte_lague", "hare", "droop"] = "dhondt"
    threshold: float = 0.0

    # Voting behavior
    temperature: float = 0.5

    # Simulation
    seed: int | None = None

    def __post_init__(self):
        if self.electoral_system not in VALID_ELECTORAL_SYSTEMS:
            raise ValueError(
                f"Unsupported electoral system: '{self.electoral_system}'. "
                f"Valid options: {sorted(VALID_ELECTORAL_SYSTEMS)}"
            )
        if self.allocation_method not in VALID_ALLOCATION_METHODS:
            raise ValueError(
                f"Unknown allocation method: '{self.allocation_method}'. "
                f"Valid options: {sorted(VALID_ALLOCATION_METHODS)}"
            )
        if self.n_voters <= 0:
            raise ValueError(f"n_voters must be positive, got {self.n_voters}")
        if self.n_constituencies <= 0:
            raise ValueError(f"n_constituencies must be positive, got {self.n_constituencies}")
        if not 0 <= self.threshold <= 1:
            raise ValueError(f"threshold must be in [0, 1], got {self.threshold}")
        if self.temperature <= 0:
            raise ValueError(f"temperature must be positive, got {self.temperature}")
        # Convert dicts to PartyConfig if needed
        if self.parties:
            self.parties = [PartyConfig(**p) if isinstance(p, dict) else p for p in self.parties]
        else:
            # Default 3-party system
            self.parties = [
                PartyConfig("Party A", -0.3, 0.1, 50),
                PartyConfig("Party B", 0.3, -0.1, 50),
                PartyConfig("Party C", 0.0, 0.3, 45),
            ]
        # Validate party positions and detect duplicates
        names = set()
        for p in self.parties:
            if p.name in names:
                raise ValueError(f"Duplicate party name: '{p.name}'")
            names.add(p.name)
            if p.valence < 0:
                raise ValueError(f"Party '{p.name}' valence must be >= 0, got {p.valence}")

    def get_party_dicts(self) -> list[dict]:
        """Convert parties to list of dicts for model consumption."""
        return [p.to_dict() if isinstance(p, PartyConfig) else p for p in self.parties]

    @property
    def n_parties(self) -> int:
        return len(self.parties)


# Re-export country configs from presets for backward compatibility
from electoral_sim.presets.australia.config import australia_house_config, australia_senate_config
from electoral_sim.presets.brazil.config import brazil_config
from electoral_sim.presets.eu.config import eu_config
from electoral_sim.presets.france.config import france_config
from electoral_sim.presets.germany.config import germany_config
from electoral_sim.presets.india.config import india_config
from electoral_sim.presets.japan.config import japan_config
from electoral_sim.presets.south_africa.config import south_africa_config
from electoral_sim.presets.uk.config import uk_config
from electoral_sim.presets.usa.config import usa_config


# Preset mapping
PRESETS = {
    "india": india_config,
    "usa": usa_config,
    "uk": uk_config,
    "germany": germany_config,
    "australia_house": australia_house_config,
    "australia_senate": australia_senate_config,
    "south_africa": south_africa_config,
    "brazil": brazil_config,
    "eu": eu_config,
    "france": france_config,
    "japan": japan_config,
}

# Data provenance registry for bundled presets
# Calibration status: structural_demo | partially_calibrated | historically_calibrated | validation_only
PRESET_PROVENANCE = {
    "india": {
        "calibration": "structural_demo",
        "source": "Election Commission of India (synthetic positions)",
        "electoral_system": "FPTP",
        "n_constituencies": 543,
    },
    "usa": {
        "calibration": "structural_demo",
        "source": "Synthetic two-party positions",
        "electoral_system": "FPTP",
        "n_constituencies": 435,
    },
    "uk": {
        "calibration": "structural_demo",
        "source": "Synthetic multi-party positions",
        "electoral_system": "FPTP",
        "n_constituencies": 650,
    },
    "germany": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, Sainte-Lagu\u00eb allocation",
        "electoral_system": "PR",
        "threshold": 0.05,
    },
    "australia_house": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions (FPTP fallback for IRV)",
        "electoral_system": "FPTP",
        "n_constituencies": 151,
    },
    "australia_senate": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions (PR fallback for STV)",
        "electoral_system": "PR",
        "n_constituencies": 8,
    },
    "south_africa": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, pure PR",
        "electoral_system": "PR",
        "allocation": "dhondt",
    },
    "brazil": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, open-list PR",
        "electoral_system": "PR",
        "allocation": "dhondt",
    },
    "eu": {
        "calibration": "structural_demo",
        "source": "European Parliament 2024-2029 term (synthetic positions)",
        "electoral_system": "PR",
        "allocation": "dhondt",
        "n_seats": 720,
    },
    "france": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions (FPTP simulation of two-round)",
        "electoral_system": "FPTP",
    },
    "japan": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions (FPTP base of parallel system)",
        "electoral_system": "FPTP",
    },
}
