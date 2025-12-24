"""
Comprehensive Integration Tests for ElectoralSim

This module tests the full integration of all package components,
ensuring they work together correctly after the repository restructuring.

Test Categories:
1. Import Tests - Verify all public APIs are accessible
2. Model Integration - Core simulation flow
3. Behavior & Dynamics - Voter behavior + opinion dynamics integration
4. Electoral Systems - FPTP, PR, IRV, STV interactions
5. Engine & Metrics - Numba acceleration, indices, coalitions
6. Preset Integration - Country-specific simulations
"""

import pytest
import numpy as np
import polars as pl


# =============================================================================
# 1. IMPORT TESTS - Verify Facade API
# =============================================================================

class TestImports:
    """Test that all public APIs are importable from top-level package."""

    def test_core_imports(self):
        """Test core model and config imports."""
        from electoral_sim import ElectionModel, Config, PartyConfig, PRESETS
        assert ElectionModel is not None
        assert Config is not None
        assert PartyConfig is not None
        assert isinstance(PRESETS, dict)

    def test_preset_imports(self):
        """Test country preset function imports."""
        from electoral_sim import india_config, usa_config, uk_config, germany_config
        assert callable(india_config)
        assert callable(usa_config)

    def test_allocation_imports(self):
        """Test seat allocation method imports."""
        from electoral_sim import (
            dhondt_allocation, sainte_lague_allocation,
            hare_quota_allocation, droop_quota_allocation, allocate_seats
        )
        assert callable(dhondt_allocation)
        assert callable(allocate_seats)

    def test_alternative_systems_imports(self):
        """Test alternative voting system imports."""
        from electoral_sim import (
            irv_election, stv_election, approval_voting,
            condorcet_winner, generate_rankings
        )
        assert callable(irv_election)
        assert callable(stv_election)

    def test_metrics_imports(self):
        """Test metric function imports."""
        from electoral_sim import (
            gallagher_index, effective_number_of_parties, efficiency_gap
        )
        assert callable(gallagher_index)

    def test_behavior_imports(self):
        """Test behavior engine imports."""
        from electoral_sim import (
            BehaviorEngine, ProximityModel, ValenceModel,
            RetrospectiveModel, StrategicVotingModel
        )
        assert BehaviorEngine is not None

    def test_dynamics_imports(self):
        """Test opinion dynamics imports."""
        from electoral_sim import OpinionDynamics
        assert OpinionDynamics is not None

    def test_coalition_imports(self):
        """Test coalition and government imports."""
        from electoral_sim import (
            minimum_winning_coalitions, minimum_connected_winning,
            coalition_strain, form_government,
            collapse_probability, simulate_government_survival, GovernmentSimulator
        )
        assert callable(minimum_winning_coalitions)
        assert callable(collapse_probability)

    def test_india_preset_imports(self):
        """Test India-specific preset imports."""
        from electoral_sim import (
            simulate_india_election, IndiaElectionResult,
            INDIA_STATES, INDIA_PARTIES
        )
        assert callable(simulate_india_election)
        assert isinstance(INDIA_STATES, dict)


# =============================================================================
# 2. MODEL INTEGRATION TESTS
# =============================================================================

class TestModelIntegration:
    """Test core ElectionModel functionality."""

    def test_basic_election(self):
        """Test a basic election can be run."""
        from electoral_sim import ElectionModel
        model = ElectionModel(n_voters=1000, n_constituencies=3, seed=42)
        results = model.run_election()

        assert "turnout" in results
        assert "seats" in results
        assert "gallagher" in results
        assert results["turnout"] > 0

    def test_fptp_system(self):
        """Test FPTP electoral system."""
        from electoral_sim import ElectionModel
        model = ElectionModel(
            n_voters=5000, n_constituencies=5,
            electoral_system="FPTP", seed=42
        )
        results = model.run_election()
        assert results["system"] == "FPTP"
        assert results["seats"].sum() == 5

    def test_pr_system(self):
        """Test PR electoral system with D'Hondt."""
        from electoral_sim import ElectionModel
        model = ElectionModel(
            n_voters=5000, n_constituencies=5,
            electoral_system="PR", allocation_method="dhondt", seed=42
        )
        results = model.run_election()
        assert results["system"] == "PR"
        assert results["seats"].sum() == 5

    def test_chainable_api(self):
        """Test chainable API for model configuration."""
        from electoral_sim import ElectionModel
        results = (
            ElectionModel(n_voters=1000, seed=42)
            .with_system("PR")
            .with_allocation("sainte_lague")
            .run_election()
        )
        assert results["system"] == "PR"

    def test_from_preset(self):
        """Test model creation from country preset."""
        from electoral_sim import ElectionModel
        model = ElectionModel.from_preset("india", n_voters=5000, seed=42)
        assert model.n_constituencies == 543
        assert len(model.parties) > 5

    def test_from_config(self):
        """Test model creation from Config object."""
        from electoral_sim import ElectionModel, Config
        config = Config(n_voters=2000, electoral_system="PR", threshold=0.05, seed=42)
        model = ElectionModel.from_config(config)
        assert model.threshold == 0.05

    def test_batch_simulation(self):
        """Test batch election simulation."""
        from electoral_sim import ElectionModel
        model = ElectionModel(n_voters=1000, n_constituencies=3, seed=42)
        batch_results = model.run_elections_batch(n_runs=5, reset_voters=True)
        assert len(batch_results) >= 5  # May include step results too
        for r in batch_results:
            assert "turnout" in r


