"""France Election Preset - National Assembly."""

from electoral_sim.core.config import Config, PartyConfig


def france_config(
    n_voters: int = 300_000,
    n_constituencies: int = 577,
    **kwargs,
) -> Config:
    """
    Preset configuration for France (National Assembly).

    577 constituencies, Two-Round System (simulated as FPTP with major alliances).
    """
    parties = [
        PartyConfig("NFP", -0.5, 0.3, 60),  # Left Alliance
        PartyConfig("Ensemble", 0.0, -0.1, 55),  # Center (Macron)
        PartyConfig("RN", 0.6, 0.5, 65),  # Far Right (Le Pen)
        PartyConfig("LR", 0.3, 0.1, 45),  # Traditional Right
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )


FRANCE_PARTIES = {
    "NFP": {"position_x": -0.5, "position_y": 0.3, "valence": 60},
    "Ensemble": {"position_x": 0.0, "position_y": -0.1, "valence": 55},
    "RN": {"position_x": 0.6, "position_y": 0.5, "valence": 65},
    "LR": {"position_x": 0.3, "position_y": 0.1, "valence": 45},
}
