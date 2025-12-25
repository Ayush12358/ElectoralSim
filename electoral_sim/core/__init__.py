"""Core module - ElectionModel and configuration."""

from electoral_sim.core.config import PRESETS, Config, PartyConfig
from electoral_sim.core.counting import count_fptp, count_pr
from electoral_sim.core.model import ElectionModel
from electoral_sim.core.voter_generation import generate_party_frame, generate_voter_frame

__all__ = [
    "ElectionModel",
    "Config",
    "PartyConfig",
    "PRESETS",
    "generate_voter_frame",
    "generate_party_frame",
    "count_fptp",
    "count_pr",
]
