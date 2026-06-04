"""USA Election Preset - House of Representatives.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values, not estimated from survey data. Seat counts and electoral
system rules (435 districts, FPTP) match the real institution.

Calibration status: ❌ Not calibrated. Party positions and valence are synthetic
defaults. For a calibrated US model, real election returns by district from MIT
Election Lab (https://electionlab.mit.edu/data) or MEDSL are recommended.

Sources: U.S. Constitution, House of Representatives rules.
"""

from electoral_sim.core.config import Config, PartyConfig


def usa_config(
    n_voters: int = 500_000,
    n_constituencies: int = 435,
    **kwargs,
) -> Config:
    """
    Preset configuration for USA (House of Representatives).

    435 districts, two-party system (FPTP).

    Parameter rationale: Parties are placed on a standard 2D ideological space
    (economic left-right, social liberal-conservative). Democrats center-left,
    Republicans center-right. Equal valence (50) reflects a competitive baseline.
    These are synthetic defaults for comparative simulation, not calibrated.

    Calibration status: ❌ Not calibrated.
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


# Party data for reference
USA_PARTIES = {
    "Democratic": {"position_x": -0.4, "position_y": -0.2, "valence": 50},
    "Republican": {"position_x": 0.4, "position_y": 0.3, "valence": 50},
}