# =============================================================================
# 3. BEHAVIOR & DYNAMICS INTEGRATION
# =============================================================================

class TestBehaviorDynamicsIntegration:
    """Test voter behavior and opinion dynamics integration."""

    def test_behavior_engine_integration(self):
        """Test custom BehaviorEngine with ElectionModel."""
        from electoral_sim import ElectionModel, BehaviorEngine, ProximityModel, ValenceModel

        engine = BehaviorEngine()
        engine.add_model(ProximityModel(weight=1.0), weight=1.0)
        engine.add_model(ValenceModel(weight=0.01), weight=1.0)

        model = ElectionModel(n_voters=1000, behavior_engine=engine, seed=42)
        results = model.run_election()
        assert results["turnout"] > 0

    def test_opinion_dynamics_standalone(self):
        """Test OpinionDynamics as a standalone component."""
        from electoral_sim import OpinionDynamics

        od = OpinionDynamics(n_agents=1000, topology="barabasi_albert", m=3, seed=42)
        opinions = od.rng.integers(0, 3, od.n_agents)

        for _ in range(10):
            opinions = od.step(opinions, model="noisy_voter", noise_rate=0.01)

        shares = od.get_opinion_shares(opinions, 3)
        assert shares.sum() == pytest.approx(1.0)

    def test_opinion_dynamics_with_model(self):
        """Test OpinionDynamics integrated with ElectionModel."""
        from electoral_sim import ElectionModel, OpinionDynamics

        od = OpinionDynamics(n_agents=1000, topology="watts_strogatz", k=4, p=0.1, seed=42)
        model = ElectionModel(n_voters=1000, opinion_dynamics=od, seed=42)

        # Run a step to trigger opinion dynamics
        model.step()
        results = model.run_election()
        assert results["turnout"] > 0


# =============================================================================
# 4. ELECTORAL SYSTEMS INTEGRATION
# =============================================================================

class TestElectoralSystemsIntegration:
    """Test various electoral system methods."""

    def test_allocation_methods(self):
        """Test all seat allocation methods produce valid results."""
        from electoral_sim import (
            dhondt_allocation, sainte_lague_allocation,
            hare_quota_allocation, droop_quota_allocation
        )

        votes = np.array([10000, 8000, 5000, 2000])
        n_seats = 10

        for allocator in [dhondt_allocation, sainte_lague_allocation,
                          hare_quota_allocation, droop_quota_allocation]:
            seats = allocator(votes, n_seats)
            assert seats.sum() == n_seats
            assert all(s >= 0 for s in seats)

    def test_threshold_application(self):
        """Test that electoral threshold filters parties."""
        from electoral_sim import allocate_seats

        votes = np.array([10000, 1000, 500])  # Third party below 5%
        n_seats = 10

        seats = allocate_seats(votes, n_seats, method="dhondt", threshold=0.05)
        assert seats[2] == 0  # Party below threshold gets no seats

    def test_irv_election(self):
        """Test Instant Runoff Voting."""
        from electoral_sim import irv_election, generate_rankings

        np.random.seed(42)
        utilities = np.random.randn(500, 4)
        rankings = generate_rankings(utilities)

        result = irv_election(rankings, 4)
        assert "winner" in result
        assert 0 <= result["winner"] < 4

    def test_stv_election(self):
        """Test Single Transferable Vote."""
        from electoral_sim import stv_election, generate_rankings

        np.random.seed(42)
        utilities = np.random.randn(500, 5)
        rankings = generate_rankings(utilities)

        result = stv_election(rankings, 5, n_seats=3)
        assert len(result["elected"]) == 3

    def test_condorcet_winner(self):
        """Test Condorcet winner calculation."""
        from electoral_sim import condorcet_winner, generate_rankings

        np.random.seed(42)
        utilities = np.random.randn(500, 4)
        rankings = generate_rankings(utilities)

        result = condorcet_winner(rankings, 4)
        assert "condorcet_winner" in result
        assert "pairwise_matrix" in result


