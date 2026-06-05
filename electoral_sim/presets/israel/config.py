"""Israel Election Preset - Knesset.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. Nationwide PR with a single national district (120 seats)
and a 3.25% electoral threshold matches the real Israeli electoral system.

Sources: Israel Central Elections Committee, Knesset rules.
"""

from electoral_sim.core.config import Config, PartyConfig


def israel_config(
    n_voters: int = 200_000,
    n_constituencies: int = 1,
    **kwargs,
) -> Config:
    """
    Preset configuration for Israel (Knesset).

    Nationwide PR with 3.25% threshold, 120 seats.

    Parameter rationale: Six significant Israeli parties spanning the
    full ideological spectrum. Likud (right), Yesh Atid (center),
    Labor (center-left), Shas (religious/Sephardi), United Torah
    Judaism (religious/Ashkenazi), Religious Zionism (far-right).
    Valence values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Likud", 0.5, 0.3, 50),
        PartyConfig("Yesh Atid", 0.1, -0.2, 45),
        PartyConfig("Labor", -0.4, -0.3, 40),
        PartyConfig("Shas", 0.3, 0.6, 35),
        PartyConfig("UTJ", 0.4, 0.5, 30),
        PartyConfig("Religious Zionism", 0.7, 0.4, 35),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="dhondt",
        threshold=0.0325,
        **kwargs,
    )


ISRAEL_PARTIES = {
    "Likud": {"position_x": 0.5, "position_y": 0.3, "valence": 50},
    "Yesh Atid": {"position_x": 0.1, "position_y": -0.2, "valence": 45},
    "Labor": {"position_x": -0.4, "position_y": -0.3, "valence": 40},
    "Shas": {"position_x": 0.3, "position_y": 0.6, "valence": 35},
    "UTJ": {"position_x": 0.4, "position_y": 0.5, "valence": 30},
    "Religious Zionism": {"position_x": 0.7, "position_y": 0.4, "valence": 35},
}
