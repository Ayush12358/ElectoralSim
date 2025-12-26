"""
Additional unit tests to improve code coverage.
Tests edge cases, presets, and basic module imports.
"""

import pytest
import numpy as np
import polars as pl


class TestBehaviorModels:
    """Tests for behavior models and engine."""

    def test_proximity_model(self):
        """Test proximity voting model."""
        from electoral_sim import ProximityModel

        model = ProximityModel()
        assert model is not None

    def test_valence_model(self):
        """Test valence voting model."""
        from electoral_sim import ValenceModel

        model = ValenceModel()
        assert model is not None

    def test_retrospective_model(self):
        """Test retrospective voting model."""
        from electoral_sim import RetrospectiveModel

        model = RetrospectiveModel()
        assert model is not None

    def test_strategic_voting_model(self):
        """Test strategic voting model."""
        from electoral_sim import StrategicVotingModel

        model = StrategicVotingModel()
        assert model is not None

    def test_behavior_engine_creation(self):
        """Test BehaviorEngine creation."""
        from electoral_sim import BehaviorEngine

        engine = BehaviorEngine()
        assert engine is not None


class TestAlternativeVotingSystems:
    """Tests for IRV, STV, and other alternative systems."""

    def test_irv_election(self):
        """Test Instant Runoff Voting."""
        from electoral_sim import irv_election

        # Rankings: 1=first choice, 2=second, 3=third
        rankings = np.array(
            [
                [1, 2, 3],
                [1, 3, 2],
                [2, 1, 3],
                [3, 2, 1],
                [3, 1, 2],
            ]
        )

        result = irv_election(rankings, n_candidates=3)
        assert "winner" in result
        assert result["winner"] in [0, 1, 2]

    def test_stv_election(self):
        """Test Single Transferable Vote."""
        from electoral_sim import stv_election

        rankings = np.array(
            [
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [2, 1, 3, 4],
                [2, 1, 3, 4],
                [3, 1, 2, 4],
                [3, 2, 1, 4],
                [3, 2, 1, 4],
                [4, 3, 2, 1],
                [4, 3, 2, 1],
            ]
        )

        result = stv_election(rankings, n_candidates=4, n_seats=2)
        assert "elected" in result

    def test_approval_voting(self):
        """Test approval voting."""
        from electoral_sim import approval_voting

        approvals = np.array(
            [
                [1, 1, 0],
                [1, 0, 0],
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 1],
            ]
        )

        result = approval_voting(approvals, n_candidates=3)
        assert "winner" in result

    def test_generate_rankings(self):
        """Test ranking generation from utilities."""
        from electoral_sim import generate_rankings

        utilities = np.array(
            [
                [0.9, 0.5, 0.1],
                [0.2, 0.8, 0.3],
                [0.1, 0.2, 0.9],
            ]
        )

        rankings = generate_rankings(utilities)
        assert rankings.shape == (3, 3)


class TestCoalitionBasics:
    """Basic tests for coalition module."""

    def test_minimum_winning_coalitions_import(self):
        """Test minimum_winning_coalitions can be imported."""
        from electoral_sim import minimum_winning_coalitions

        assert callable(minimum_winning_coalitions)

    def test_coalition_strain_import(self):
        """Test coalition_strain can be imported."""
        from electoral_sim import coalition_strain

        assert callable(coalition_strain)

    def test_collapse_probability_import(self):
        """Test collapse_probability can be imported."""
        from electoral_sim import collapse_probability

        assert callable(collapse_probability)


class TestVoterGeneration:
    """Tests for voter frame generation."""

    def test_voter_frame_exists(self):
        """Test that voters have a DataFrame."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=100, seed=42)
        assert model.voters.df is not None
        assert len(model.voters.df) == 100


class TestPartyAgents:
    """Tests for party agent functionality."""

    def test_party_frame_exists(self):
        """Test party frame exists."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=100, seed=42)
        assert model.parties.df is not None
        assert len(model.parties.df) > 0


class TestMorePresets:
    """Additional preset tests."""

    def test_all_presets_loadable(self):
        """Test all presets can be loaded."""
        from electoral_sim import PRESETS

        for name, factory in PRESETS.items():
            config = factory()
            assert config is not None, f"Preset {name} failed to load"


class TestEdgeCases:
    """Edge case tests."""

    def test_small_election(self):
        """Test with minimum voters."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=10, n_constituencies=1, seed=42)
        results = model.run_election()
        assert results is not None

    def test_single_party(self):
        """Test with single party."""
        from electoral_sim import ElectionModel

        parties = [{"name": "Only Party", "position_x": 0, "position_y": 0, "valence": 50}]
        model = ElectionModel(n_voters=100, parties=parties, seed=42)
        results = model.run_election()
        assert results is not None

    def test_many_parties(self):
        """Test with many parties."""
        from electoral_sim import ElectionModel

        parties = [
            {
                "name": f"Party {i}",
                "position_x": np.sin(i) * 0.5,
                "position_y": np.cos(i) * 0.5,
                "valence": 50,
            }
            for i in range(15)
        ]
        model = ElectionModel(n_voters=1000, parties=parties, seed=42)
        results = model.run_election()
        assert results is not None
        assert len(results["seats"]) == 15

    def test_high_temperature(self):
        """Test with high temperature (random voting)."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, temperature=10.0, seed=42)
        results = model.run_election()
        assert results is not None

    def test_low_temperature(self):
        """Test with low temperature (deterministic voting)."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, temperature=0.01, seed=42)
        results = model.run_election()
        assert results is not None

    def test_with_nota(self):
        """Test with NOTA option enabled."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, include_nota=True, seed=42)
        results = model.run_election()
        assert results is not None

    def test_pr_system(self):
        """Test PR electoral system."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", seed=42)
        results = model.run_election()
        assert results["system"] == "PR"

    def test_different_allocation_methods(self):
        """Test different PR allocation methods."""
        from electoral_sim import ElectionModel

        for method in ["dhondt", "sainte_lague", "hare", "droop"]:
            model = ElectionModel(
                n_voters=1000, electoral_system="PR", allocation_method=method, seed=42
            )
            results = model.run_election()
            assert results is not None

    def test_with_threshold(self):
        """Test PR with electoral threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", threshold=0.05, seed=42)
        results = model.run_election()
        assert results is not None


class TestNumbaAcceleration:
    """Tests for Numba-accelerated functions."""

    def test_numba_available(self):
        """Test Numba availability check."""
        from electoral_sim.engine.numba_accel import NUMBA_AVAILABLE

        # Just check it's a boolean
        assert isinstance(NUMBA_AVAILABLE, bool)

    def test_fptp_count_fast(self):
        """Test FPTP counting."""
        from electoral_sim.engine.numba_accel import fptp_count_fast

        votes = np.array([0, 0, 1, 1, 1, 2])
        constituencies = np.array([0, 0, 0, 0, 0, 0])

        seats, counts = fptp_count_fast(constituencies, votes, 1, 3)
        assert seats is not None
        assert counts is not None
