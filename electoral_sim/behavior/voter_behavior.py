"""
Voter Behavior Models

Implements different factors that influence voter utility and choice.
Modular and pluggable.
"""

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class BehaviorModel(Protocol):
    """Protocol for voting behavior components."""

    def compute_utility(self, voters, parties, **kwargs) -> np.ndarray: ...


class ProximityModel:
    """Standard spatial model: utility decreases with ideological distance."""

    def __init__(self, weight: float = 1.0, dimensionality: int = 2):
        self.weight = weight
        self.dimensionality = dimensionality

    def compute_utility(
        self, voter_positions: np.ndarray, party_positions: np.ndarray, **kwargs
    ) -> np.ndarray:
        """
        Args:
            voter_positions: (n_voters, dims)
            party_positions: (n_parties, dims)
        Returns:
            (n_voters, n_parties) utility matrix
        """
        # (n_voters, 1, dims) - (1, n_parties, dims) -> (n_voters, n_parties, dims)
        diff = voter_positions[:, np.newaxis, :] - party_positions[np.newaxis, :, :]
        dist = np.linalg.norm(diff, axis=2)
        return -self.weight * dist


class ValenceModel:
    """Valence model: utility increases with party's non-policy appeal."""

    def __init__(self, weight: float = 0.01):
        self.weight = weight

    def compute_utility(self, n_voters: int, valence: np.ndarray, **kwargs) -> np.ndarray:
        """
        Args:
            n_voters: Number of voters
            valence: (n_parties,) valence scores
        Returns:
            (n_voters, n_parties) utility matrix
        """
        return np.tile(self.weight * valence, (n_voters, 1))


class RetrospectiveModel:
    """Economic/Retrospective voting: reward/punish incumbents based on 'economic mood'."""

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
        """
        Args:
            incumbent_mask: bool array (n_parties,)
            economic_growth: Current growth rate (can be voter-specific or global)
        """
        utility = np.zeros((n_voters, n_parties))
        # Logic: If growth > 0, bonus to incumbents. If growth < 0, penalty.
        # Here we assume a simple global growth for now
        reward = self.weight * economic_growth
        utility[:, incumbent_mask] = reward
        return utility


class StrategicVotingModel:
    """Strategic voting: voters discount candidates seen as unviable (Duverger's Law)."""

    def __init__(self, sensitivity: float = 1.0):
        self.sensitivity = sensitivity

    def compute_utility(self, n_voters: int, viability: np.ndarray, **kwargs) -> np.ndarray:
        """
        Args:
            viability: (n_parties,) estimated probability of winning or 'expected vote share'
        """
        # Penalty for low viability
        penalty = self.sensitivity * (np.log(viability + 1e-6))
        return np.tile(penalty, (n_voters, 1))


class SociotropicPocketbookModel:
    """
    Economic voting with sociotropic vs pocketbook distinction.

    - Sociotropic: Voters evaluate based on NATIONAL economic conditions
    - Pocketbook: Voters evaluate based on PERSONAL financial situation

    Research shows higher-educated voters tend to be more sociotropic.
    """

    def __init__(self, sociotropic_weight: float = 0.5, pocketbook_weight: float = 0.5):
        self.sociotropic_weight = sociotropic_weight
        self.pocketbook_weight = pocketbook_weight

    def compute_utility(
        self,
        n_voters: int,
        n_parties: int,
        incumbent_mask: np.ndarray,
        economic_growth: float,  # National (sociotropic signal)
        personal_income_change: np.ndarray | None = None,  # Individual (pocketbook)
        perception_type: np.ndarray | None = None,  # 0=pocketbook, 1=sociotropic
        **kwargs,
    ) -> np.ndarray:
        """
        Args:
            economic_growth: National GDP growth rate
            personal_income_change: (n_voters,) individual income change
            perception_type: (n_voters,) 0=pocketbook, 1=sociotropic (or blend)
        """
        utility = np.zeros((n_voters, n_parties))

        # Default: everyone uses national (sociotropic)
        if perception_type is None:
            perception_type = np.ones(n_voters)
        if personal_income_change is None:
            personal_income_change = np.zeros(n_voters)

        # Blend sociotropic and pocketbook evaluations
        sociotropic_effect = self.sociotropic_weight * economic_growth * perception_type
        pocketbook_effect = self.pocketbook_weight * personal_income_change * (1 - perception_type)

        total_effect = sociotropic_effect + pocketbook_effect

        # Apply to incumbents
        utility[:, incumbent_mask] = total_effect[:, np.newaxis]

        return utility


