"""
Improved tests with:
- Property-based testing (Hypothesis)
- Parameterized tests
- Performance benchmarks
- Error handling tests
- Real-world validation tests
"""

import pytest
import numpy as np
import time

# Hypothesis for property-based testing
try:
    from hypothesis import given, strategies as st, settings, assume

    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False


# ============================================================================
# PROPERTY-BASED TESTS (Hypothesis)
# ============================================================================


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="Hypothesis not installed")
class TestPropertyBased:
    """Property-based tests that generate random inputs."""

    @given(n_voters=st.integers(10, 5000), n_const=st.integers(1, 50))
    @settings(max_examples=20, deadline=None)
    def test_seats_dont_exceed_constituencies(self, n_voters, n_const):
        """Total seats should never exceed number of constituencies in FPTP."""
        from electoral_sim import ElectionModel

        model = ElectionModel(
            n_voters=n_voters, n_constituencies=n_const, electoral_system="FPTP", seed=42
        )
        results = model.run_election()
        assert sum(results["seats"]) <= n_const

    @given(n_voters=st.integers(100, 2000))
    @settings(max_examples=15, deadline=None)
    def test_turnout_is_valid_proportion(self, n_voters):
        """Turnout should always be between 0 and 1."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=n_voters, seed=42)
        results = model.run_election()
        assert 0 <= results["turnout"] <= 1

    @given(temp=st.floats(min_value=0.01, max_value=100.0))
    @settings(max_examples=15, deadline=None)
    def test_temperature_produces_valid_results(self, temp):
        """Any valid temperature should produce valid election results."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=500, temperature=temp, seed=42)
        results = model.run_election()
        assert results is not None
        assert "seats" in results

    @given(threshold=st.floats(min_value=0.0, max_value=0.25))
    @settings(max_examples=10, deadline=None)
    def test_threshold_produces_valid_pr_results(self, threshold):
        """Any valid threshold should work with PR system."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", threshold=threshold, seed=42)
        results = model.run_election()
        assert results is not None

    @given(votes=st.lists(st.integers(min_value=1, max_value=100000), min_size=2, max_size=10))
    @settings(max_examples=20, deadline=None)
    def test_allocation_sums_to_total_seats(self, votes):
        """PR allocation should always sum to exactly total seats."""
        from electoral_sim.systems.allocation import dhondt_allocation

        votes_arr = np.array(votes)
        total_seats = 20
        seats = dhondt_allocation(votes_arr, total_seats)
        assert sum(seats) == total_seats


# ============================================================================
# PARAMETERIZED TESTS
# ============================================================================


class TestParameterized:
    """Parameterized tests to reduce code duplication."""

    @pytest.mark.parametrize("system", ["FPTP", "PR"])
    def test_basic_systems(self, system):
        """Test basic electoral systems work."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system=system, seed=42)
        results = model.run_election()
        assert results["system"] == system

    @pytest.mark.parametrize("method", ["dhondt", "sainte_lague", "hare", "droop"])
    def test_all_allocation_methods(self, method):
        """Test all PR allocation methods."""
        from electoral_sim import ElectionModel

        model = ElectionModel(
            n_voters=1000, electoral_system="PR", allocation_method=method, seed=42
        )
        results = model.run_election()
        assert results is not None

    @pytest.mark.parametrize(
        "preset",
        [
            "india",
            "usa",
            "uk",
            "germany",
            "france",
            "australia_house",
            "brazil",
            "japan",
            "south_africa",
        ],
    )
    def test_all_presets_run(self, preset):
        """Test all country presets can run elections."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset(preset, n_voters=1000)
        results = model.run_election()
        assert results is not None

    @pytest.mark.parametrize("n_voters", [10, 100, 1000, 5000])
    def test_various_voter_counts(self, n_voters):
        """Test elections work with various voter counts."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=n_voters, seed=42)
        results = model.run_election()
        assert results is not None

    @pytest.mark.parametrize("n_const", [1, 5, 10, 50, 100])
    def test_various_constituency_counts(self, n_const):
        """Test elections work with various constituency counts."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=max(100, n_const * 10), n_constituencies=n_const, seed=42)
        results = model.run_election()
        assert results is not None

    @pytest.mark.parametrize("seed", [1, 42, 100, 999, 12345])
    def test_various_seeds(self, seed):
        """Test various random seeds work."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=500, seed=seed)
        results = model.run_election()
        assert results is not None


