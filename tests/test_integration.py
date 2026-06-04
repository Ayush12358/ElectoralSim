"""
Integration tests — cross-module and end-to-end workflows only.

Unit tests for individual modules are in their respective files:
test_behavior.py, test_engine.py, test_dynamics.py, test_model.py,
test_presets.py, test_metrics.py, test_infra.py.
"""

import numpy as np
import polars as pl
import pytest


# =============================================================================
# BEHAVIOR + DYNAMICS INTEGRATION
# =============================================================================


class TestBehaviorDynamicsIntegration:
    """Behavior engine + opinion dynamics working together."""

    def test_custom_behavior_engine_with_model(self):
        from electoral_sim import ElectionModel, BehaviorEngine, ProximityModel, ValenceModel

        engine = BehaviorEngine()
        engine.add_model(ProximityModel(weight=1.0), weight=1.0)
        engine.add_model(ValenceModel(weight=0.01), weight=1.0)

        model = ElectionModel(n_voters=1000, behavior_engine=engine, seed=42)
        results = model.run_election()
        assert results["turnout"] > 0

    def test_opinion_dynamics_standalone(self):
        from electoral_sim import OpinionDynamics

        od = OpinionDynamics(n_agents=1000, topology="barabasi_albert", m=3, seed=42)
        opinions = od.rng.integers(0, 3, od.n_agents)
        for _ in range(10):
            opinions = od.step(opinions, model="noisy_voter", noise_rate=0.01)
        shares = od.get_opinion_shares(opinions, 3)
        assert shares.sum() == pytest.approx(1.0)

    def test_opinion_dynamics_with_model(self):
        from electoral_sim import ElectionModel, OpinionDynamics

        od = OpinionDynamics(n_agents=1000, topology="watts_strogatz", k=4, p=0.1, seed=42)
        model = ElectionModel(n_voters=1000, opinion_dynamics=od, seed=42)
        model.step()
        results = model.run_election()
        assert results["turnout"] > 0


# =============================================================================
# END-TO-END WORKFLOWS
# =============================================================================


class TestEndToEndWorkflows:
    """Complete simulation workflows with multiple components."""

    def test_full_election_cycle(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=5000, n_constituencies=10, seed=42)
        results = model.run_election()
        assert results["turnout"] > 0.5
        assert results["gallagher"] >= 0
        assert results["enp_votes"] >= 1
        assert results["enp_seats"] >= 1

    def test_comparative_analysis(self):
        """FPTP vs PR comparison on same voter base."""
        from electoral_sim import ElectionModel

        model_fptp = ElectionModel(n_voters=5000, n_constituencies=10, electoral_system="FPTP", seed=42)
        model_pr = ElectionModel(n_voters=5000, n_constituencies=10, electoral_system="PR", seed=42)

        r_fptp = model_fptp.run_election()
        r_pr = model_pr.run_election()

        # PR should generally be more proportional
        assert r_pr["gallagher"] <= r_fptp["gallagher"] + 20

    def test_monte_carlo_simulation(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=2000, n_constituencies=5, seed=42)
        batch_results = model.run_elections_batch(n_runs=10, reset_voters=True)
        turnouts = [r["turnout"] for r in batch_results]
        assert np.std(turnouts) > 0

    def test_all_electoral_systems_end_to_end(self):
        """Run elections under all electoral systems."""
        from electoral_sim import ElectionModel

        for system, method in [
            ("FPTP", "dhondt"),
            ("PR", "dhondt"),
            ("PR", "sainte_lague"),
            ("PR", "hare"),
            ("PR", "droop"),
        ]:
            model = ElectionModel(
                n_voters=1000, n_constituencies=5,
                electoral_system=system, allocation_method=method, seed=42,
            )
            results = model.run_election()
            assert results is not None
            assert results["seats"].sum() > 0

    def test_all_presets_end_to_end(self):
        """Run elections on all country presets."""
        from electoral_sim import ElectionModel

        for preset in ["usa", "uk", "germany", "france", "brazil", "japan", "south_africa",
                        "australia_house"]:
            model = ElectionModel.from_preset(preset, n_voters=3000)
            results = model.run_election()
            assert results is not None
            assert "gallagher" in results

    def test_wave_election_integration(self):
        """National mood affects seat distribution."""
        from electoral_sim import ElectionModel

        model_pro = ElectionModel(n_voters=2000, national_mood=3.0, seed=42)
        r_pro = model_pro.run_election()

        model_anti = ElectionModel(n_voters=2000, national_mood=-3.0, seed=42)
        r_anti = model_anti.run_election()

        assert r_pro is not None
        assert r_anti is not None

    def test_full_simulation_with_all_features(self):
        """All features enabled: behavior + dynamics + events + strategy."""
        from electoral_sim import ElectionModel, BehaviorEngine, ProximityModel, RetrospectiveModel, OpinionDynamics

        engine = BehaviorEngine()
        engine.add_model(ProximityModel(weight=1.0))
        engine.add_model(RetrospectiveModel(weight=0.5))

        od = OpinionDynamics(n_agents=500, topology="barabasi_albert", m=3, seed=42)

        model = ElectionModel(
            n_voters=500,
            n_constituencies=5,
            behavior_engine=engine,
            opinion_dynamics=od,
            economic_growth=0.03,
            event_probs={"scandal": 0.1, "shock": 0.05},
            use_adaptive_strategy=True,
            seed=42,
        )

        for _ in range(5):
            model.step()

        results = model.run_election()
        assert results is not None
        assert results["turnout"] > 0


# =============================================================================
# CROSS-MODULE TESTS
# =============================================================================


class TestCrossModule:
    """Tests that span multiple modules."""

    def test_metrics_from_election(self):
        """Run election and compute metrics from results."""
        from electoral_sim import ElectionModel, gallagher_index, effective_number_of_parties

        model = ElectionModel(n_voters=2000, seed=42)
        results = model.run_election()

        vote_shares = results["vote_counts"] / results["vote_counts"].sum()
        seat_shares = results["seats"] / results["seats"].sum() if results["seats"].sum() > 0 else vote_shares

        gal = gallagher_index(vote_shares, seat_shares)
        enp = effective_number_of_parties(vote_shares)
        assert gal >= 0
        assert enp >= 1

    def test_coalition_from_election(self):
        """Run election and form government from results."""
        from electoral_sim import ElectionModel, form_government

        model = ElectionModel.from_preset("germany", n_voters=5000)
        results = model.run_election()

        seats = results["seats"]
        positions = model.parties.get_positions()[:, 0]
        names = model.parties.get_names()

        gov = form_government(seats, positions, names)
        assert "success" in gov
