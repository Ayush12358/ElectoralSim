"""
Government Stability and Collapse Models

Implements:
- Sigmoid, Linear, Exponential collapse probability
- Survival time estimation
"""

from typing import Literal

import numpy as np


def collapse_probability(
    time_in_office: int,
    strain: float,
    stability: float,
    model: Literal["sigmoid", "linear", "exponential"] = "sigmoid",
    base_rate: float = 0.05,
    max_term: int = 60,  # months
) -> float:
    """
    Calculate probability of government collapse at given time.

    Args:
        time_in_office: Months since government formation
        strain: Coalition policy strain (0-∞)
        stability: Coalition stability score (0-1)
        model: Collapse model type
        base_rate: Base monthly collapse probability
        max_term: Maximum term length (100% collapse if reached)

    Returns:
        Probability of collapse (0-1)
    """
    # Time factor: increases as term progresses
    time_factor = time_in_office / max_term

    # Strain factor: higher strain = more likely to collapse
    strain_factor = 1.0 + strain

    # Stability factor: inverted (lower stability = more likely)
    instability = 1.0 - stability

    # Combined hazard
    hazard = base_rate * strain_factor * (1.0 + instability)

    if model == "sigmoid":
        # S-curve: slow at start, accelerates, then slows at end
        x = 10 * (time_factor - 0.5)
        probability = hazard / (1.0 + np.exp(-x))

    elif model == "exponential":
        # Exponential growth in collapse risk
        probability = hazard * np.exp(2 * time_factor)

    else:  # linear
        # Linear increase over time
        probability = hazard * (1.0 + time_factor)

    # Force collapse at max term
    if time_in_office >= max_term:
        return 1.0

    return np.clip(probability, 0.0, 1.0)


def simulate_government_survival(
    strain: float,
    stability: float,
    model: Literal["sigmoid", "linear", "exponential"] = "sigmoid",
    max_term: int = 60,
    n_simulations: int = 1000,
    seed: int | None = None,
) -> dict:
    """
    Simulate government survival to get expected duration.

    Args:
        strain: Coalition strain value
        stability: Coalition stability score
        model: Collapse model type
        max_term: Maximum term in months
        n_simulations: Number of Monte Carlo simulations
        seed: Random seed

    Returns:
        Dictionary with survival statistics
    """
    rng = np.random.default_rng(seed)

    survival_times = []

    for _ in range(n_simulations):
        for month in range(1, max_term + 1):
            prob = collapse_probability(month, strain, stability, model, max_term=max_term)
            if rng.random() < prob:
                survival_times.append(month)
                break
        else:
            survival_times.append(max_term)

    survival_times = np.array(survival_times)

    return {
        "mean_survival": float(survival_times.mean()),
        "median_survival": float(np.median(survival_times)),
        "std_survival": float(survival_times.std()),
        "full_term_prob": float((survival_times >= max_term).mean()),
        "early_collapse_prob": float((survival_times < max_term / 2).mean()),
        "min_survival": int(survival_times.min()),
        "max_survival": int(survival_times.max()),
    }


def hazard_rate(
    time_in_office: int,
    events: list[dict] | None = None,
    base_hazard: float = 0.02,
) -> float:
    """
    Calculate instantaneous hazard rate.

    Hazard increases with time and negative events.

    Args:
        time_in_office: Months in office
        events: List of events with {type: str, severity: float}
        base_hazard: Base hazard rate

    Returns:
        Hazard rate (probability per unit time)
    """
    # Time-increasing hazard (bathtub curve - high at start, low middle, high end)
    if time_in_office < 6:
        # Honeymoon period uncertainty
        time_hazard = 0.8
    elif time_in_office < 36:
        # Stable middle period
        time_hazard = 0.5 + 0.01 * (time_in_office - 6)
    else:
        # Late term instability
        time_hazard = 0.8 + 0.02 * (time_in_office - 36)

    # Event effects
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
    """
    Calculate hazard rate using simplified Cox Proportional Hazards model.

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

    # Calculate linear predictor (partial likelihood)
    linear_predictor = 0.0
    for name, value in covariates.items():
        if name in coefficients:
            linear_predictor += coefficients[name] * value

    # Baseline hazard h_0(t) - assumes increasing risk over time (Weibull-like)
    # Shape parameter k=1.5 (increasing risk)
    baseline = base_hazard * (time_in_office**0.5)

    return baseline * np.exp(linear_predictor)


class GovernmentSimulator:
    """
    Simulates government lifecycle.

    Example:
        gov = GovernmentSimulator(strain=0.3, stability=0.7)
        gov.simulate(max_months=60)
        print(gov.summary())
    """

    def __init__(
        self,
        strain: float,
        stability: float,
        coalition_parties: list[str] | None = None,
        model: str = "sigmoid",
        seed: int | None = None,
    ):
        self.strain = strain
        self.stability = stability
        self.coalition = coalition_parties or ["Government"]
        self.model = model
        self.rng = np.random.default_rng(seed)

        self.months_in_office = 0
        self.collapsed = False
        self.collapse_reason: str | None = None
        self.events: list[dict] = []

    def add_event(self, event_type: str, severity: float = 1.0) -> None:
        """Add a destabilizing event."""
        self.events.append(
            {
                "type": event_type,
                "severity": severity,
                "month": self.months_in_office,
            }
        )

    def step(self) -> bool:
        """
        Advance one month. Returns True if government survives.
        """
        if self.collapsed:
            return False

        self.months_in_office += 1

        prob = collapse_probability(
            self.months_in_office,
            self.strain,
            self.stability,
            model=self.model,
        )

        # Adjust for recent events (within last 3 months)
        recent_events = [
            e
            for e in self.events
            if e["month"] >= self.months_in_office - 3 and e["month"] <= self.months_in_office
        ]
        if recent_events:
            event_boost = sum(e["severity"] * 0.1 for e in recent_events)
            prob = min(1.0, prob + event_boost)

        if self.rng.random() < prob:
            self.collapsed = True
            self.collapse_reason = "policy_strain" if self.strain > 0.5 else "time_in_office"
            return False

        return True

    def simulate(self, max_months: int = 60) -> int:
        """Run simulation until collapse or max_months. Returns survival time."""
        while self.months_in_office < max_months and self.step():
            pass
        return self.months_in_office

    def summary(self) -> dict:
        """Get simulation summary."""
        return {
            "coalition": self.coalition,
            "months_in_office": self.months_in_office,
            "collapsed": self.collapsed,
            "collapse_reason": self.collapse_reason,
            "strain": self.strain,
            "stability": self.stability,
            "n_events": len(self.events),
        }
