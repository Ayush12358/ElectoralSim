"""Japan Election Preset - House of Representatives."""

from electoral_sim.core.config import Config, PartyConfig


def japan_config(
    n_voters: int = 250_000,
    n_constituencies: int = 289,  # FPTP districts (total 465 seats with 176 PR)
    **kwargs,
) -> Config:
    """
    Preset configuration for Japan (House of Representatives).

    Parallel system (289 FPTP + 176 PR). Defaulting here to FPTP base
    for the primary constituency model.
    """
    parties = [
        PartyConfig("LDP", 0.4, 0.2, 70),
        PartyConfig("CDP", -0.3, -0.1, 55),
        PartyConfig("Ishin", 0.5, -0.3, 50),
        PartyConfig("Komeito", 0.2, 0.3, 45),
        PartyConfig("JCP", -0.7, 0.1, 40),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",  # Parallel system base
        **kwargs,
    )


JAPAN_PARTIES = {
    "LDP": {"position_x": 0.4, "position_y": 0.2, "valence": 70},
    "CDP": {"position_x": -0.3, "position_y": -0.1, "valence": 55},
    "Ishin": {"position_x": 0.5, "position_y": -0.3, "valence": 50},
}
