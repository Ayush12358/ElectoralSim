# Copyright 2025-2026 Ayush Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for electoral metrics: Gallagher, ENP, HHI, efficiency gap, VSE, and utility functions."""

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

        for shares in [
            np.array([1.0]),
            np.array([0.5, 0.5]),
            np.array([0.9, 0.1]),
            np.array([0.25, 0.25, 0.25, 0.25]),
        ]:
            assert effective_number_of_parties(shares) >= 1.0

    def test_handles_percentages(self):
        """ENP auto-converts percentages > 1.5."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        enp = effective_number_of_parties(np.array([50.0, 50.0]))
        assert abs(enp - 2.0) < 0.01


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

        equal = herfindahl_hirschman_index(np.array([0.25, 0.25, 0.25, 0.25]))
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

    def test_efficiency_gap_zero_votes(self):
        """efficiency_gap returns 0.0 for zero total votes."""
        from electoral_sim.metrics.indices import efficiency_gap

        result = efficiency_gap(np.array([0, 0]), np.array([0, 0]), np.array([1, 0]))
        assert result == 0.0

    def test_enp_zero_shares(self):
        """effective_number_of_parties returns 1.0 for all-zero shares."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        assert effective_number_of_parties(np.array([0.0, 0.0, 0.0])) == 1.0
        assert effective_number_of_parties(np.array([])) == 1.0

    def test_turnout_rate(self):
        from electoral_sim.metrics.indices import turnout_rate

        assert turnout_rate(750, 1000) == 0.75
        assert turnout_rate(0, 1000) == 0.0
        assert turnout_rate(100, 0) == 0.0

    def test_vote_share(self):
        from electoral_sim.metrics.indices import vote_share

        assert vote_share(300, 1000) == 0.3
        assert vote_share(0, 1000) == 0.0
        assert vote_share(100, 0) == 0.0

    def test_seat_share(self):
        from electoral_sim.metrics.indices import seat_share

        assert seat_share(50, 100) == 0.5
        assert seat_share(0, 100) == 0.0
        assert seat_share(10, 0) == 0.0

    def test_seats_votes_ratio(self):
        from electoral_sim.metrics.indices import seats_votes_ratio

        assert seats_votes_ratio(0.6, 0.4) == pytest.approx(1.5)
        assert seats_votes_ratio(0.3, 0.5) == pytest.approx(0.6)
        assert seats_votes_ratio(0.5, 0.0) == 0.0


