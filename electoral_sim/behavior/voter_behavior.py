"""Voter Behavior Engine — orchestrates multiple behavior models.

Model classes (ProximityModel, ValenceModel, etc.) live in _models.py
to keep each file under the 250-LOC ceiling.
"""

import numpy as np

from electoral_sim.behavior._models import (  # noqa: F401 — re-exported for backward compatibility
    BehaviorModel,
    ProximityModel,
    RetrospectiveModel,
    SociotropicPocketbookModel,
    StrategicVotingModel,
    ValenceModel,
    WastedVoteModel,
)


class BehaviorEngine:
    """Combines multiple behavior models into a single utility matrix."""

    def __init__(self):
        self.models = []

    def add_model(self, model, weight: float = 1.0):
        """Add a behavior model with its blending weight.

        Args:
            model: Behavior model instance (ProximityModel, ValenceModel, etc.)
            weight: Blending weight for this model's contribution
        """
        self.models.append((model, weight))

    def compute_all(self, voter_data: dict, party_data: dict, **kwargs) -> np.ndarray:
        """
        Compute combined utility matrix from all registered models.

        Args:
            voter_data: Dict with 'n_voters' and voter-specific data
            party_data: Dict with 'n_parties' and party-specific data
            **kwargs: Additional parameters (use_gpu, growth, etc.)

        Returns:
            (n_voters, n_parties) utility matrix
        """
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
