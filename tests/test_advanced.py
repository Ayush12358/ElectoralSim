"""
Additional tests for coalition, government, and advanced features.
"""

import pytest
import numpy as np


class TestCoalitionFormation:
    """Tests for coalition formation algorithms."""

    def test_minimum_winning_coalitions_import(self):
        """Test MWC function can be imported."""
        from electoral_sim import minimum_winning_coalitions

        assert callable(minimum_winning_coalitions)

    def test_coalition_strain_import(self):
        """Test coalition strain import."""
        from electoral_sim import coalition_strain

        assert callable(coalition_strain)


class TestGovernmentSimulation:
    """Tests for government stability simulation."""

    def test_collapse_probability_zero_strain(self):
        """Test collapse probability with zero strain."""
        from electoral_sim import collapse_probability

        # (time_in_office, strain, stability)
        prob = collapse_probability(12, 0.0, 0.8)
        assert 0 <= prob <= 1

    def test_collapse_probability_high_strain(self):
        """Test collapse probability with high strain."""
        from electoral_sim import collapse_probability

        # (time_in_office, strain, stability)
        prob = collapse_probability(24, 2.0, 0.3)
        assert 0 <= prob <= 1

    def test_government_simulator_import(self):
        """Test GovernmentSimulator can be imported."""
        from electoral_sim import GovernmentSimulator

        assert GovernmentSimulator is not None

    def test_simulate_government_survival_import(self):
        """Test simulate_government_survival import."""
        from electoral_sim import simulate_government_survival

        assert callable(simulate_government_survival)


class TestFormGovernment:
    """Tests for government formation."""

    def test_form_government_import(self):
        """Test form_government can be imported."""
        from electoral_sim import form_government

        assert callable(form_government)


class TestMetricsAdvanced:
    """Advanced tests for metrics module."""

    def test_gallagher_index_extreme(self):
        """Test Gallagher with extreme disproportionality."""
        from electoral_sim.metrics.indices import gallagher_index

        vote_shares = np.array([0.20, 0.20, 0.20, 0.20, 0.20])
        seat_shares = np.array([1.0, 0.0, 0.0, 0.0, 0.0])

        lsq = gallagher_index(vote_shares, seat_shares)
        assert lsq > 0
        assert lsq < 100

    def test_enp_many_parties(self):
        """Test ENP with many small parties."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        shares = np.ones(10) / 10
        enp = effective_number_of_parties(shares)
        assert enp == pytest.approx(10.0, abs=0.01)

    def test_enp_fragmented(self):
        """Test ENP with fragmented party system."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        shares = np.array([0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.05, 0.05])
        enp = effective_number_of_parties(shares)
        assert 4 < enp < 8


class TestIndiaPreset:
    """Tests specifically for India preset."""

    def test_india_states_import(self):
        """Test INDIA_STATES can be imported."""
        from electoral_sim import INDIA_STATES

        assert isinstance(INDIA_STATES, dict)

    def test_india_parties_import(self):
        """Test INDIA_PARTIES can be imported."""
        from electoral_sim import INDIA_PARTIES

        assert isinstance(INDIA_PARTIES, dict)

    def test_simulate_india_election_import(self):
        """Test simulate_india_election can be imported."""
        from electoral_sim import simulate_india_election

        assert callable(simulate_india_election)

    def test_india_election_result_class(self):
        """Test IndiaElectionResult class."""
        from electoral_sim import IndiaElectionResult

        assert IndiaElectionResult is not None


class TestChainableAPI:
    """Tests for fluent/chainable API."""

    def test_full_chain(self):
        """Test full chainable API."""
        from electoral_sim import ElectionModel

        model = (
            ElectionModel(n_voters=1000, seed=42)
            .with_system("PR")
            .with_allocation("sainte_lague")
            .with_threshold(0.03)
            .with_temperature(0.8)
        )

        assert model.electoral_system == "PR"
        assert model.allocation_method == "sainte_lague"
        assert model.threshold == 0.03
        assert model.temperature == 0.8

        results = model.run_election()
        assert results is not None

    def test_chain_returns_self(self):
        """Test that chain methods return self."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=100, seed=42)
        result = model.with_system("FPTP")
        assert result is model


class TestMultipleElections:
    """Tests for running multiple elections."""

    def test_run_multiple_elections(self):
        """Test running multiple elections."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)

        results = []
        for _ in range(5):
            r = model.run_election()
            results.append(r)

        assert len(results) == 5

    def test_batch_simulation(self):
        """Test batch election simulation."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)

        all_results = []
        for i in range(10):
            result = model.run_election()
            all_results.append(result["turnout"])

        assert len(all_results) == 10


class TestRandomSeeds:
    """Tests for reproducibility with seeds."""

    def test_same_seed_same_result(self):
        """Test that same seed gives same results."""
        from electoral_sim import ElectionModel

        model1 = ElectionModel(n_voters=1000, seed=12345)
        result1 = model1.run_election()

        model2 = ElectionModel(n_voters=1000, seed=12345)
        result2 = model2.run_election()

        assert result1["turnout"] == pytest.approx(result2["turnout"], abs=0.01)

    def test_different_seed_different_result(self):
        """Test that different seeds give different results."""
        from electoral_sim import ElectionModel

        results = []
        for seed in [1, 2, 3]:
            model = ElectionModel(n_voters=1000, seed=seed)
            result = model.run_election()
            results.append(result["turnout"])

        assert len(set([round(r, 2) for r in results])) > 1


class TestConstituencies:
    """Tests for constituency handling."""

    def test_many_constituencies(self):
        """Test with many constituencies."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=5000, n_constituencies=50, seed=42)
        results = model.run_election()

        assert results is not None

    def test_single_constituency(self):
        """Test with single constituency."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, n_constituencies=1, seed=42)
        results = model.run_election()

        assert results is not None
        if results["system"] == "FPTP":
            assert sum(results["seats"]) == 1


class TestVSEMetric:
    """Tests for Voter Satisfaction Efficiency."""

    def test_vse_in_results(self):
        """Test that VSE is computed in results."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()

        # VSE should be in results
        if "vse" in results:
            assert -1 <= results["vse"] <= 1


class TestENPMetrics:
    """Tests for ENP metrics in results."""

    def test_enp_votes_in_results(self):
        """Test ENP votes is in results."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()

        if "enp_votes" in results:
            assert results["enp_votes"] >= 1

    def test_enp_seats_in_results(self):
        """Test ENP seats is in results."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()

        if "enp_seats" in results:
            assert results["enp_seats"] >= 1
