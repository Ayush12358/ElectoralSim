"""
India Election Preset - Config for generic ElectionModel.

Provides india_config() for the PRESETS registry and IndiaElectionModel
that runs state-by-state simulation through the generic engine.
"""

from electoral_sim.core.config import Config, PartyConfig
from electoral_sim.presets.india.data import INDIA_PARTIES


def india_config(
    n_voters: int = 1_000_000,
    n_constituencies: int = 543,
    **kwargs,
) -> Config:
    """
    Preset configuration for India (Lok Sabha).

    For full state-by-state simulation with regional party weights,
    use `simulate_india_election()` instead.

    Data provenance: Synthetic/structural preset. Party positions are approximate
    demonstration values not estimated from survey data. 543 constituencies and
    FPTP system match the real Lok Sabha.

    Parameter rationale: Includes 19 national and regional parties placed on a 2D
    ideological space. Valence values are synthetic defaults intended to produce
    plausible competition patterns, not calibrated against election data.

    Calibration status: ❌ Not calibrated. For the full calibrated simulator with
    state-level weights, alliance counting, and NOTA detection, use
    `simulate_india_election()` which runs state-by-state simulations through the
    generic ElectionModel engine.

    Sources: Election Commission of India, Constitution of India.

    Args:
        n_voters: Total voters across all constituencies
        n_constituencies: Number of Lok Sabha constituencies (default 543)
        **kwargs: Additional Config parameters

    Returns:
        Config object for ElectionModel
    """
    # Build party list from INDIA_PARTIES data
    parties = []
    for name, pdata in INDIA_PARTIES.items():
        parties.append(
            PartyConfig(
                name=name,
                position_x=pdata["position_x"],
                position_y=pdata["position_y"],
                valence=pdata["valence"],
            )
        )

    return Config(
        n_voters=n_voters,
        n_constituencies=n_constituencies,
        parties=parties,
        electoral_system="FPTP",
        **kwargs,
    )
