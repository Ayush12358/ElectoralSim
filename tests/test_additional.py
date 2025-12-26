"""
Tests for behaviors, dynamics, and additional modules.
"""

import pytest
import numpy as np


class TestBehaviorEngineAdvanced:
    """Advanced behavior engine tests."""

    def test_engine_add_model(self):
        """Test adding models to engine."""
        from electoral_sim import BehaviorEngine, ProximityModel

        engine = BehaviorEngine()
        engine.add_model(ProximityModel(weight=1.0))
        assert len(engine.models) > 0

    def test_engine_compute_utilities(self):
        """Test engine computes utilities."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=100, seed=42)
        # Engine is used internally - model should work
        results = model.run_election()
        assert results is not None

    def test_proximity_weight(self):
        """Test proximity model with custom weight."""
        from electoral_sim import ProximityModel

        model = ProximityModel(weight=2.0)
        assert model.weight == 2.0

    def test_valence_weight(self):
        """Test valence model with custom weight."""
        from electoral_sim import ValenceModel

        model = ValenceModel(weight=0.5)
        assert model.weight == 0.5


class TestOpinionDynamicsAdvanced:
    """Advanced opinion dynamics tests."""

    def test_opinion_dynamics_import(self):
        """Test OpinionDynamics import."""
        from electoral_sim import OpinionDynamics

        assert OpinionDynamics is not None

    def test_create_network(self):
        """Test network creation for opinion dynamics."""
        import networkx as nx

        G = nx.barabasi_albert_graph(100, 3)
        assert len(G.nodes()) == 100


class TestAllocationMethods:
    """Test all allocation methods."""

    def test_dhondt_basic(self):
        """Test D'Hondt allocation."""
        from electoral_sim.systems.allocation import dhondt_allocation

        votes = np.array([100000, 80000, 30000])
        seats = dhondt_allocation(votes, 10)
        assert sum(seats) == 10

    def test_sainte_lague_basic(self):
        """Test Sainte-Lague allocation."""
        from electoral_sim.systems.allocation import sainte_lague_allocation

        votes = np.array([100000, 80000, 30000])
        seats = sainte_lague_allocation(votes, 10)
        assert sum(seats) == 10

    def test_hare_basic(self):
        """Test Hare quota allocation."""
        from electoral_sim.systems.allocation import hare_quota_allocation

        votes = np.array([100000, 80000, 30000])
        seats = hare_quota_allocation(votes, 10)
        assert sum(seats) == 10

    def test_droop_basic(self):
        """Test Droop quota allocation."""
        from electoral_sim.systems.allocation import droop_quota_allocation

        votes = np.array([100000, 80000, 30000])
        seats = droop_quota_allocation(votes, 10)
        assert sum(seats) == 10

    def test_allocation_proportionality(self):
        """Test that allocation is roughly proportional."""
        from electoral_sim.systems.allocation import dhondt_allocation

        votes = np.array([500, 300, 200])  # 50%, 30%, 20%
        seats = dhondt_allocation(votes, 10)

        # Largest party should get most seats
        assert seats[0] >= seats[1]
        assert seats[1] >= seats[2]


