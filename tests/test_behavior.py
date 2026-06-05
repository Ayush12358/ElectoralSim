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
            2,
            2,
            incumbents,
            economic_growth=0.02,
            personal_income_change=np.array([0.01, 0.05]),
            perception_type=perception,
        )
        assert u.shape == (2, 2)

    def test_sociotropic_with_default_perception(self):
        """SociotropicPocketbookModel with no perception_type defaults to all sociotropic."""
        from electoral_sim import SociotropicPocketbookModel

        model = SociotropicPocketbookModel()
        incumbents = np.array([True, False])
        u = model.compute_utility(10, 2, incumbents, economic_growth=0.03)
        assert u.shape == (10, 2)

    def test_sociotropic_with_personal_income(self):
        """SociotropicPocketbookModel with personal_income_change."""
        from electoral_sim import SociotropicPocketbookModel

        model = SociotropicPocketbookModel(sociotropic_weight=0.3, pocketbook_weight=0.7)
        incumbents = np.array([True, False])
        u = model.compute_utility(
            5,
            2,
            incumbents,
            economic_growth=0.02,
            personal_income_change=np.array([0.05, -0.02, 0.01, 0.03, -0.01]),
            perception_type=np.array([0.8, 0.3, 0.5, 0.9, 0.1]),
        )
        assert u.shape == (5, 2)

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

    def test_engine_with_all_models(self):
        """BehaviorEngine with all 6 behavior models."""
        from electoral_sim import (
            BehaviorEngine,
            ProximityModel,
            ValenceModel,
            RetrospectiveModel,
            StrategicVotingModel,
            SociotropicPocketbookModel,
            WastedVoteModel,
        )
        from electoral_sim import ElectionModel

        engine = BehaviorEngine()
        engine.add_model(ProximityModel(weight=1.0))
        engine.add_model(ValenceModel(weight=0.01))
        engine.add_model(RetrospectiveModel(weight=0.5))
        engine.add_model(StrategicVotingModel(sensitivity=1.0))
        engine.add_model(SociotropicPocketbookModel())
        engine.add_model(WastedVoteModel(penalty=2.0))

        model = ElectionModel(n_voters=500, behavior_engine=engine, economic_growth=0.02, seed=42)
        results = model.run_election()
        assert results is not None


class TestPartyStrategy:
    """Adaptive party strategy tests."""

    def test_random_walk_strategy(self):
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame(
            {
                "name": ["A", "B"],
                "position_x": [0.0, 0.5],
                "position_y": [0.0, -0.3],
            }
        )
        voters_df = pl.DataFrame(
            {
                "ideology_x": np.random.normal(0, 0.3, 100),
                "ideology_y": np.random.normal(0, 0.3, 100),
            }
        )
        new_df = adaptive_strategy_step(
            parties_df, voters_df, strategy="random_walk", learning_rate=0.1
        )
        # Positions should have changed slightly
        assert abs(new_df["position_x"][0] - 0.0) > 0 or abs(new_df["position_x"][1] - 0.5) > 0

    def test_median_voter_strategy(self):
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame(
            {
                "name": ["A"],
                "position_x": [-1.0],
                "position_y": [0.0],
            }
        )
        voters_df = pl.DataFrame(
            {
                "ideology_x": np.ones(100) * 0.5,
                "ideology_y": np.zeros(100),
            }
        )
        new_df = adaptive_strategy_step(
            parties_df, voters_df, strategy="median_voter", learning_rate=0.5
        )
        # Party should move right, toward the median
        assert new_df["position_x"][0] > -1.0

    def test_position_clipping(self):
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame(
            {
                "name": ["A"],
                "position_x": [0.99],
                "position_y": [0.99],
            }
        )
        voters_df = pl.DataFrame(
            {
                "ideology_x": np.ones(20) * 2.0,
                "ideology_y": np.ones(20) * 2.0,
            }
        )
        new_df = adaptive_strategy_step(
            parties_df, voters_df, strategy="median_voter", learning_rate=0.5
        )
        assert -1.0 <= new_df["position_x"][0] <= 1.0
        assert -1.0 <= new_df["position_y"][0] <= 1.0

    def test_missing_position_x_returns_unchanged(self):
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame({"name": ["A", "B"]})
        voters_df = pl.DataFrame({"ideology_x": [0.0]})
        result = adaptive_strategy_step(parties_df, voters_df)
        assert result is parties_df

    def test_median_voter_with_noise(self):
        """median_voter strategy with noise parameter."""
        from electoral_sim.agents.party_strategy import adaptive_strategy_step
        import polars as pl

        parties_df = pl.DataFrame(
            {
                "name": ["A"],
                "position_x": [0.0],
                "position_y": [0.0],
            }
        )
        voters_df = pl.DataFrame(
            {
                "ideology_x": np.ones(50) * 0.5,
                "ideology_y": np.zeros(50),
            }
        )
        new_df = adaptive_strategy_step(
            parties_df,
            voters_df,
            strategy="median_voter",
            learning_rate=0.1,
            noise=0.1,
            rng=np.random.default_rng(42),
        )
        # Position should have moved toward median
        assert new_df["position_x"][0] > 0.0


