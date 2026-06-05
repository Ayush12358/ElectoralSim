"""
Voter Generation Module

Contains functions for generating voter DataFrames with demographics,
ideology, and behavioral attributes.


CSES-Style Survey Calibration
-----------------------------
The Comparative Study of Electoral Systems (CSES) provides standardized
post-election survey variables that can be mapped to simulation parameters
for calibrated presets. Below is the recommended mapping:

CSES Variable → Simulation Parameter
    vote_choice        → party_id (target for behavior model fitting)
    ideology_LR        → ideology_x (left-right self-placement)
    age, education     → knowledge, turnout_prob (demographic weights)
    political_trust    → media_susceptibility (inverse)
    democratic_satisf  → turnout_prob (modifier)
    income_change      → personal_income_change (pocketbook model)
    retrospective_eco  → economic_perception (sociotropic model)

Usage for calibration:
    1. Load CSES data for the target election
    2. Map variables to the simulation parameter space
    3. Fit behavior model weights to match observed vote choice
    4. Validate against held-out elections

Data download is optional and not bundled with the package. See:
    https://cses.org/ for data access and licensing.
"""

import numpy as np
import polars as pl


def generate_party_frame(
    parties: list[dict],
    include_nota: bool = False,
) -> pl.DataFrame:
    """
    Generate party DataFrame from configuration.

    Args:
        parties: List of party configuration dicts
        include_nota: Whether to add NOTA (None of the Above) option

    Returns:
        Polars DataFrame with party attributes
    """
    party_data = [
        {
            "name": p.get("name", f"Party {i}"),
            "position_x": float(p.get("position_x", 0.0)),
            "position_y": float(p.get("position_y", 0.0)),
            "valence": float(p.get("valence", 50.0)),
            "incumbent": bool(p.get("incumbent", False)),
            "is_nota": False,
        }
        for i, p in enumerate(parties)
    ]

    # Add NOTA if requested
    if include_nota:
        party_data.append(
            {
                "name": "NOTA",
                "position_x": 0.0,
                "position_y": 0.0,
                "valence": 0.0,  # No appeal
                "incumbent": False,
                "is_nota": True,
            }
        )

    return pl.DataFrame(party_data)


from electoral_sim.core._voter_gen import generate_voter_frame  # noqa: E402, F401