class WastedVoteModel:
    """
    Tactical voting based on fear of wasting vote.

    Voters penalize parties they perceive as having no chance of winning.
    Threshold-based: parties below viability threshold get a fixed penalty.
    This is a simpler, more direct version of strategic voting.
    """

    def __init__(self, penalty: float = 2.0, viability_threshold: float = 0.05):
        self.penalty = penalty
        self.viability_threshold = viability_threshold

    def compute_utility(self, n_voters: int, viability: np.ndarray, **kwargs) -> np.ndarray:
        """
        Args:
            viability: (n_parties,) expected vote share or probability of winning
        """
        # Binary penalty: below threshold → wasted vote
        is_wasted = viability < self.viability_threshold
        penalty_vec = np.where(is_wasted, -self.penalty, 0.0)
        return np.tile(penalty_vec, (n_voters, 1))


class BehaviorEngine:
    """Combines multiple behavior models into a single utility matrix."""

    def __init__(self):
        self.models = []

    def add_model(self, model, weight: float = 1.0):
        self.models.append((model, weight))

    def compute_all(self, voter_data: dict, party_data: dict, **kwargs) -> np.ndarray:
        n_voters = voter_data["n_voters"]
        n_parties = party_data["n_parties"]
        use_gpu = kwargs.get("use_gpu", False)

        if use_gpu:
            import cupy as cp

            total_utility = cp.zeros((n_voters, n_parties), dtype=cp.float32)

            # Convert basic data to GPU
            v_pos = cp.asarray(voter_data["positions"], dtype=cp.float32)
            p_pos = cp.asarray(party_data["positions"], dtype=cp.float32)
            valence = cp.asarray(party_data["valence"], dtype=cp.float32)
            incumbents = cp.asarray(party_data["incumbents"], dtype=bool)

            for model, w in self.models:
                if isinstance(model, ProximityModel):
                    # Optimized proximity on GPU
                    diff = v_pos[:, cp.newaxis, :] - p_pos[cp.newaxis, :, :]
                    u = -model.weight * cp.sqrt(cp.sum(diff**2, axis=2))
                elif isinstance(model, ValenceModel):
                    u = model.weight * valence[cp.newaxis, :]
                elif isinstance(model, RetrospectiveModel):
                    reward = model.weight * kwargs.get("growth", 0.0)
                    u = cp.zeros((n_voters, n_parties), dtype=cp.float32)
                    u[:, incumbents] = reward
                else:
                    # Fallback to CPU for specialized models if not GPU-ready
                    # (This part is tricky, we'll assume models return NumPy and we convert)
                    u_cpu = model.compute_utility(voter_data, party_data, **kwargs)
                    u = cp.asarray(u_cpu, dtype=cp.float32)

                total_utility += w * u

            return cp.asnumpy(total_utility)

        else:
            total_utility = np.zeros((n_voters, n_parties))

            for model, w in self.models:
                if isinstance(model, ProximityModel):
                    u = model.compute_utility(voter_data["positions"], party_data["positions"])
                elif isinstance(model, ValenceModel):
                    u = model.compute_utility(n_voters, party_data["valence"])
                elif isinstance(model, RetrospectiveModel):
                    u = model.compute_utility(
                        n_voters, n_parties, party_data["incumbents"], kwargs.get("growth", 0.0)
                    )
                elif isinstance(model, StrategicVotingModel):
                    # Strategic voting: needs viability scores
                    viability = party_data.get("viability")
                    if viability is None:
                        viability = kwargs.get("viability")
                    if viability is None:
                        viability = np.ones(n_parties) / n_parties  # Default: equal viability
                    u = model.compute_utility(n_voters, viability)
                elif isinstance(model, WastedVoteModel):
                    # Wasted vote model: needs viability scores
                    viability = party_data.get("viability")
                    if viability is None:
                        viability = kwargs.get("viability")
                    if viability is None:
                        viability = np.ones(n_parties) / n_parties  # Default: equal viability
                    u = model.compute_utility(n_voters, viability)
                elif isinstance(model, SociotropicPocketbookModel):
                    # Economic voting with sociotropic/pocketbook distinction
                    voter_df = voter_data.get("df")
                    perception_type = None
                    if (
                        voter_df is not None
                        and hasattr(voter_df, "columns")
                        and "economic_perception" in voter_df.columns
                    ):
                        perception_type = voter_df["economic_perception"].to_numpy()
                    u = model.compute_utility(
                        n_voters,
                        n_parties,
                        party_data["incumbents"],
                        economic_growth=kwargs.get("growth", 0.0),
                        personal_income_change=voter_data.get("personal_income_change"),
                        perception_type=perception_type,
                    )
                else:
                    # Generic fallback - try to call with standard args
                    try:
                        u = model.compute_utility(n_voters, n_parties, **kwargs)
                    except TypeError:
                        # If that fails, try minimal interface
                        u = np.zeros((n_voters, n_parties))

                total_utility += w * u

            return total_utility
