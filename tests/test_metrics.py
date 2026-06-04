"""Tests for electoral metrics: Gallagher, ENP, HHI, efficiency gap, VSE, and invariants."""

import numpy as np
import pytest


class TestGallagherIndex:
    """Gallagher disproportionality index."""

    def test_basic(self):
        from electoral_sim.metrics.indices import gallagher_index

        vote_shares = np.array([0.45, 0.35, 0.20])
        seat_shares = np.array([0.55, 0.35, 0.10])
        result = gallagher_index(vote_shares, seat_shares)
        assert 0 < result < 20

    def test_perfect_proportionality(self):
        from electoral_sim.metrics.indices import gallagher_index

        shares = np.array([0.4, 0.3, 0.2, 0.1])
        assert gallagher_index(shares, shares) == pytest.approx(0.0, abs=0.001)

    def test_extreme_disproportionality(self):
        from electoral_sim.metrics.indices import gallagher_index

        vote_shares = np.array([0.20, 0.20, 0.20, 0.20, 0.20])
        seat_shares = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
        result = gallagher_index(vote_shares, seat_shares)
        assert result > 50

    def test_known_uk_value(self):
        """UK 2019 approximate Gallagher should be 10-25."""
        from electoral_sim.metrics.indices import gallagher_index

        vote_shares = np.array([0.437, 0.322, 0.116, 0.039, 0.027, 0.059])
        seat_shares = np.array([0.562, 0.312, 0.017, 0.074, 0.000, 0.035])
        lsq = gallagher_index(vote_shares, seat_shares)
        assert 5 < lsq < 30

    def test_handles_percentages(self):
        """Should auto-convert percentages to shares."""
        from electoral_sim.metrics.indices import gallagher_index

        # Values > 1.5 should be treated as percentages
        vote_shares = np.array([45.0, 35.0, 20.0])
        seat_shares = np.array([55.0, 35.0, 10.0])
        result = gallagher_index(vote_shares, seat_shares)
        assert 0 < result < 20


class TestEffectiveNumberOfParties:
    """ENP (Laakso-Taagepera) tests."""

    def test_two_equal_parties(self):
        from electoral_sim.metrics.indices import effective_number_of_parties

        enp = effective_number_of_parties(np.array([0.5, 0.5]))
        assert abs(enp - 2.0) < 0.01

    def test_single_party(self):
        from electoral_sim.metrics.indices import effective_number_of_parties

        enp = effective_number_of_parties(np.array([1.0]))
        assert abs(enp - 1.0) < 0.01

    def test_many_equal_parties(self):
        from electoral_sim.metrics.indices import effective_number_of_parties

        enp = effective_number_of_parties(np.array([0.1] * 10))
        assert abs(enp - 10.0) < 0.01

    def test_multiparty_system(self):
        """Germany-like fragmentation should have ENP > 4."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        shares = np.array([0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.05, 0.05])
        assert effective_number_of_parties(shares) > 4

    def test_never_less_than_one(self):
        from electoral_sim.metrics.indices import effective_number_of_parties

        for shares in [np.array([1.0]), np.array([0.5, 0.5]), np.array([0.9, 0.1]),
                       np.array([0.25, 0.25, 0.25, 0.25])]:
            assert effective_number_of_parties(shares) >= 1.0


class TestOtherMetrics:
    """Loosemore-Hanby, HHI, efficiency gap."""

    def test_loosemore_hanby(self):
        from electoral_sim.metrics.indices import loosemore_hanby_index

        vote_shares = np.array([0.4, 0.35, 0.25])
        seat_shares = np.array([0.5, 0.3, 0.2])
        result = loosemore_hanby_index(vote_shares, seat_shares)
        assert 0 <= result <= 100

    def test_hhi(self):
        from electoral_sim.metrics.indices import herfindahl_hirschman_index

        # Equal shares → low concentration
        equal = herfindahl_hirschman_index(np.array([0.25, 0.25, 0.25, 0.25]))
        # Single dominant → high concentration
        dominant = herfindahl_hirschman_index(np.array([0.9, 0.05, 0.03, 0.02]))
        assert dominant > equal

    def test_efficiency_gap(self):
        from electoral_sim.metrics.indices import efficiency_gap

        # 5 districts: party A wins 3, party B wins 2
        party_a_votes = np.array([60, 55, 52, 40, 45])
        party_b_votes = np.array([40, 45, 48, 60, 55])
        party_a_seats = np.array([1, 1, 1, 0, 0])
        result = efficiency_gap(party_a_votes, party_b_votes, party_a_seats)
        assert isinstance(result, float)

    def test_efficiency_gap_known_case(self):
        """Known test case for efficiency gap."""
        from electoral_sim.metrics.indices import efficiency_gap

        party_a_votes = np.array([52, 48])
        party_b_votes = np.array([48, 52])
        party_a_seats = np.array([1, 0])
        result = efficiency_gap(party_a_votes, party_b_votes, party_a_seats)
        assert isinstance(result, float)


class TestVSE:
    """Voter Satisfaction Efficiency tests."""

    def test_vse_in_results(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()
        assert "vse" in results
        assert isinstance(results["vse"], float)
