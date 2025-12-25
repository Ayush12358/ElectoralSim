"""USA Election Preset - House of Representatives."""

from electoral_sim.core.config import Config, PartyConfig


def usa_config(
    n_voters: int = 500_000,
    n_constituencies: int = 435,
    **kwargs,
) -> Config:
    """
    Preset configuration for USA (House of Representatives).

    435 districts, two-party system (FPTP).
    """
    parties = [
        PartyConfig("Democratic", -0.4, -0.2, 50),
        PartyConfig("Republican", 0.4, 0.3, 50),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )


# Party data for reference
USA_PARTIES = {
    "Democratic": {"position_x": -0.4, "position_y": -0.2, "valence": 50},
    "Republican": {"position_x": 0.4, "position_y": 0.3, "valence": 50},
}
