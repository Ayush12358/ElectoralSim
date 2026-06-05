"""Canada Election Preset - House of Commons.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. 338 ridings (constituencies) and FPTP match the real
Canadian federal electoral system.

Sources: Elections Canada, Canadian Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def canada_config(
    n_voters: int = 338_000,
    n_constituencies: int = 338,
    **kwargs,
) -> Config:
    """
    Preset configuration for Canada (House of Commons).

    338 ridings, multi-party FPTP.

    Parameter rationale: Five major federal parties. Liberal (center-left),
    Conservative (center-right), NDP (left/social democratic), Bloc Quebecois
    (Quebec nationalist, center-left), Green (left/environmental). Valence
    values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Liberal", -0.3, -0.2, 50),
        PartyConfig("Conservative", 0.4, 0.2, 45),
        PartyConfig("NDP", -0.5, -0.3, 40),
        PartyConfig("Bloc Quebecois", -0.2, -0.5, 35),
        PartyConfig("Green", -0.6, -0.4, 30),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )


CANADA_PARTIES = {
    "Liberal": {"position_x": -0.3, "position_y": -0.2, "valence": 50},
    "Conservative": {"position_x": 0.4, "position_y": 0.2, "valence": 45},
    "NDP": {"position_x": -0.5, "position_y": -0.3, "valence": 40},
    "Bloc Quebecois": {"position_x": -0.2, "position_y": -0.5, "valence": 35},
    "Green": {"position_x": -0.6, "position_y": -0.4, "valence": 30},
}
