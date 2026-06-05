# Copyright 2025-2026 Ayush Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


from electoral_sim.engine._hazards import (  # noqa: E402, F401
    cox_proportional_hazard,
    hazard_rate,
)
