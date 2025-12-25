"""UK Election Preset - House of Commons."""

from electoral_sim.core.config import Config, PartyConfig


def uk_config(
    n_voters: int = 500_000,
    n_constituencies: int = 650,
    **kwargs,
) -> Config:
    """
    Preset configuration for UK (House of Commons).

    650 constituencies, multi-party FPTP.
    """
    parties = [
        PartyConfig("Conservative", 0.3, 0.2, 45),
        PartyConfig("Labour", -0.3, -0.1, 50),
        PartyConfig("Liberal Democrats", 0.0, -0.2, 40),
        PartyConfig("SNP", -0.2, -0.3, 45),
        PartyConfig("Green", -0.5, -0.4, 35),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )


# Party data for reference
UK_PARTIES = {
    "Conservative": {"position_x": 0.3, "position_y": 0.2, "valence": 45},
    "Labour": {"position_x": -0.3, "position_y": -0.1, "valence": 50},
    "Liberal Democrats": {"position_x": 0.0, "position_y": -0.2, "valence": 40},
    "SNP": {"position_x": -0.2, "position_y": -0.3, "valence": 45},
    "Green": {"position_x": -0.5, "position_y": -0.4, "valence": 35},
}