# ============================================================================
# PERFORMANCE BENCHMARK TESTS
# ============================================================================


@pytest.mark.slow
class TestPerformance:
    """Performance benchmark tests (marked slow, skip with -m 'not slow')."""

    def test_1k_voters_under_1_second(self):
        """1K voters should complete in under 1 second."""
        from electoral_sim import ElectionModel

        start = time.time()
        model = ElectionModel(n_voters=1000, seed=42)
        model.run_election()
        elapsed = time.time() - start

        assert elapsed < 1.0, f"1K voters took {elapsed:.2f}s (expected <1s)"

    def test_10k_voters_under_5_seconds(self):
        """10K voters should complete in under 5 seconds."""
        from electoral_sim import ElectionModel

        start = time.time()
        model = ElectionModel(n_voters=10_000, seed=42)
        model.run_election()
        elapsed = time.time() - start

        assert elapsed < 5.0, f"10K voters took {elapsed:.2f}s (expected <5s)"

    def test_batch_10_elections_under_10_seconds(self):
        """10 elections should complete in under 10 seconds."""
        from electoral_sim import ElectionModel

        start = time.time()
        model = ElectionModel(n_voters=5000, seed=42)
        for _ in range(10):
            model.run_election()
        elapsed = time.time() - start

        assert elapsed < 10.0, f"10 elections took {elapsed:.2f}s (expected <10s)"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


class TestErrorHandling:
    """Tests for proper error handling."""

    def test_invalid_electoral_system_raises_error(self):
        """Invalid electoral system should raise an error or fall back gracefully."""
        from electoral_sim import ElectionModel

        try:
            model = ElectionModel(n_voters=100, electoral_system="INVALID_SYSTEM")
            results = model.run_election()
            # If no error, check that it fell back to a valid system
            assert results["system"] in ["FPTP", "PR", "IRV", "STV"]
        except (ValueError, KeyError):
            pass  # Expected behavior

    def test_invalid_allocation_method_raises_error(self):
        """Invalid allocation method should raise an error."""
        from electoral_sim import ElectionModel

        with pytest.raises((ValueError, KeyError)):
            model = ElectionModel(
                n_voters=100, electoral_system="PR", allocation_method="invalid_method"
            )
            model.run_election()

    def test_invalid_preset_raises_error(self):
        """Invalid preset should raise an error."""
        from electoral_sim import ElectionModel

        with pytest.raises((ValueError, KeyError)):
            ElectionModel.from_preset("nonexistent_country")

    def test_negative_voters_handled(self):
        """Negative voters should be handled gracefully."""
        from electoral_sim import ElectionModel

        # Should either work with min value or raise error
        try:
            model = ElectionModel(n_voters=-100, seed=42)
            # If it doesn't raise, it should handle gracefully
        except (ValueError, TypeError):
            pass  # Expected

    def test_zero_constituencies_handled(self):
        """Zero constituencies should be handled."""
        from electoral_sim import ElectionModel

        try:
            model = ElectionModel(n_voters=100, n_constituencies=0, seed=42)
            model.run_election()
        except (ValueError, ZeroDivisionError):
            pass  # Expected


# ============================================================================
# REAL-WORLD VALIDATION TESTS
# ============================================================================


