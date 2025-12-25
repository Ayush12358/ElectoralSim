"""South Africa Election Preset - National Assembly."""

from electoral_sim.core.config import Config, PartyConfig


def south_africa_config(
    n_voters: int = 200_000,
    n_constituencies: int = 1,  # National list (simplified)
    **kwargs,
) -> Config:
    """
    Preset configuration for South Africa (National Assembly).

    Pure PR (Proportional Representation).
    """
    parties = [
        PartyConfig("ANC", -0.2, 0.1, 55),
        PartyConfig("DA", 0.3, -0.2, 50),
        PartyConfig("MK", -0.4, 0.4, 45),
        PartyConfig("EFF", -0.8, 0.5, 40),
        PartyConfig("IFP", 0.5, 0.3, 35),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="dhondt",
        **kwargs,
    )


SOUTH_AFRICA_PARTIES = {
    "ANC": {"position_x": -0.2, "position_y": 0.1, "valence": 55},
    "DA": {"position_x": 0.3, "position_y": -0.2, "valence": 50},
    "MK": {"position_x": -0.4, "position_y": 0.4, "valence": 45},
    "EFF": {"position_x": -0.8, "position_y": 0.5, "valence": 40},
    "IFP": {"position_x": 0.5, "position_y": 0.3, "valence": 35},
}
