"""Australia Election Preset - House and Senate.

Data provenance: Synthetic/structural preset. Party positions are approximate.
151 House districts (IRV) and 8 state/territory Senate divisions (STV) match
the real Australian electoral system. Compulsory voting is not modeled.

Sources: Australian Constitution, Australian Electoral Commission (AEC).
"""

from electoral_sim.core.config import Config, PartyConfig


def australia_house_config(
    n_voters: int = 150_000,
    n_constituencies: int = 151,
    **kwargs,
) -> Config:
    """
    Preset configuration for Australia (House of Representatives).

    151 districts, IRV (Instant Runoff Voting).

    Parameter rationale: Four major Australian parties plus Independents.
    Labor (center-left), Liberal/National Coalition (center-right), Greens (left/environmental),
    One Nation (far-right). Valence values are synthetic defaults for comparative
    simulation, not calibrated against AEC results.

    Calibration status: ❌ Not calibrated.
    """
    parties = [
        PartyConfig("Labor", -0.3, -0.1, 55),
        PartyConfig("Liberal", 0.4, 0.2, 55),
        PartyConfig("Greens", -0.7, -0.4, 45),
        PartyConfig("One Nation", 0.8, 0.6, 40),
        PartyConfig("Independent", 0.0, 0.0, 45),
    ]

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="IRV",
        **kwargs,
    )


def australia_senate_config(
    n_voters: int = 150_000,
    n_constituencies: int = 8,  # 6 states + 2 territories
    **kwargs,
) -> Config:
    """
    Preset configuration for Australia (Senate).

    8 districts (states/territories), STV (Single Transferable Vote).
    """
    parties = [
        PartyConfig("Labor", -0.3, -0.1, 55),
        PartyConfig("Liberal", 0.4, 0.2, 55),
        PartyConfig("Greens", -0.7, -0.4, 45),
        PartyConfig("One Nation", 0.8, 0.6, 40),
    ]

    # 76 seats total, usually 12 per state
    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="STV",
        **kwargs,
    )


AUSTRALIA_PARTIES = {
    "Labor": {"position_x": -0.3, "position_y": -0.1, "valence": 55},
    "Liberal": {"position_x": 0.4, "position_y": 0.2, "valence": 55},
    "Greens": {"position_x": -0.7, "position_y": -0.4, "valence": 45},
    "One Nation": {"position_x": 0.8, "position_y": 0.6, "valence": 40},
}
