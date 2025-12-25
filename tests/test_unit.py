"""
Unit tests for electoral systems and core calculations.
These tests focus on specific functions to improve code coverage.
"""

import pytest
import numpy as np


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
        assert isinstance(results, dict)
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
