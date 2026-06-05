"""Wales Election Preset - Senedd Cymru.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. Additional Member System (AMS) with 40 constituency (FPTP)
seats and 20 regional list (PR) seats matches the real Welsh Senedd.

Sources: Senedd Cymru, Government of Wales Act 2006.
"""

from electoral_sim.core.config import Config, PartyConfig


def wales_config(
    n_voters: int = 60_000,
    n_constituencies: int = 40,
    **kwargs,
) -> Config:
    """
    Preset configuration for Wales (Senedd Cymru).

    40 constituency seats + 20 regional list seats, AMS.

    Parameter rationale: Four major Welsh parties. Labour (center-left,
    dominant), Conservative (center-right), Plaid Cymru (center-left/
    nationalist), Liberal Democrats (centrist/liberal). Valence values
    are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Labour", -0.3, -0.1, 55),
        PartyConfig("Conservative", 0.4, 0.2, 35),
        PartyConfig("Plaid Cymru", -0.2, -0.3, 40),
        PartyConfig("Liberal Democrat", 0.0, -0.2, 25),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        allocation_method="dhondt",
        **kwargs,
    )


WALES_PARTIES = {
    "Labour": {"position_x": -0.3, "position_y": -0.1, "valence": 55},
    "Conservative": {"position_x": 0.4, "position_y": 0.2, "valence": 35},
    "Plaid Cymru": {"position_x": -0.2, "position_y": -0.3, "valence": 40},
    "Liberal Democrat": {"position_x": 0.0, "position_y": -0.2, "valence": 25},
}
