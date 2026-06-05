"""Netherlands Election Preset - Tweede Kamer.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. Nationwide PR with a single national district (150 seats)
and a very low 0.67% threshold matches the real Dutch electoral system.

Sources: Kiesraad (Dutch Electoral Council), Dutch Constitution.
"""

from electoral_sim.core.config import Config, PartyConfig


def netherlands_config(
    n_voters: int = 200_000,
    n_constituencies: int = 1,
    **kwargs,
) -> Config:
    """
    Preset configuration for Netherlands (Tweede Kamer).

    Nationwide PR with 0.67% threshold, 150 seats. Useful for
    fragmentation and coalition comparison studies.

    Parameter rationale: Eight major Dutch parties spanning the full
    ideological spectrum. VVD (center-right/liberal), D66 (social-liberal),
    CDA (Christian democrat), PvdA/GL (center-left/green), SP (socialist),
    PVV (far-right), FvD (far-right/conservative), CU (Christian/social).
    Valence values are synthetic defaults for comparative simulation.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("VVD", 0.4, -0.1, 50),
        PartyConfig("D66", 0.1, -0.3, 45),
        PartyConfig("CDA", 0.3, 0.1, 40),
        PartyConfig("PvdA/GL", -0.4, -0.4, 45),
        PartyConfig("SP", -0.6, -0.2, 35),
        PartyConfig("PVV", 0.7, 0.4, 30),
        PartyConfig("FvD", 0.8, 0.6, 25),
        PartyConfig("CU", 0.2, 0.4, 30),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="dhondt",
        threshold=0.0067,
        **kwargs,
    )


NETHERLANDS_PARTIES = {
    "VVD": {"position_x": 0.4, "position_y": -0.1, "valence": 50},
    "D66": {"position_x": 0.1, "position_y": -0.3, "valence": 45},
    "CDA": {"position_x": 0.3, "position_y": 0.1, "valence": 40},
    "PvdA/GL": {"position_x": -0.4, "position_y": -0.4, "valence": 45},
    "SP": {"position_x": -0.6, "position_y": -0.2, "valence": 35},
    "PVV": {"position_x": 0.7, "position_y": 0.4, "valence": 30},
    "FvD": {"position_x": 0.8, "position_y": 0.6, "valence": 25},
    "CU": {"position_x": 0.2, "position_y": 0.4, "valence": 30},
}