# =============================================================================
# 5. ENGINE & METRICS INTEGRATION
# =============================================================================

class TestEngineMetricsIntegration:
    """Test engine acceleration and metric calculations."""

    def test_numba_acceleration(self):
        """Test Numba-accelerated functions work correctly."""
        from electoral_sim.engine.numba_accel import (
            dhondt_fast, sainte_lague_fast, fptp_count_fast, NUMBA_AVAILABLE
        )

        votes = np.array([10000, 8000, 5000], dtype=np.int64)
        seats = dhondt_fast(votes, 10)
        assert seats.sum() == 10

    def test_gallagher_index(self):
        """Test Gallagher index calculation."""
        from electoral_sim import gallagher_index

        vote_shares = np.array([0.4, 0.35, 0.25])
        seat_shares = np.array([0.5, 0.4, 0.1])

        gal = gallagher_index(vote_shares, seat_shares)
        assert gal > 0

    def test_effective_number_of_parties(self):
        """Test ENP calculation."""
        from electoral_sim import effective_number_of_parties

        shares = np.array([0.5, 0.5])
        enp = effective_number_of_parties(shares)
        assert enp == pytest.approx(2.0)

        shares = np.array([1.0])
        enp = effective_number_of_parties(shares)
        assert enp == pytest.approx(1.0)

    def test_coalition_formation(self):
        """Test coalition formation logic."""
        from electoral_sim import (
            minimum_winning_coalitions, minimum_connected_winning,
            coalition_strain, form_government
        )

        seats = np.array([45, 35, 15, 5])
        positions = np.array([0.6, -0.2, 0.1, -0.5])
        names = ["Right", "Center-Left", "Center", "Left"]

        mwcs = minimum_winning_coalitions(seats)
        assert len(mwcs) > 0

        gov = form_government(seats, positions, names)
        assert gov["success"]
        assert gov["seats"] >= 51

    def test_government_stability(self):
        """Test government stability simulation."""
        from electoral_sim import (
            collapse_probability, simulate_government_survival, GovernmentSimulator
        )

        prob = collapse_probability(30, strain=0.3, stability=0.7, model="sigmoid")
        assert 0 <= prob <= 1

        survival = simulate_government_survival(0.3, 0.7, n_simulations=50, seed=42)
        assert "mean_survival" in survival

        gov_sim = GovernmentSimulator(strain=0.3, stability=0.7, seed=42)
        months = gov_sim.simulate(max_months=60)
        assert months > 0


# =============================================================================
# 6. PRESET & GENERIC FEATURE INTEGRATION
# =============================================================================

