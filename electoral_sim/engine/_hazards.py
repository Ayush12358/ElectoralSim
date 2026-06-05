"""Hazard rate models for government collapse.

Extracted from government.py to keep each file under the 250-LOC ceiling.
"""

import numpy as np


def hazard_rate(
    time_in_office: int,
    events: list[dict] | None = None,
    base_hazard: float = 0.02,
) -> float:
    """Calculate instantaneous hazard rate.

    Hazard increases with time and negative events.

    Args:
        time_in_office: Months in office
        events: List of events with {type: str, severity: float}
        base_hazard: Base hazard rate

    Returns:
        Hazard rate (probability per unit time)
    """
    if time_in_office < 6:
        time_hazard = 0.8
    elif time_in_office < 36:
        time_hazard = 0.5 + 0.01 * (time_in_office - 6)
    else:
        time_hazard = 0.8 + 0.02 * (time_in_office - 36)

    event_hazard = 0.0
    if events:
        event_weights = {
            "scandal": 0.3,
            "economic_crisis": 0.4,
            "defection": 0.5,
            "vote_of_no_confidence": 0.8,
            "leadership_challenge": 0.3,
        }
        for event in events:
            event_type = event.get("type", "other")
            severity = event.get("severity", 1.0)
            weight = event_weights.get(event_type, 0.1)
            event_hazard += weight * severity

    return base_hazard * time_hazard * (1.0 + event_hazard)


def cox_proportional_hazard(
    time_in_office: int,
    covariates: dict[str, float],
    base_hazard: float = 0.01,
    coefficients: dict[str, float] | None = None,
) -> float:
    """Calculate hazard rate using simplified Cox Proportional Hazards model.

    h(t|x) = h_0(t) * exp(sum(b_i * x_i))

    Args:
        time_in_office: T (baseline hazard increases with time)
        covariates: Dictionary of covariate values (x)
        base_hazard: Base hazard scalar
        coefficients: Dictionary of regression coefficients (b)

    Returns:
        Hazard rate at time t given covariates x

    Default Coefficients (based on Warwick 1994):
        - majority_margin: -2.0 (larger majority = safer)
        - coalition_strain: +1.5 (more strain = riskier)
        - n_parties: +0.2 (more parties = slightly riskier)
        - economic_growth: -0.5 (growth = safer)
    """
    if coefficients is None:
        coefficients = {
            "majority_margin": -2.0,
            "coalition_strain": 1.5,
            "n_parties": 0.2,
            "economic_growth": -0.5,
            "polarization": 1.0,
        }

    linear_predictor = 0.0
    for name, value in covariates.items():
        if name in coefficients:
            linear_predictor += coefficients[name] * value

    baseline = base_hazard * (time_in_office**0.5)
    return baseline * np.exp(linear_predictor)
