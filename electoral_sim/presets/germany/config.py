"""Germany Election Preset - Bundestag."""

from electoral_sim.core.config import Config, PartyConfig


def germany_config(
    n_voters: int = 500_000,
    n_constituencies: int = 299,  # Direct mandates
    **kwargs,
) -> Config:
    """
    Preset configuration for Germany (Bundestag).

    MMP system with 5% threshold.
    """
    parties = [
        PartyConfig("CDU/CSU", 0.2, 0.1, 50),
        PartyConfig("SPD", -0.2, -0.1, 48),
        PartyConfig("Grüne", -0.3, -0.4, 45),
        PartyConfig("FDP", 0.3, -0.2, 40),
        PartyConfig("AfD", 0.5, 0.5, 35),
        PartyConfig("Linke", -0.5, -0.2, 35),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="sainte_lague",
        threshold=0.05,
        **kwargs,
    )


# Party data for reference
GERMANY_PARTIES = {
    "CDU/CSU": {"position_x": 0.2, "position_y": 0.1, "valence": 50},
    "SPD": {"position_x": -0.2, "position_y": -0.1, "valence": 48},
    "Grüne": {"position_x": -0.3, "position_y": -0.4, "valence": 45},
    "FDP": {"position_x": 0.3, "position_y": -0.2, "valence": 40},
    "AfD": {"position_x": 0.5, "position_y": 0.5, "valence": 35},
    "Linke": {"position_x": -0.5, "position_y": -0.2, "valence": 35},
}