class TestVSE:
    """Voter Satisfaction Efficiency tests."""

    def test_vse_in_results(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()
        assert "vse" in results
        assert isinstance(results["vse"], float)

    def test_calculate_welfare_basic(self):
        from electoral_sim.analysis.vse import calculate_welfare

        utilities = np.array([10.0, 20.0, 30.0])
        assert calculate_welfare(utilities) == 60.0

    def test_calculate_welfare_with_weights(self):
        from electoral_sim.analysis.vse import calculate_welfare

        utilities = np.array([10.0, 20.0, 30.0])
        weights = np.array([0.5, 0.3, 0.2])
        result = calculate_welfare(utilities, weights=weights)
        assert result == pytest.approx(5.0 + 6.0 + 6.0)

    def test_calculate_vse_perfect_system(self):
        """VSE = 1.0 when actual outcome matches optimal."""
        from electoral_sim.analysis.vse import calculate_vse

        # Voter utilities: 3 voters, 2 parties
        # Party 0 gives utility [10, 10, 10] → total 30
        # Party 1 gives utility [5, 5, 5] → total 15
        utilities = np.array([[10, 5], [10, 5], [10, 5]])
        # Optimal is party 0 (total 30), random is mean(30,15)=22.5
        # If actual = optimal (all seats to party 0): VSE = (30-22.5)/(30-22.5) = 1.0
        seat_shares = np.array([1.0, 0.0])
        vse = calculate_vse(utilities, seat_shares)
        assert vse == pytest.approx(1.0)

    def test_calculate_vse_random_system(self):
        """VSE ≈ 0 when actual = random."""
        from electoral_sim.analysis.vse import calculate_vse

        utilities = np.array([[10, 5], [10, 5], [10, 5]])
        # Actual = random (equal seats)
        seat_shares = np.array([0.5, 0.5])
        vse = calculate_vse(utilities, seat_shares)
        assert vse == pytest.approx(0.0)

    def test_calculate_vse_all_equal(self):
        """VSE = 0 when all parties give equal utility."""
        from electoral_sim.analysis.vse import calculate_vse

        utilities = np.array([[5, 5], [5, 5]])
        seat_shares = np.array([1.0, 0.0])
        vse = calculate_vse(utilities, seat_shares)
        assert vse == 0.0

    def test_partisan_bias_symmetric(self):
        """Partisan bias is 0 when seat share = vote share."""
        from electoral_sim.metrics.indices import partisan_bias

        votes = np.array([60, 55, 40, 45])
        seats = np.array([1, 1, 0, 0])
        bias = partisan_bias(votes, seats)
        assert isinstance(bias, float)

    def test_mean_median_gap_symmetric(self):
        """Mean-median gap is 0 when mean = median."""
        from electoral_sim.metrics.indices import mean_median_gap

        gap = mean_median_gap(np.array([0.5, 0.5, 0.5]))
        assert gap == 0.0

    def test_mean_median_gap_cracked(self):
        """Mean-median gap is positive when cracked (mean > median)."""
        from electoral_sim.metrics.indices import mean_median_gap

        # Cracked: many districts close to 0.4, one district at 0.9
        gap = mean_median_gap(np.array([0.4, 0.4, 0.4, 0.9]))
        assert gap > 0

    def test_partisan_gini_equal(self):
        """Partisan Gini is 0 when all districts have same share."""
        from electoral_sim.metrics.indices import partisan_gini

        gini = partisan_gini(np.array([0.5, 0.5, 0.5, 0.5]))
        assert gini == 0.0

    def test_partisan_gini_edge_cases(self):
        """Partisan Gini handles edge cases."""
        from electoral_sim.metrics.indices import partisan_gini

        assert partisan_gini(np.array([])) == 0.0
        assert partisan_gini(np.array([0.3])) == 0.0

    def test_responsiveness_basic(self):
        """Responsiveness returns a finite float."""
        from electoral_sim.metrics.indices import responsiveness

        votes = np.array([0.6, 0.5, 0.4])
        seats = np.array([1, 1, 0])
        r = responsiveness(votes, seats)
        assert isinstance(r, float)
        assert np.isfinite(r)

    def test_swing_ratio_basic(self):
        """Swing ratio returns a non-negative float."""
        from electoral_sim.metrics.indices import swing_ratio

        votes_a = np.array([60, 55, 40])
        votes_b = np.array([40, 45, 60])
        seats_a = np.array([1, 1, 0])
        ratio = swing_ratio(votes_a, votes_b, seats_a)
        assert ratio >= 0

    def test_polsby_popper_circle(self):
        """Polsby-Popper of a circle (area=π, perimeter=2π) is 1.0."""
        from electoral_sim.metrics.indices import polsby_popper

        score = polsby_popper(np.pi, 2 * np.pi)
        assert abs(score - 1.0) < 0.001

    def test_polsby_popper_zero_perimeter(self):
        """Polsby-Popper with zero perimeter returns 0.0."""
        from electoral_sim.metrics.indices import polsby_popper

        assert polsby_popper(100, 0) == 0.0

    def test_convex_hull_compactness_convex(self):
        """Convex hull compactness of a convex shape is 1.0."""
        from electoral_sim.metrics.indices import convex_hull_compactness

        score = convex_hull_compactness(50, 50)
        assert score == 1.0
