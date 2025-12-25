"""Brazil Election Preset - Chamber of Deputies."""

from electoral_sim.core.config import Config, PartyConfig


def brazil_config(
    n_voters: int = 300_000,
    n_constituencies: int = 26,  # 26 states + Federal District
    **kwargs,
) -> Config:
    """
    Preset configuration for Brazil (Chamber of Deputies).

    513 seats, Open-list PR (D'Hondt).
    """
    parties = [
        PartyConfig("PT", -0.4, 0.2, 60),
        PartyConfig("PL", 0.5, 0.4, 60),
        PartyConfig("União Brasil", 0.1, -0.1, 50),
        PartyConfig("PP", 0.2, -0.2, 50),
        PartyConfig("MDB", 0.0, 0.0, 50),
        PartyConfig("PSD", 0.1, 0.1, 45),
        PartyConfig("Republicanos", 0.3, 0.2, 45),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="PR",
        allocation_method="dhondt",
        **kwargs,
    )


BRAZIL_PARTIES = {
    "PT": {"position_x": -0.4, "position_y": 0.2, "valence": 60},
    "PL": {"position_x": 0.5, "position_y": 0.4, "valence": 60},
    "União": {"position_x": 0.1, "position_y": -0.1, "valence": 50},
    "MDB": {"position_x": 0.0, "position_y": 0.0, "valence": 50},
}
