"""Tests for voter behavior models and party strategy."""

import pytest
import numpy as np


class TestBehaviorModels:
    """All 6 behavior model classes + BehaviorEngine composition."""

    def test_proximity_model_creation(self):
        from electoral_sim import ProximityModel

        model = ProximityModel()
        assert model is not None

    def test_proximity_custom_weight(self):
        from electoral_sim import ProximityModel

        model = ProximityModel(weight=2.0)
        assert model.weight == 2.0

    def test_proximity_utility_shape(self):
        from electoral_sim import ProximityModel

        model = ProximityModel()
        voter_pos = np.random.normal(0, 0.3, (100, 2))
        party_pos = np.array([[-0.5, -0.2], [0.3, 0.1], [0.0, 0.3]])
        u = model.compute_utility(voter_pos, party_pos)
        assert u.shape == (100, 3)
        # Closer parties should have higher utility (less negative)
        assert u[:, 0].mean() < 0  # All distances are negative

    def test_valence_model_creation(self):
        from electoral_sim import ValenceModel

        model = ValenceModel()
        assert model is not None

    def test_valence_custom_weight(self):
        from electoral_sim import ValenceModel

        model = ValenceModel(weight=0.5)
        assert model.weight == 0.5

    def test_valence_utility_shape(self):
        from electoral_sim import ValenceModel

        model = ValenceModel(weight=0.01)
        valence = np.array([50.0, 60.0, 40.0])
        u = model.compute_utility(100, valence)
        assert u.shape == (100, 3)
        # Higher valence → higher utility
        assert u[0, 1] > u[0, 2]

    def test_retrospective_model_creation(self):
        from electoral_sim import RetrospectiveModel

        model = RetrospectiveModel()
        assert model is not None

    def test_retrospective_incumbent_bonus(self):
        from electoral_sim import RetrospectiveModel

        model = RetrospectiveModel(weight=0.5)
        incumbents = np.array([True, False, False])
        # Positive growth → bonus to incumbent
        u = model.compute_utility(100, 3, incumbents, economic_growth=0.03)
        assert u[:, 0].mean() > 0  # Incumbent gets positive utility
        assert u[:, 1].mean() == 0  # Non-incumbents get zero

    def test_retrospective_negative_growth(self):
        from electoral_sim import RetrospectiveModel

        model = RetrospectiveModel(weight=0.5)
        incumbents = np.array([True, False])
        u = model.compute_utility(100, 2, incumbents, economic_growth=-0.05)
        assert u[:, 0].mean() < 0  # Incumbent gets penalty

    def test_strategic_voting_model_creation(self):
        from electoral_sim import StrategicVotingModel

        model = StrategicVotingModel()
        assert model is not None

    def test_strategic_low_viability_penalty(self):
        from electoral_sim import StrategicVotingModel

        model = StrategicVotingModel(sensitivity=2.0)
        viability = np.array([0.5, 0.01, 0.3])
        u = model.compute_utility(100, viability)
        assert u.shape == (100, 3)
        # Low viability party (0.01) gets biggest penalty
        assert u[0, 1] < u[0, 0]

    def test_sociotropic_pocketbook_model(self):
        from electoral_sim import SociotropicPocketbookModel

        model = SociotropicPocketbookModel()
        incumbents = np.array([True, False])
        u = model.compute_utility(100, 2, incumbents, economic_growth=0.02)
        assert u.shape == (100, 2)
        # With default sociotropic weighting, incumbent gets positive utility
        assert u[:, 0].mean() > 0

    def test_sociotropic_with_perception_type(self):
        from electoral_sim import SociotropicPocketbookModel

        model = SociotropicPocketbookModel()
        incumbents = np.array([True, False])
        perception = np.array([0.8, 0.3])  # voter 0: sociotropic, voter 1: pocketbook
        u = model.compute_utility(
            2, 2, incumbents,
            economic_growth=0.02,
            personal_income_change=np.array([0.01, 0.05]),
            perception_type=perception,
        )
        assert u.shape == (2, 2)

    def test_wasted_vote_model(self):
        from electoral_sim import WastedVoteModel

        model = WastedVoteModel(penalty=3.0, viability_threshold=0.1)
        viability = np.array([0.5, 0.05, 0.3])
        u = model.compute_utility(100, viability)
        assert u.shape == (100, 3)
        # Party below threshold (0.05 < 0.1) gets penalty
        assert u[0, 1] < 0
        # Party above threshold gets no penalty
        assert u[0, 0] == 0


class TestBehaviorEngine:
    """BehaviorEngine composition and dispatch."""

    def test_engine_creation(self):
        from electoral_sim import BehaviorEngine

        engine = BehaviorEngine()
        assert len(engine.models) == 0

    def test_engine_add_model(self):
        from electoral_sim import BehaviorEngine, ProximityModel

        engine = BehaviorEngine()
        engine.add_model(ProximityModel(weight=1.0))
        assert len(engine.models) == 1

    def test_engine_compute_utilities(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=100, seed=42)
        results = model.run_election()
        assert results is not None


class TestPartyStrategy:
    """Adaptive party strategy tests."""

    def test_random_walk_strategy(self):
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame({
            "name": ["A", "B"],
            "position_x": [0.0, 0.5],
            "position_y": [0.0, -0.3],
        })
        voters_df = pl.DataFrame({
            "ideology_x": np.random.normal(0, 0.3, 100),
            "ideology_y": np.random.normal(0, 0.3, 100),
        })
        new_df = adaptive_strategy_step(parties_df, voters_df, strategy="random_walk", learning_rate=0.1)
        # Positions should have changed slightly
        assert abs(new_df["position_x"][0] - 0.0) > 0 or abs(new_df["position_x"][1] - 0.5) > 0

    def test_median_voter_strategy(self):
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame({
            "name": ["A"],
            "position_x": [-1.0],
            "position_y": [0.0],
        })
        voters_df = pl.DataFrame({
            "ideology_x": np.ones(100) * 0.5,
            "ideology_y": np.zeros(100),
        })
        new_df = adaptive_strategy_step(parties_df, voters_df, strategy="median_voter", learning_rate=0.5)
        # Party should move right, toward the median
        assert new_df["position_x"][0] > -1.0

    def test_position_clipping(self):
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame({
            "name": ["A"],
            "position_x": [0.99],
            "position_y": [0.99],
        })
        voters_df = pl.DataFrame({
            "ideology_x": np.ones(20) * 2.0,
            "ideology_y": np.ones(20) * 2.0,
        })
        new_df = adaptive_strategy_step(parties_df, voters_df, strategy="median_voter", learning_rate=0.5)
        assert -1.0 <= new_df["position_x"][0] <= 1.0
        assert -1.0 <= new_df["position_y"][0] <= 1.0

    def test_missing_position_x_returns_unchanged(self):
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame({"name": ["A", "B"]})
        voters_df = pl.DataFrame({"ideology_x": [0.0]})
        result = adaptive_strategy_step(parties_df, voters_df)
        assert result is parties_df