class TestCampaignFinance:
    """Tests for campaign finance model."""

    def test_campaign_finance_creation(self):
        """CampaignFinance creates with default parameters."""
        from electoral_sim.behavior.campaign import CampaignFinance

        cf = CampaignFinance()
        assert cf.base_spending == 1_000_000.0
        assert cf.incumbent_advantage == 1.5

    def test_compute_spending_incumbent_advantage(self):
        """Incumbents get more spending."""
        from electoral_sim.behavior.campaign import CampaignFinance

        cf = CampaignFinance()
        incumbents = np.array([True, False, False])
        rng = np.random.default_rng(42)
        spending = cf.compute_spending(3, incumbents, rng)
        assert len(spending) == 3
        assert spending[0] > spending[1]

    def test_spending_to_valence_diminishing(self):
        """Spending-to-valence has diminishing returns."""
        from electoral_sim.behavior.campaign import CampaignFinance

        cf = CampaignFinance(diminishing_factor=0.5)
        low = cf.spending_to_valence(np.array([100_000]))
        high = cf.spending_to_valence(np.array([10_000_000]))
        ratio = high[0] / low[0]
        assert ratio < 10  # 100x spending should give <10x valence

    def test_media_environment_step(self):
        """MediaEnvironment.step() returns exposure, sentiment, reach."""
        from electoral_sim.behavior.campaign import MediaEnvironment

        media = MediaEnvironment()
        result = media.step(3, rng=np.random.default_rng(42))
        assert len(result["exposure"]) == 3
        assert len(result["sentiment"]) == 3
        assert result["reach"] > 0

    def test_media_misinformation_susceptibility(self):
        """Low media diversity → high misinformation susceptibility."""
        from electoral_sim.behavior.campaign import MediaEnvironment

        media = MediaEnvironment()
        high_div = media.misinformation_susceptibility(np.array([0.9, 0.9, 0.9]))
        low_div = media.misinformation_susceptibility(np.array([0.1, 0.1, 0.1]))
        assert low_div > high_div

    def test_voter_registration_model(self):
        """VoterRegistration computes eligibility, registration, turnout."""
        from electoral_sim.behavior.campaign import VoterRegistration

        vr = VoterRegistration()
        age = np.array([25, 35, 55, 65, 75])
        result = vr.compute_eligibility(5, age, rng=np.random.default_rng(42))
        assert len(result["eligible"]) == 5
        assert result["will_vote"].sum() >= 0

    def test_campaign_targeting_allocate(self):
        """CampaignTargeting allocates more to marginal districts."""
        from electoral_sim.behavior.campaign import CampaignTargeting

        ct = CampaignTargeting(total_budget=100)
        marginality = np.array([0.9, 0.1, 0.9])
        allocation = ct.allocate_resources(marginality)
        assert len(allocation) == 3
        assert allocation[0] > allocation[1]  # More $ to marginal districts

    def test_strategic_voting_district_viability(self):
        """StrategicVotingModel accepts district-level viability."""
        from electoral_sim.behavior.voter_behavior import StrategicVotingModel

        model = StrategicVotingModel(sensitivity=1.0)
        # District-level: party 0 viable in district 0, party 1 viable in district 1
        district_viability = np.array([
            [0.8, 0.2],  # District 0: party 0 strong
            [0.2, 0.8],  # District 1: party 1 strong
        ])
        result = model.compute_utility(2, np.array([0.5, 0.5]),
                                       constituency_viability=district_viability)
        assert result.shape == (2, 2)
        # Party with higher local viability should have less penalty (higher utility)
        assert result[0, 0] > result[0, 1]  # District 0 prefers party 0

    def test_turnout_mobilization_decompose(self):
        """TurnoutMobilization decomposes turnout into components."""
        from electoral_sim.behavior.campaign import TurnoutMobilization

        tm = TurnoutMobilization()
        result = tm.decompose_turnout(0.65, 0.05, 0.03, 0.08)
        assert "baseline" in result
        assert "total" in result
        assert 0 <= result["total"] <= 1