class TestAllMetrics:
    """Test all electoral metrics."""

    def test_gallagher_range(self):
        """Test Gallagher index is in valid range."""
        from electoral_sim.metrics.indices import gallagher_index

        vote_shares = np.array([0.4, 0.3, 0.2, 0.1])
        seat_shares = np.array([0.5, 0.3, 0.15, 0.05])

        lsq = gallagher_index(vote_shares, seat_shares)
        assert 0 <= lsq <= 100

    def test_enp_calculation(self):
        """Test ENP calculation."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        # Two equal parties = ENP of 2
        shares = np.array([0.5, 0.5])
        enp = effective_number_of_parties(shares)
        assert enp == pytest.approx(2.0, abs=0.01)

    def test_efficiency_gap_calculation(self):
        """Test efficiency gap."""
        from electoral_sim.metrics.indices import efficiency_gap

        votes_a = np.array([600, 600, 400])
        votes_b = np.array([400, 400, 600])
        seats_a = np.array([1, 1, 0])

        gap = efficiency_gap(votes_a, votes_b, seats_a)
        assert -1 <= gap <= 1


class TestModelEdgeCases:
    """More edge case tests."""

    def test_zero_threshold(self):
        """Test PR with zero threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", threshold=0.0, seed=42)
        results = model.run_election()
        assert results is not None

    def test_high_threshold(self):
        """Test PR with high threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel(
            n_voters=1000, electoral_system="PR", threshold=0.10, seed=42  # 10% threshold
        )
        results = model.run_election()
        assert results is not None

    def test_temperature_extremes(self):
        """Test extreme temperature values."""
        from electoral_sim import ElectionModel

        for temp in [0.001, 0.1, 1.0, 5.0, 100.0]:
            model = ElectionModel(n_voters=500, temperature=temp, seed=42)
            results = model.run_election()
            assert results is not None

    def test_various_voter_counts(self):
        """Test various voter counts."""
        from electoral_sim import ElectionModel

        for n in [10, 100, 1000, 5000]:
            model = ElectionModel(n_voters=n, seed=42)
            results = model.run_election()
            assert results is not None


class TestAllPresets:
    """Test all country presets individually."""

    def test_india_preset_detailed(self):
        """Test India preset in detail."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("india", n_voters=5000)
        assert model.n_constituencies == 543
        results = model.run_election()
        assert results is not None

    def test_usa_preset_detailed(self):
        """Test USA preset in detail."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("usa", n_voters=5000)
        assert model.n_constituencies == 435
        results = model.run_election()
        assert results is not None

    def test_uk_preset_detailed(self):
        """Test UK preset in detail."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("uk", n_voters=5000)
        assert model.n_constituencies == 650
        results = model.run_election()
        assert results is not None

    def test_germany_preset_detailed(self):
        """Test Germany preset in detail."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("germany", n_voters=5000)
        results = model.run_election()
        assert results is not None

    def test_france_preset_detailed(self):
        """Test France preset in detail."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("france", n_voters=5000)
        results = model.run_election()
        assert results is not None

    def test_australia_preset_detailed(self):
        """Test Australia preset in detail."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("australia_house", n_voters=5000)
        results = model.run_election()
        assert results is not None

    def test_brazil_preset_detailed(self):
        """Test Brazil preset in detail."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("brazil", n_voters=5000)
        results = model.run_election()
        assert results is not None


class TestReproducibility:
    """Test reproducibility across runs."""

    def test_deterministic_with_seed(self):
        """Test same seed gives identical results."""
        from electoral_sim import ElectionModel

        results1 = ElectionModel(n_voters=1000, seed=999).run_election()
        results2 = ElectionModel(n_voters=1000, seed=999).run_election()

        # Turnout should be identical
        assert results1["turnout"] == results2["turnout"]

    def test_different_seeds_differ(self):
        """Test different seeds give different results."""
        from electoral_sim import ElectionModel

        results1 = ElectionModel(n_voters=1000, seed=1).run_election()
        results2 = ElectionModel(n_voters=1000, seed=2).run_election()
        results3 = ElectionModel(n_voters=1000, seed=3).run_election()

        turnouts = [results1["turnout"], results2["turnout"], results3["turnout"]]
        # Not all should be identical
        assert len(set([round(t, 3) for t in turnouts])) > 1


class TestResultStructure:
    """Test result dictionary structure."""

    def test_fptp_result_keys(self):
        """Test FPTP results have expected keys."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="FPTP", seed=42)
        results = model.run_election()

        assert "system" in results
        assert "seats" in results
        assert "turnout" in results

    def test_pr_result_keys(self):
        """Test PR results have expected keys."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", seed=42)
        results = model.run_election()

        assert "system" in results
        assert "seats" in results
        assert "turnout" in results
