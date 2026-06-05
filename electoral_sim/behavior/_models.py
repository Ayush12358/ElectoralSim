"""Voter behavior model classes — standalone utility computation components.

Extracted from voter_behavior.py to keep each file under the 250-LOC ceiling.
BehaviorEngine (the orchestrator) remains in voter_behavior.py.
"""

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class BehaviorModel(Protocol):
    """Protocol for voting behavior components."""

    def compute_utility(self, voters, parties, **kwargs) -> np.ndarray: ...


class ProximityModel:
    """Standard spatial model: utility decreases with ideological distance.

    Required party fields: positions (n_parties, dims)
    Required voter fields: positions (n_voters, dims)
    """

    model_name = "proximity"

    def __init__(self, weight: float = 1.0, dimensionality: int = 2):
        self.weight = weight
        self.dimensionality = dimensionality

    def compute_utility(
        self, voter_positions: np.ndarray, party_positions: np.ndarray, **kwargs
    ) -> np.ndarray:
        diff = voter_positions[:, np.newaxis, :] - party_positions[np.newaxis, :, :]
        dist = np.linalg.norm(diff, axis=2)
        return -self.weight * dist


class ValenceModel:
    """Valence model: utility increases with party's non-policy appeal.

    Required party fields: valence (n_parties,)
    """

    model_name = "valence"

    def __init__(self, weight: float = 0.01):
        self.weight = weight

    def compute_utility(self, n_voters: int, valence: np.ndarray, **kwargs) -> np.ndarray:
        return np.tile(self.weight * valence, (n_voters, 1))


class RetrospectiveModel:
    """Economic/Retrospective voting: reward/punish incumbents based on 'economic mood'.

    Required party fields: incumbent_mask (n_parties,) boolean
    Required kwargs: economic_growth (float)
    """

    model_name = "retrospective"

    def __init__(self, weight: float = 0.5):
        self.weight = weight

    def compute_utility(
        self,
        n_voters: int,
        n_parties: int,
        incumbent_mask: np.ndarray,
        economic_growth: float,
        **kwargs,
    ) -> np.ndarray:
        utility = np.zeros((n_voters, n_parties))
        reward = self.weight * economic_growth
        utility[:, incumbent_mask] = reward
        return utility


class StrategicVotingModel:
    """Strategic voting: voters discount candidates seen as unviable (Duverger's Law)."""

    model_name = "strategic"

    def __init__(self, sensitivity: float = 1.0):
        self.sensitivity = sensitivity

    def compute_utility(self, n_voters: int, viability: np.ndarray, **kwargs) -> np.ndarray:
        district_viability = kwargs.get("constituency_viability")
        if district_viability is not None:
            penalty = self.sensitivity * np.log(district_viability + 1e-6)
        else:
            penalty = self.sensitivity * np.log(viability + 1e-6)
            penalty = np.tile(penalty, (n_voters, 1))
        return penalty


class SociotropicPocketbookModel:
    """Economic voting with sociotropic vs pocketbook distinction.

    - Sociotropic: Voters evaluate based on NATIONAL economic conditions
    - Pocketbook: Voters evaluate based on PERSONAL financial situation
    """

    model_name = "sociotropic_pocketbook"

    def __init__(self, sociotropic_weight: float = 0.5, pocketbook_weight: float = 0.5):
        self.sociotropic_weight = sociotropic_weight
        self.pocketbook_weight = pocketbook_weight

    def compute_utility(
        self,
        n_voters: int,
        n_parties: int,
        incumbent_mask: np.ndarray,
        economic_growth: float,
        personal_income_change: np.ndarray | None = None,
        perception_type: np.ndarray | None = None,
        **kwargs,
    ) -> np.ndarray:
        utility = np.zeros((n_voters, n_parties))

        if perception_type is None:
            perception_type = np.ones(n_voters)
        if personal_income_change is None:
            personal_income_change = np.zeros(n_voters)

        sociotropic_effect = self.sociotropic_weight * economic_growth * perception_type
        pocketbook_effect = self.pocketbook_weight * personal_income_change * (1 - perception_type)

        total_effect = sociotropic_effect + pocketbook_effect
        utility[:, incumbent_mask] = total_effect[:, np.newaxis]
        return utility


class WastedVoteModel:
    """Tactical voting based on fear of wasting vote.

    Voters penalize parties they perceive as having no chance of winning.
    """

    model_name = "wasted_vote"

    def __init__(self, penalty: float = 2.0, viability_threshold: float = 0.05):
        self.penalty = penalty
        self.viability_threshold = viability_threshold

    def compute_utility(self, n_voters: int, viability: np.ndarray, **kwargs) -> np.ndarray:
        is_wasted = viability < self.viability_threshold
        penalty_vec = np.where(is_wasted, -self.penalty, 0.0)
        return np.tile(penalty_vec, (n_voters, 1))
