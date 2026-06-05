"""
Unit tests for electoral systems and core calculations.
These tests focus on specific functions to improve code coverage.
"""

import pytest
import numpy as np
from hypothesis import given, strategies as st, assume


class TestElectoralSystems:
    """Tests for electoral system calculations."""

    def test_fptp_basic(self):
        """Test FPTP with simple vote counts."""
        from electoral_sim.engine.numba_accel import fptp_count_fast

        # Each voter votes for a party: 0,0,1,1,1,2 = Party 1 gets 3 votes
        votes = np.array([0, 0, 1, 1, 1, 2])
        constituencies = np.array([0, 0, 0, 0, 0, 0])  # All in constituency 0
        n_const = 1
        n_parties = 3

        # fptp_count_fast(constituencies, votes, n_constituencies, n_parties)
        seats, vote_counts = fptp_count_fast(constituencies, votes, n_const, n_parties)
        assert int(seats[1]) == 1  # Party 1 wins the constituency
        assert int(seats[0]) == 0
        assert int(seats[2]) == 0

    def test_fptp_multiple_constituencies(self):
        """Test FPTP with multiple constituencies."""
        from electoral_sim.engine.numba_accel import fptp_count_fast

        # 6 voters in 2 constituencies
        # Const 0: voters vote 0, 0, 1 -> Party 0 wins
        # Const 1: voters vote 1, 1, 0 -> Party 1 wins
        votes = np.array([0, 0, 1, 1, 1, 0])
        constituencies = np.array([0, 0, 0, 1, 1, 1])
        n_const = 2
        n_parties = 2

        seats, vote_counts = fptp_count_fast(constituencies, votes, n_const, n_parties)
        assert int(seats[0]) == 1  # Party 0 wins constituency 0
        assert int(seats[1]) == 1  # Party 1 wins constituency 1

    def test_dhondt_allocation(self):
        """Test D'Hondt seat allocation."""
        from electoral_sim.systems.allocation import dhondt_allocation

        votes = np.array([100000, 80000, 30000])
        total_seats = 10

        seats = dhondt_allocation(votes, total_seats)
        assert sum(seats) == total_seats
        assert seats[0] > seats[1] > seats[2]

    def test_sainte_lague_allocation(self):
        """Test Sainte-Lague seat allocation."""
        from electoral_sim.systems.allocation import sainte_lague_allocation

        votes = np.array([100000, 80000, 30000])
        total_seats = 10

        seats = sainte_lague_allocation(votes, total_seats)
        assert sum(seats) == total_seats

    def test_hare_quota(self):
        """Test Hare quota allocation."""
        from electoral_sim.systems.allocation import hare_quota_allocation

        votes = np.array([100000, 80000, 30000])
        total_seats = 10

        seats = hare_quota_allocation(votes, total_seats)
        assert sum(seats) == total_seats

    def test_droop_quota(self):
        """Test Droop quota allocation."""
        from electoral_sim.systems.allocation import droop_quota_allocation

        votes = np.array([100000, 80000, 30000])
        total_seats = 10

        seats = droop_quota_allocation(votes, total_seats)
        assert sum(seats) == total_seats

    @pytest.mark.parametrize(
        "allocator_name",
        ["dhondt", "sainte_lague", "hare", "droop"],
    )
    def test_allocation_zero_guards(self, allocator_name):
        """All allocators handle zero votes and non-positive seats gracefully."""
        from electoral_sim.systems.allocation import ALLOCATION_METHODS

        allocator = ALLOCATION_METHODS[allocator_name]

        # Zero total votes → zeros
        seats = allocator(np.array([0, 0, 0]), 5)
        assert isinstance(seats, np.ndarray)
        assert seats.sum() == 0

        # Zero seats → zeros
        seats = allocator(np.array([100, 80, 30]), 0)
        assert seats.sum() == 0

        # Negative seats → zeros
        seats = allocator(np.array([100, 80, 30]), -1)
        assert seats.sum() == 0

    def test_allocation_all_thresholded_zero(self):
        """All parties below threshold with zero votes → zeros."""
        from electoral_sim.systems.allocation import dhondt_allocation

        votes = np.array([0, 0, 0])
        seats = dhondt_allocation(votes, 5, threshold=0.05)
        assert seats.sum() == 0


