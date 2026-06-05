"""Campaign model classes — voter registration, targeting, mobilization, access.

Extracted from campaign.py to keep each file under the 250-LOC ceiling.
CampaignFinance and MediaEnvironment remain in campaign.py.
"""

from __future__ import annotations

import numpy as np


class VoterRegistration:
    """Voter registration and eligibility model.

    Models eligible population, registration status, turnout probability,
    age/citizenship constraints, and registration deadlines.
    """

    def __init__(
        self,
        eligible_rate: float = 0.85,
        registration_rate: float = 0.75,
        base_turnout: float = 0.65,
        age_effect: float = 0.1,
    ):
        self.eligible_rate = eligible_rate
        self.registration_rate = registration_rate
        self.base_turnout = base_turnout
        self.age_effect = age_effect

    def compute_eligibility(
        self,
        n_voters: int,
        age: np.ndarray | None = None,
        rng: np.random.Generator | None = None,
    ) -> dict[str, np.ndarray]:
        if rng is None:
            rng = np.random.default_rng()

        eligible = rng.random(n_voters) < self.eligible_rate
        registered = eligible & (rng.random(n_voters) < self.registration_rate)

        turnout_prob = np.full(n_voters, self.base_turnout)
        if age is not None:
            age_norm = (age - np.median(age)) / 10.0
            turnout_prob += self.age_effect * age_norm
        turnout_prob = np.clip(turnout_prob, 0.0, 1.0)

        will_vote = registered & (rng.random(n_voters) < turnout_prob)

        return {
            "eligible": eligible,
            "registered": registered,
            "will_vote": will_vote,
        }


class CampaignTargeting:
    """Local campaign targeting: parties allocate resources across
    constituencies based on marginal-seat value with budget constraints
    and diminishing returns on persuasion.
    """

    def __init__(
        self,
        total_budget: float = 100.0,
        marginal_weight: float = 0.7,
        persuasion_decay: float = 0.5,
    ):
        self.total_budget = total_budget
        self.marginal_weight = marginal_weight
        self.persuasion_decay = persuasion_decay

    def allocate_resources(
        self,
        marginality: np.ndarray,
    ) -> np.ndarray:
        weights = self.marginal_weight * marginality + (1 - self.marginal_weight) * 0.5
        weights = weights / weights.sum()
        return self.total_budget * weights

    def persuasion_effect(
        self,
        spending: np.ndarray,
    ) -> np.ndarray:
        return (spending**self.persuasion_decay) * 0.01


class TurnoutMobilization:
    """Turnout mobilization: models canvassing, GOTV, persuasion vs
    mobilization, targeted demographics, and resource allocation.
    """

    def __init__(
        self,
        base_turnout: float = 0.65,
        canvass_effect: float = 0.05,
        mobilization_effect: float = 0.08,
    ):
        self.base_turnout = base_turnout
        self.canvass_effect = canvass_effect
        self.mobilization_effect = mobilization_effect

    def decompose_turnout(
        self,
        baseline: float,
        alienation: float,
        indifference: float,
        mobilization: float,
    ) -> dict[str, float]:
        return {
            "baseline": baseline,
            "alienation_effect": -alienation,
            "indifference_effect": -indifference,
            "mobilization_effect": mobilization,
            "total": max(0.0, min(1.0, baseline - alienation - indifference + mobilization)),
        }


class PollingAccess:
    """Polling-place accessibility model: distance, wait time, opening
    hours, and registration friction effects on turnout.
    """

    def __init__(
        self,
        distance_decay: float = 0.1,
        wait_penalty: float = 0.05,
        registration_friction: float = 0.02,
    ):
        self.distance_decay = distance_decay
        self.wait_penalty = wait_penalty
        self.registration_friction = registration_friction

    def compute_turnout_adjustment(
        self,
        distances: np.ndarray,
        wait_times: np.ndarray | None = None,
        base_turnout: float = 0.65,
    ) -> np.ndarray:
        result = np.full(len(distances), base_turnout, dtype=float)
        result -= self.distance_decay * distances
        result -= self.registration_friction
        if wait_times is not None:
            result -= self.wait_penalty * wait_times
        return np.clip(result, 0.0, 1.0)
