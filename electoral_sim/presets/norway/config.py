"""Norway Election Preset - Storting.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. PR with Sainte-Lague allocation and leveling seats in
19 multi-member counties matches the real Norwegian electoral system.

Sources: Norwegian Directorate of Elections, Norwegian Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def norway_config(
    n_voters: int = 169_000,
    n_constituencies: int = 19,
    **kwargs,
) -> Config:
    """
    Preset configuration for Norway (Storting).

    169 seats from 19 counties, Sainte-Lague PR with 4% threshold.

    Parameter rationale: Seven major Norwegian parties. Labour (center-left/
    social democratic), Conservative (center-right), Centre (centrist/
    agrarian), Progress (right/populist), Socialist Left (left/socialist),
    Liberal (centrist/social-liberal), Christian Democrat (center/Christian).
    Valence values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Labour", -0.3, -0.1, 50),
        PartyConfig("Conservative", 0.3, 0.1, 45),
        PartyConfig("Centre", 0.1, 0.2, 35),
        PartyConfig("Progress", 0.6, 0.4, 30),
        PartyConfig("Socialist Left", -0.6, -0.3, 30),
        PartyConfig("Liberal", 0.1, -0.2, 25),
        PartyConfig("Christian Democrat", 0.2, 0.3, 25),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="sainte_lague",
        threshold=0.04,
        **kwargs,
    )


NORWAY_PARTIES = {
    "Labour": {"position_x": -0.3, "position_y": -0.1, "valence": 50},
    "Conservative": {"position_x": 0.3, "position_y": 0.1, "valence": 45},
    "Centre": {"position_x": 0.1, "position_y": 0.2, "valence": 35},
    "Progress": {"position_x": 0.6, "position_y": 0.4, "valence": 30},
    "Socialist Left": {"position_x": -0.6, "position_y": -0.3, "valence": 30},
    "Liberal": {"position_x": 0.1, "position_y": -0.2, "valence": 25},
    "Christian Democrat": {"position_x": 0.2, "position_y": 0.3, "valence": 25},
}