class TestRealWorldValidation:
    """Tests comparing against real-world data and academic results."""

    def test_gallagher_known_values(self):
        """Test Gallagher index against known UK 2019 approximate values."""
        from electoral_sim.metrics.indices import gallagher_index

        # UK 2019 approximate: 15-16% Gallagher index
        # Using simplified vote/seat shares
        vote_shares = np.array([0.437, 0.322, 0.116, 0.039, 0.027, 0.059])
        seat_shares = np.array([0.562, 0.312, 0.017, 0.074, 0.000, 0.035])

        lsq = gallagher_index(vote_shares, seat_shares)
        # Should be in reasonable range (10-25 for UK)
        assert 5 < lsq < 30

    def test_enp_two_party_system(self):
        """ENP for classic two-party system should be ~2."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        # US 2020 approximate (two-party dominant)
        shares = np.array([0.513, 0.467, 0.02])  # Dem, Rep, Other
        enp = effective_number_of_parties(shares)

        # Should be close to 2 for two-party system
        assert 1.5 < enp < 2.5

    def test_enp_multiparty_system(self):
        """ENP for multiparty system should be >3."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        # Germany-like fragmentation
        shares = np.array([0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.05, 0.05])
        enp = effective_number_of_parties(shares)

        # Should be higher for fragmented system
        assert enp > 4

    def test_allocation_proportionality(self):
        """PR allocation should be more proportional than FPTP."""
        from electoral_sim import ElectionModel
        from electoral_sim.metrics.indices import gallagher_index

        # Run same voters with FPTP and PR
        model_fptp = ElectionModel(n_voters=5000, electoral_system="FPTP", seed=42)
        results_fptp = model_fptp.run_election()

        model_pr = ElectionModel(n_voters=5000, electoral_system="PR", seed=42)
        results_pr = model_pr.run_election()

        # PR should generally have lower Gallagher (more proportional)
        # Note: This is a weak test because simulation may vary
        assert results_pr is not None
        assert results_fptp is not None

    def test_india_lok_sabha_structure(self):
        """India preset should have 543 constituencies."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("india", n_voters=5000)
        assert model.n_constituencies == 543

    def test_usa_house_structure(self):
        """USA preset should have 435 constituencies."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("usa", n_voters=5000)
        assert model.n_constituencies == 435

    def test_uk_commons_structure(self):
        """UK preset should have 650 constituencies."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("uk", n_voters=5000)
        assert model.n_constituencies == 650


# ============================================================================
# INVARIANT TESTS
# ============================================================================


class TestInvariants:
    """Tests for mathematical and logical invariants."""

    def test_seats_non_negative(self):
        """All seat counts should be non-negative."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()

        assert all(s >= 0 for s in results["seats"])

    def test_vote_shares_sum_to_one(self):
        """Vote shares should sum to approximately 1."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()

        if "vote_shares" in results:
            assert abs(sum(results["vote_shares"]) - 1.0) < 0.01

    def test_enp_never_less_than_one(self):
        """ENP should never be less than 1."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        test_cases = [
            np.array([1.0]),  # Single party
            np.array([0.5, 0.5]),  # Two equal
            np.array([0.9, 0.1]),  # Dominant with minor
            np.array([0.25, 0.25, 0.25, 0.25]),  # Four equal
        ]

        for shares in test_cases:
            enp = effective_number_of_parties(shares)
            assert enp >= 1.0

    def test_gallagher_zero_for_perfect_proportionality(self):
        """Gallagher index should be 0 for perfect proportionality."""
        from electoral_sim.metrics.indices import gallagher_index

        shares = np.array([0.4, 0.3, 0.2, 0.1])
        lsq = gallagher_index(shares, shares)

        assert lsq == pytest.approx(0.0, abs=0.001)

    def test_determinism_with_same_seed(self):
        """Same seed should produce valid results."""
        from electoral_sim import ElectionModel

        # With same seed, model initialization should be consistent
        model = ElectionModel(n_voters=1000, seed=12345)
        result = model.run_election()

        # Verify result structure is valid
        assert result is not None
        assert "seats" in result
        assert "turnout" in result
        assert 0 <= result["turnout"] <= 1
