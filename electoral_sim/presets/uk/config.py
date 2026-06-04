"""UK Election Preset - House of Commons.

Data provenance: Synthetic/structural preset. Party positions are approximate
demonstration values. 650 constituencies and FPTP match the real institution.

Calibration status: ❌ Not calibrated. For calibration, the British Election Study
(https://www.britishelectionstudy.com) provides individual-level survey data, and
the UK Electoral Commission provides official results.

Sources: UK Parliament rules, House of Commons Library.
"""

from electoral_sim.core.config import Config, PartyConfig


def uk_config(
    n_voters: int = 500_000,
    n_constituencies: int = 650,
    **kwargs,
) -> Config:
    """
    Preset configuration for UK (House of Commons).

    650 constituencies, multi-party FPTP.

    Parameter rationale: Five major UK-wide parties placed on a 2D space.
    SNP represents Scottish nationalism. Valence values range 35-50 to reflect
    relative competitiveness. These are synthetic defaults for comparative
    simulation, not calibrated against election data.

    Calibration status: ❌ Not calibrated.
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
