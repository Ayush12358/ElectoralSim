"""
Configuration classes for ElectoralSim

Provides dataclass-based configuration for clean model setup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


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
        # Convert dicts to PartyConfig if needed
        if self.parties:
            self.parties = [
                PartyConfig(**p) if isinstance(p, dict) else p
                for p in self.parties
            ]
        else:
            # Default 3-party system
            self.parties = [
                PartyConfig("Party A", -0.3, 0.1, 50),
                PartyConfig("Party B", 0.3, -0.1, 50),
                PartyConfig("Party C", 0.0, 0.3, 45),
            ]
    
    def get_party_dicts(self) -> list[dict]:
        """Convert parties to list of dicts for model consumption."""
        return [p.to_dict() if isinstance(p, PartyConfig) else p for p in self.parties]
    
    @property
    def n_parties(self) -> int:
        return len(self.parties)


# =============================================================================
# PRESET CONFIGURATIONS
# =============================================================================

def india_config(
    n_voters: int = 1_000_000,
    n_constituencies: int = 543,
    **kwargs,
) -> Config:
    """
    Preset configuration for India (Lok Sabha).
    
    543 constituencies, major national parties.
    """
    parties = [
        PartyConfig("BJP", 0.4, 0.5, 70),
        PartyConfig("INC", -0.2, -0.1, 55),
        PartyConfig("AAP", -0.3, -0.3, 50),
        PartyConfig("TMC", -0.1, 0.1, 45),
        PartyConfig("DMK", -0.4, -0.4, 45),
        PartyConfig("SP", -0.2, 0.2, 40),
        PartyConfig("BSP", -0.1, 0.3, 35),
        PartyConfig("Others", 0.0, 0.0, 30),
    ]
    
    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )


def usa_config(
    n_voters: int = 500_000,
    n_constituencies: int = 435,
    **kwargs,
) -> Config:
    """
    Preset configuration for USA (House of Representatives).
    
    435 districts, two-party system.
    """
    parties = [
        PartyConfig("Democratic", -0.4, -0.2, 50),
        PartyConfig("Republican", 0.4, 0.3, 50),
    ]
    
    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )


def uk_config(
    n_voters: int = 500_000,
    n_constituencies: int = 650,
    **kwargs,
) -> Config:
    """
    Preset configuration for UK (House of Commons).
    
    650 constituencies, multi-party FPTP.
    """
    parties = [
        PartyConfig("Conservative", 0.3, 0.2, 45),
        PartyConfig("Labour", -0.3, -0.1, 50),
        PartyConfig("Liberal Democrats", 0.0, -0.2, 40),
        PartyConfig("SNP", -0.2, -0.3, 45),
        PartyConfig("Green", -0.5, -0.4, 35),
    ]
    
    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )


def germany_config(
    n_voters: int = 500_000,
    n_constituencies: int = 299,  # Direct mandates
    **kwargs,
) -> Config:
    """
    Preset configuration for Germany (Bundestag).
    
    MMP system with 5% threshold.
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


# Preset mapping
PRESETS = {
    "india": india_config,
    "usa": usa_config,
    "uk": uk_config,
    "germany": germany_config,
}