class TestPresetFeatureIntegration:
    """Test country presets and generic features like NOTA."""

    def test_nota_feature(self):
        """Test NOTA (None of the Above) functionality."""
        from electoral_sim import ElectionModel

        model = ElectionModel(
            n_voters=1000, n_constituencies=2,
            include_nota=True, seed=42
        )
        results = model.run_election()

        party_names = model.parties.df["name"].to_list()
        assert "NOTA" in party_names

        nota_idx = party_names.index("NOTA")
        assert results["seats"][nota_idx] == 0

    def test_reserved_constituency_feature(self):
        """Test reserved constituency constraints."""
        from electoral_sim import ElectionModel

        parties = [
            {"name": "General", "position_x": 0.2, "position_y": 0.2},
            {"name": "Reserved", "position_x": -0.2, "position_y": -0.2},
        ]
        constraints = {0: ["Reserved"]}

        model = ElectionModel(
            n_voters=1000, n_constituencies=2,
            parties=parties, constituency_constraints=constraints, seed=42
        )
        results = model.run_election()

        # The Reserved party should win the reserved constituency
        assert results["seats"][1] >= 1

    def test_india_simulation(self):
        """Test India-specific election simulation."""
        from electoral_sim import simulate_india_election

        result = simulate_india_election(
            n_voters_per_constituency=100,  # Small for test speed
            seed=42, verbose=False
        )

        assert sum(result.seats.values()) == 543
        assert result.nda_seats >= 0
        assert result.india_seats >= 0

    def test_voter_knowledge_attributes(self):
        """Test political_knowledge and misinfo_susceptibility voter attributes."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        voter_df = model.voters.df

        # Check columns exist
        assert "political_knowledge" in voter_df.columns
        assert "misinfo_susceptibility" in voter_df.columns

        # Check value ranges
        knowledge = voter_df["political_knowledge"].to_numpy()
        assert knowledge.min() >= 0
        assert knowledge.max() <= 100

        susceptibility = voter_df["misinfo_susceptibility"].to_numpy()
        assert susceptibility.min() >= 0
        assert susceptibility.max() <= 1

    def test_wave_elections_national_mood(self):
        """Test national_mood parameter for wave elections."""
        from electoral_sim import ElectionModel

        parties = [
            {"name": "Incumbent", "position_x": 0.2, "valence": 50, "incumbent": True},
            {"name": "Challenger", "position_x": -0.2, "valence": 50, "incumbent": False},
        ]

        # Strong anti-incumbent wave
        model_wave = ElectionModel(
            n_voters=2000, n_constituencies=5, parties=parties,
            national_mood=-20.0, seed=42
        )
        # No wave
        model_neutral = ElectionModel(
            n_voters=2000, n_constituencies=5, parties=parties,
            national_mood=0.0, seed=42
        )

        r_wave = model_wave.run_election()
        r_neutral = model_neutral.run_election()

        # Anti-incumbent wave should hurt incumbent party
        assert r_wave["seats"][0] <= r_neutral["seats"][0]

    def test_junior_partner_penalty(self):
        """Test junior_partner_penalty coalition function."""
        from electoral_sim.engine.coalition import junior_partner_penalty
        import numpy as np

        seats = np.array([200, 50, 30])  # 3-party coalition
        coalition = [0, 1, 2]

        penalties = junior_partner_penalty(seats, coalition)

        # Dominant partner gets bonus
        assert penalties[0] > 0

        # Junior partners get penalties (negative values)
        assert penalties[1] < 0
        assert penalties[2] < 0

        # Smallest partner gets largest penalty
        assert penalties[2] <= penalties[1]


# =============================================================================
# 7. END-TO-END WORKFLOW TESTS
# =============================================================================

class TestEndToEndWorkflows:
    """Test complete simulation workflows."""

    def test_full_election_cycle(self):
        """Test a complete election cycle with metrics."""
        from electoral_sim import ElectionModel, gallagher_index, effective_number_of_parties

        model = ElectionModel(n_voters=5000, n_constituencies=10, seed=42)
        results = model.run_election()

        # Verify all expected outputs
        assert results["turnout"] > 0.5
        assert results["gallagher"] >= 0
        assert results["enp_votes"] >= 1
        assert results["enp_seats"] >= 1
        assert results["seats"].sum() <= 10  # May be less if some constituencies have no votes

    def test_comparative_analysis(self):
        """Test comparing FPTP vs PR outcomes."""
        from electoral_sim import ElectionModel

        # Same voters, different systems
        model_fptp = ElectionModel(
            n_voters=5000, n_constituencies=10,
            electoral_system="FPTP", seed=42
        )
        model_pr = ElectionModel(
            n_voters=5000, n_constituencies=10,
            electoral_system="PR", seed=42
        )

        r_fptp = model_fptp.run_election()
        r_pr = model_pr.run_election()

        # PR should generally be more proportional
        assert r_pr["gallagher"] <= r_fptp["gallagher"] + 20  # Rough heuristic

    def test_monte_carlo_simulation(self):
        """Test Monte Carlo style batch simulation."""
        from electoral_sim import ElectionModel
        import numpy as np

        model = ElectionModel(n_voters=2000, n_constituencies=5, seed=42)
        batch_results = model.run_elections_batch(n_runs=10, reset_voters=True)

        turnouts = [r["turnout"] for r in batch_results]
        assert np.std(turnouts) > 0  # Some variation across runs


# =============================================================================
# MAIN - Run tests directly
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
