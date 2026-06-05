"""Ireland Election Preset - Dáil Éireann.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. STV (Single Transferable Vote) in multi-member constituencies
(3-5 seats each) matches the real Irish electoral system.

Sources: Houses of the Oireachtas, Irish Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def ireland_config(
    n_voters: int = 160_000,
    n_constituencies: int = 39,
    **kwargs,
) -> Config:
    """
    Preset configuration for Ireland (Dáil Éireann).

    160 TDs from 39 multi-member constituencies, STV.

    Parameter rationale: Five major Irish parties. Fine Gael (center-right),
    Fianna Fáil (center/catch-all), Sinn Féin (left/nationalist), Labour
    (center-left), Social Democrats (center-left/social democratic), Green
    (left/environmental). Valence values are synthetic defaults for
    comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Fine Gael", 0.3, -0.1, 50),
        PartyConfig("Fianna Fail", 0.1, 0.0, 45),
        PartyConfig("Sinn Fein", -0.5, 0.3, 40),
        PartyConfig("Labour", -0.3, -0.2, 35),
        PartyConfig("Social Democrats", -0.2, -0.3, 30),
        PartyConfig("Green", -0.6, -0.4, 25),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        **kwargs,
    )


IRELAND_PARTIES = {
    "Fine Gael": {"position_x": 0.3, "position_y": -0.1, "valence": 50},
    "Fianna Fail": {"position_x": 0.1, "position_y": 0.0, "valence": 45},
    "Sinn Fein": {"position_x": -0.5, "position_y": 0.3, "valence": 40},
    "Labour": {"position_x": -0.3, "position_y": -0.2, "valence": 35},
    "Social Democrats": {"position_x": -0.2, "position_y": -0.3, "valence": 30},
    "Green": {"position_x": -0.6, "position_y": -0.4, "valence": 25},
}