class TestMetrics:
    """Tests for electoral metrics."""

    def test_gallagher_index(self):
        """Test Gallagher disproportionality index."""
        from electoral_sim.metrics.indices import gallagher_index

        vote_shares = np.array([0.45, 0.35, 0.20])
        seat_shares = np.array([0.55, 0.35, 0.10])

        lsq = gallagher_index(vote_shares, seat_shares)
        assert 0 <= lsq <= 100
        assert lsq > 0  # Some disproportionality

    def test_gallagher_perfect_proportionality(self):
        """Test Gallagher index with perfect proportionality."""
        from electoral_sim.metrics.indices import gallagher_index

        shares = np.array([0.50, 0.30, 0.20])
        lsq = gallagher_index(shares, shares)
        assert lsq == pytest.approx(0.0, abs=0.001)

    def test_effective_number_of_parties(self):
        """Test ENP calculation."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        # Two equal parties
        shares = np.array([0.5, 0.5])
        enp = effective_number_of_parties(shares)
        assert enp == pytest.approx(2.0, abs=0.01)

        # Single dominant party
        shares = np.array([1.0, 0.0])
        enp = effective_number_of_parties(shares)
        assert enp == pytest.approx(1.0, abs=0.01)

    def test_efficiency_gap(self):
        """Test efficiency gap calculation."""
        from electoral_sim.metrics.indices import efficiency_gap

        # Party A wins 3 districts, Party B wins 2
        district_votes_a = np.array([600, 600, 600, 400, 400])
        district_votes_b = np.array([400, 400, 400, 600, 600])
        party_a_seats = np.array([1, 1, 1, 0, 0])  # A wins first 3

        gap = efficiency_gap(district_votes_a, district_votes_b, party_a_seats)
        assert -1 <= gap <= 1


class TestConfig:
    """Tests for configuration classes."""

    def test_config_defaults(self):
        """Test Config with default values."""
        from electoral_sim import Config

        config = Config()
        assert config.n_voters == 100_000
        assert config.n_constituencies == 10
        assert config.electoral_system == "FPTP"

    def test_config_custom(self):
        """Test Config with custom values."""
        from electoral_sim import Config

        config = Config(n_voters=50_000, electoral_system="PR")
        assert config.n_voters == 50_000
        assert config.electoral_system == "PR"

    def test_party_config(self):
        """Test PartyConfig creation."""
        from electoral_sim import PartyConfig

        party = PartyConfig(name="Test Party", position_x=0.3, position_y=-0.2, valence=60)
        assert party.name == "Test Party"
        assert party.position_x == 0.3
        assert party.valence == 60

    def test_config_rejects_invalid_electoral_system(self):
        """Config raises ValueError for unsupported electoral systems."""
        from electoral_sim import Config

        for system in ["IRV", "STV", "INVALID", "MMP"]:
            with pytest.raises(ValueError, match="Unsupported electoral system"):
                Config(n_voters=100, electoral_system=system)

    def test_config_rejects_invalid_allocation_method(self):
        """Config raises ValueError for unsupported allocation methods."""
        from electoral_sim import Config

        for method in ["INVALID", "saintelague", "Hare", "dHondt"]:
            with pytest.raises(ValueError, match="Unknown allocation method"):
                Config(n_voters=100, allocation_method=method)

    @pytest.mark.parametrize("field,value,match", [
        ("n_voters", 0, "n_voters must be positive"),
        ("n_constituencies", 0, "n_constituencies must be positive"),
        ("threshold", 1.5, "threshold must be"),
        ("threshold", -0.1, "threshold must be"),
        ("temperature", 0, "temperature must be positive"),
    ])
    def test_config_rejects_invalid_values(self, field, value, match):
        """Config raises ValueError for out-of-range parameter values."""
        from electoral_sim import Config

        kwargs = {"n_voters": 100, field: value}
        with pytest.raises(ValueError, match=match):
            Config(**kwargs)

    def test_config_rejects_duplicate_party_names(self):
        """Config raises ValueError for duplicate party names."""
        from electoral_sim import Config, PartyConfig

        parties = [
            PartyConfig("Same", 0.0, 0.0),
            PartyConfig("Same", 0.5, 0.5),
        ]
        with pytest.raises(ValueError, match="Duplicate party name"):
            Config(n_voters=100, parties=parties)

    def test_config_rejects_negative_valence(self):
        """Config raises ValueError for negative valence."""
        from electoral_sim import Config, PartyConfig

        parties = [PartyConfig("Bad", 0.0, 0.0, valence=-1)]
        with pytest.raises(ValueError, match="valence must be >= 0"):
            Config(n_voters=100, parties=parties)

    def test_candidate_config(self):
        """CandidateConfig stores candidate-level data."""
        from electoral_sim import CandidateConfig

        c = CandidateConfig("John", "Party A", 5, 0.3, -0.1, 60, True)
        assert c.name == "John"
        assert c.party == "Party A"
        assert c.constituency == 5
        assert c.valence == 60
        assert c.incumbent is True

    def test_config_with_candidates(self):
        """Config accepts optional candidate list."""
        from electoral_sim import Config, CandidateConfig

        candidates = [CandidateConfig("A1", "Party A", 0, valence=60)]
        config = Config(n_voters=100, candidates=candidates)
        assert config.candidates[0].name == "A1"

    def test_config_with_alliances(self):
        """Config accepts optional alliance/bloc definitions."""
        from electoral_sim import Config

        config = Config(n_voters=100, alliances={"Coalition A": ["Party X", "Party Y"]})
        assert config.alliances is not None
        assert "Coalition A" in config.alliances
        assert len(config.alliances["Coalition A"]) == 2

    def test_allocation_methods_config_and_registry_synced(self):
        """VALID_ALLOCATION_METHODS from config matches ALLOCATION_METHODS registry."""
        from electoral_sim.core.config import VALID_ALLOCATION_METHODS
        from electoral_sim.systems.allocation import ALLOCATION_METHODS

        config_set = set(VALID_ALLOCATION_METHODS)
        registry_set = set(ALLOCATION_METHODS.keys())
        assert config_set == registry_set, (
            f"Mismatch: config={sorted(config_set)}, registry={sorted(registry_set)}"
        )


class TestPresets:
    """Tests for country presets."""

    def test_india_preset(self):
        """Test India preset configuration."""
        from electoral_sim import PRESETS

        india = PRESETS["india"]()
        assert india.n_constituencies == 543
        assert india.electoral_system == "FPTP"
        assert len(india.parties) >= 5

    def test_usa_preset(self):
        """Test USA preset configuration."""
        from electoral_sim import PRESETS

        usa = PRESETS["usa"]()
        assert usa.n_constituencies == 435
        assert usa.electoral_system == "FPTP"

    def test_uk_preset(self):
        """Test UK preset configuration."""
        from electoral_sim import PRESETS

        uk = PRESETS["uk"]()
        assert uk.n_constituencies == 650
        assert uk.electoral_system == "FPTP"

    def test_germany_preset(self):
        """Test Germany preset configuration."""
        from electoral_sim import PRESETS

        germany = PRESETS["germany"]()
        # Germany uses MMP (Mixed Member Proportional)
        assert germany.electoral_system in ["MMP", "PR", "FPTP"]


class TestModel:
    """Tests for ElectionModel class."""

    def test_model_creation(self):
        """Test basic model creation."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, n_constituencies=5, seed=42)
        assert model.n_constituencies == 5
        assert len(model.voters) == 1000

    def test_model_from_preset(self):
        """Test model creation from preset."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("india", n_voters=10_000)
        assert model.n_constituencies == 543
        assert len(model.voters) == 10_000

    def test_run_election(self):
        """Test running a basic election."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()

        # Check result structure
        assert results is not None
        assert hasattr(results, '__getitem__')  # dict or ElectionResult (dict-compatible)
        # Check that key results exist
        assert "seats" in results
        assert "turnout" in results

    def test_chainable_api(self):
        """Test chainable API."""
        from electoral_sim import ElectionModel

        model = (
            ElectionModel(n_voters=1000, seed=42)
            .with_system("PR")
            .with_allocation("dhondt")
            .with_threshold(0.05)
        )
        assert model.electoral_system == "PR"
        assert model.allocation_method == "dhondt"
        assert model.threshold == 0.05


