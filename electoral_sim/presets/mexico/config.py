"""Mexico Election Preset - Chamber of Deputies.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. Mixed-member system with 300 FPTP districts and 200 PR
list seats matches the real Mexican Chamber of Deputies structure.

Sources: Instituto Nacional Electoral (INE), Mexican Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def mexico_config(
    n_voters: int = 300_000,
    n_constituencies: int = 300,
    **kwargs,
) -> Config:
    """
    Preset configuration for Mexico (Chamber of Deputies).

    300 FPTP district seats + 200 PR list seats, parallel mixed system.

    Parameter rationale: Six major Mexican parties. MORENA (left/populist),
    PAN (center-right), PRI (center/corporatist), MC (center-left), PVEM
    (green/center), PT (left/labor). Valence values are synthetic defaults
    for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("MORENA", -0.3, 0.2, 55),
        PartyConfig("PAN", 0.3, -0.1, 40),
        PartyConfig("PRI", 0.0, 0.0, 35),
        PartyConfig("MC", -0.1, -0.2, 30),
        PartyConfig("PVEM", 0.1, -0.3, 25),
        PartyConfig("PT", -0.5, 0.1, 25),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )


MEXICO_PARTIES = {
    "MORENA": {"position_x": -0.3, "position_y": 0.2, "valence": 55},
    "PAN": {"position_x": 0.3, "position_y": -0.1, "valence": 40},
    "PRI": {"position_x": 0.0, "position_y": 0.0, "valence": 35},
    "MC": {"position_x": -0.1, "position_y": -0.2, "valence": 30},
    "PVEM": {"position_x": 0.1, "position_y": -0.3, "valence": 25},
    "PT": {"position_x": -0.5, "position_y": 0.1, "valence": 25},
}
