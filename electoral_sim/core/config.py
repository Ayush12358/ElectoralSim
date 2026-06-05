"""
Configuration classes for ElectoralSim

Provides dataclass-based configuration for clean model setup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

VALID_ELECTORAL_SYSTEMS = frozenset({"FPTP", "PR"})
VALID_ALLOCATION_METHODS = frozenset({"dhondt", "sainte_lague", "hare", "droop"})

# Domain type aliases (newtypes for API clarity and static analysis)
PartyID = int  # Party identifier (index into party arrays)
ConstituencyID = int  # Constituency identifier
VoterID = int  # Voter identifier
SeatCount = int  # Number of seats (non-negative integer)
VoteShare = float  # Vote share (0.0–1.0)


class CalibrationStatus(str, Enum):
    """Calibration status for election presets."""

    STRUCTURAL_DEMO = "structural_demo"
    PARTIALLY_CALIBRATED = "partially_calibrated"
    HISTORICALLY_CALIBRATED = "historically_calibrated"
    VALIDATION_ONLY = "validation_only"


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
class CandidateConfig:
    """Configuration for a single candidate within a party.

    Enables candidate-level modeling with individual valence,
    incumbency status, local ideology, and demographics.

    Attributes:
        name: Candidate name
        party: Party name this candidate belongs to
        constituency: Constituency ID (or None for party-list)
        position_x: Candidate-specific economic position
        position_y: Candidate-specific social position
        valence: Candidate-level non-policy appeal (overrides party default if higher)
        incumbent: Whether this candidate is an incumbent
    """

    name: str
    party: str
    constituency: int | None = None
    position_x: float = 0.0
    position_y: float = 0.0
    valence: float = 50.0
    incumbent: bool = False


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

    # Candidates (optional candidate-level modeling — preserves party-level API)
    candidates: list[CandidateConfig] | None = None

    # Alliances/blocs (for coalition-heavy systems like India, EU)
    # e.g., alliances = {"NDA": ["BJP", "Others"], "INDIA": ["INC", "SP"]}
    alliances: dict[str, list[str]] | None = None

    # Electoral system
    electoral_system: Literal["FPTP", "PR"] = "FPTP"
    allocation_method: Literal["dhondt", "sainte_lague", "hare", "droop"] = "dhondt"
    threshold: float = 0.0

    # Voting behavior
    temperature: float = 0.5

    # Multi-tier apportionment (national, regional, constituency tiers)
    # e.g., tier_metadata = {"tiers": ["national", "regional"], "seats_per_tier": [200, 300]}
    tier_metadata: dict | None = None

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
from electoral_sim.presets.canada.config import canada_config
from electoral_sim.presets.chile.config import chile_config
from electoral_sim.presets.eu.config import eu_config
from electoral_sim.presets.france.config import france_config
from electoral_sim.presets.germany.config import germany_config
from electoral_sim.presets.india.config import india_config
from electoral_sim.presets.ireland.config import ireland_config
from electoral_sim.presets.israel.config import israel_config
from electoral_sim.presets.japan.config import japan_config
from electoral_sim.presets.mexico.config import mexico_config
from electoral_sim.presets.netherlands.config import netherlands_config
from electoral_sim.presets.norway.config import norway_config
from electoral_sim.presets.nz.config import nz_config
from electoral_sim.presets.scotland.config import scotland_config
from electoral_sim.presets.south_africa.config import south_africa_config
from electoral_sim.presets.spain.config import spain_config
from electoral_sim.presets.sweden.config import sweden_config
from electoral_sim.presets.switzerland.config import switzerland_config
from electoral_sim.presets.uk.config import uk_config
from electoral_sim.presets.usa.config import usa_config
from electoral_sim.presets.wales.config import wales_config


# Preset mapping
PRESETS = {
    "india": india_config,
    "usa": usa_config,
    "uk": uk_config,
    "germany": germany_config,
    "australia_house": australia_house_config,
    "australia_senate": australia_senate_config,
    "south_africa": south_africa_config,
    "spain": spain_config,
    "sweden": sweden_config,
    "brazil": brazil_config,
    "canada": canada_config,
    "chile": chile_config,
    "eu": eu_config,
    "france": france_config,
    "ireland": ireland_config,
    "israel": israel_config,
    "japan": japan_config,
    "mexico": mexico_config,
    "netherlands": netherlands_config,
    "norway": norway_config,
    "nz": nz_config,
    "scotland": scotland_config,
    "switzerland": switzerland_config,
    "wales": wales_config,
}

from electoral_sim.core._provenance import PRESET_PROVENANCE  # noqa: F401, E402
