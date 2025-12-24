"""Core module - ElectionModel and configuration."""

from electoral_sim.core.model import ElectionModel
from electoral_sim.core.config import Config, PartyConfig, PRESETS
from electoral_sim.core.voter_generation import generate_voter_frame, generate_party_frame
from electoral_sim.core.counting import count_fptp, count_pr

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
