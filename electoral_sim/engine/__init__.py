"""
Electoral Engine Module

Contains core logic for coalition formation, government stability, and acceleration.
"""

from electoral_sim.engine.coalition import (
    minimum_winning_coalitions,
    minimum_connected_winning,
    coalition_strain,
    form_government,
    junior_partner_penalty,
    allocate_portfolios_laver_shepsle,
)

from electoral_sim.engine.government import (
    collapse_probability,
    simulate_government_survival,
    hazard_rate,
    cox_proportional_hazard,
    GovernmentSimulator,
)

from electoral_sim.engine.numba_accel import (
    vote_mnl_fast,
    fptp_count_fast,
    compute_utilities_numba,
    NUMBA_AVAILABLE,
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
