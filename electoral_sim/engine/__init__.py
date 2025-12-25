"""
Electoral Engine Module

Contains core logic for coalition formation, government stability, and acceleration.
"""

from electoral_sim.engine.coalition import (
    allocate_portfolios_laver_shepsle,
    coalition_strain,
    form_government,
    junior_partner_penalty,
    minimum_connected_winning,
    minimum_winning_coalitions,
)
from electoral_sim.engine.government import (
    GovernmentSimulator,
    collapse_probability,
    cox_proportional_hazard,
    hazard_rate,
    simulate_government_survival,
)
from electoral_sim.engine.numba_accel import (
    NUMBA_AVAILABLE,
    compute_utilities_numba,
    fptp_count_fast,
    vote_mnl_fast,
)

__all__ = [
    # Coalition
    "minimum_winning_coalitions",
    "minimum_connected_winning",
    "coalition_strain",
    "form_government",
    "calculate_coalition_strain",
    "junior_partner_penalty",
    "allocate_portfolios_laver_shepsle",
    "form_coalition_with_utility",
    # Government
    "collapse_probability",
    "simulate_government_survival",
    "hazard_rate",
    "cox_proportional_hazard",
    "GovernmentSimulator",
    # Acceleration
    "vote_mnl_fast",
    "fptp_count_fast",
    "compute_utilities_numba",
    "NUMBA_AVAILABLE",
]