class TestElectoralInvariants:
    """Hypothesis property tests for electoral-system invariants."""

    @given(
        votes=st.lists(st.integers(min_value=1, max_value=10000), min_size=2, max_size=10),
        n_seats=st.integers(min_value=1, max_value=100),
    )
    def test_allocation_seat_sum_invariant(self, votes, n_seats):
        """Allocators return exactly n_seats for valid positive votes."""
        from electoral_sim.systems.allocation import (
            dhondt_allocation,
            sainte_lague_allocation,
            hare_quota_allocation,
        )

        votes_arr = np.array(votes, dtype=np.int64)
        assume(votes_arr.sum() > 0)

        for allocator in [dhondt_allocation, sainte_lague_allocation, hare_quota_allocation]:
            seats = allocator(votes_arr, n_seats)
            assert seats.sum() == n_seats, f"{allocator.__name__}: {seats.tolist()}"
            assert np.all(seats >= 0)

    @given(
        votes=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=8),
    )
    def test_enp_is_finite(self, votes):
        """ENP returns finite value for any valid vote shares."""
        from electoral_sim.metrics.indices import effective_number_of_parties

        arr = np.array(votes)
        shares = arr / arr.sum() if arr.sum() > 0 else arr
        result = effective_number_of_parties(shares)
        assert np.isfinite(result)
        assert result >= 1.0

    @given(
        shares=st.lists(st.floats(min_value=0, max_value=1), min_size=2, max_size=8),
    )
    def test_gallagher_is_finite(self, shares):
        """Gallagher returns finite value for any valid equal-length shares."""
        from electoral_sim.metrics.indices import gallagher_index

        v = np.array(shares)
        s = np.roll(v, 1)  # same length, different distribution
        assume(v.sum() > 0)
        result = gallagher_index(v / v.sum(), s / s.sum())
        assert np.isfinite(result)
        assert result >= 0

    @given(
        n_voters=st.integers(min_value=50, max_value=1000),
        seed=st.integers(min_value=0, max_value=9999),
    )
    def test_turnout_in_valid_range(self, n_voters, seed):
        """Turnout is always in [0, 1]."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=n_voters, seed=seed)
        results = model.run_election()
        assert 0.0 <= results["turnout"] <= 1.0

    @given(
        votes=st.lists(st.integers(min_value=1, max_value=10000), min_size=2, max_size=8),
        n_seats=st.integers(min_value=2, max_value=50),
    )
    def test_allocation_non_negative(self, votes, n_seats):
        """Seat allocations contain no negative values."""
        from electoral_sim.systems.allocation import dhondt_allocation, sainte_lague_allocation, hare_quota_allocation

        votes_arr = np.array(votes, dtype=np.int64)
        assume(votes_arr.sum() > 0)

        for allocator in [dhondt_allocation, sainte_lague_allocation, hare_quota_allocation]:
            seats = allocator(votes_arr, n_seats)
            assert np.all(seats >= 0), f"{allocator.__name__}: {seats.tolist()}"


class TestTypeHints:
    """Smoke tests for typing.get_type_hints() on public modules."""

    def test_election_model_type_hints(self):
        """ElectionModel.__init__ type hints are introspectable (TYPE_CHECKING imports may fail)."""
        import typing
        from electoral_sim import ElectionModel

        try:
            hints = typing.get_type_hints(ElectionModel.__init__)
            assert isinstance(hints, dict)
        except NameError:
            pass  # TYPE_CHECKING-only imports (BehaviorEngine, etc.) can't resolve at runtime

    def test_config_type_hints(self):
        """Config.__init__ type hints resolve without error."""
        import typing
        from electoral_sim import Config

        hints = typing.get_type_hints(Config.__init__)
        assert len(hints) > 0

    def test_behavior_engine_type_hints(self):
        """BehaviorEngine.compute_all type hints resolve without error."""
        import typing
        from electoral_sim import BehaviorEngine

        hints = typing.get_type_hints(BehaviorEngine.compute_all)
        assert isinstance(hints, dict)
