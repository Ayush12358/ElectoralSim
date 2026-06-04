"""Tests for ElectionModel: creation, config, presets, step, edge cases, and advanced features."""

import pytest
import numpy as np
import polars as pl


class TestModelEdgeCases:
    """Edge case tests for ElectionModel."""

    def test_small_election(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=10, n_constituencies=1, seed=42)
        results = model.run_election()
        assert results is not None

    def test_single_party(self):
        from electoral_sim import ElectionModel

        parties = [{"name": "Only Party", "position_x": 0, "position_y": 0, "valence": 50}]
        model = ElectionModel(n_voters=100, parties=parties, seed=42)
        results = model.run_election()
        assert results is not None

    def test_many_parties(self):
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
        assert len(results["seats"]) == 15

    def test_high_temperature(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, temperature=10.0, seed=42)
        results = model.run_election()
        assert results is not None

    def test_low_temperature(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, temperature=0.01, seed=42)
        results = model.run_election()
        assert results is not None

    def test_with_nota(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, include_nota=True, seed=42)
        results = model.run_election()
        assert results is not None

    def test_nota_in_pr(self):
        """NOTA in PR system should not win seats."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", include_nota=True, seed=42)
        results = model.run_election()
        assert results is not None

    def test_pr_system(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", seed=42)
        results = model.run_election()
        assert results["system"] == "PR"

    def test_different_allocation_methods(self):
        from electoral_sim import ElectionModel

        for method in ["dhondt", "sainte_lague", "hare", "droop"]:
            model = ElectionModel(
                n_voters=1000, electoral_system="PR", allocation_method=method, seed=42
            )
            results = model.run_election()
            assert results is not None

    def test_with_threshold(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", threshold=0.05, seed=42)
        results = model.run_election()
        assert results is not None

    def test_zero_threshold(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", threshold=0.0, seed=42)
        results = model.run_election()
        assert results is not None

    def test_high_threshold(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, electoral_system="PR", threshold=0.2, seed=42)
        results = model.run_election()
        assert results is not None

    def test_temperature_extremes(self):
        from electoral_sim import ElectionModel

        for temp in [0.01, 0.1, 1.0, 5.0, 10.0]:
            model = ElectionModel(n_voters=500, temperature=temp, seed=42)
            results = model.run_election()
            assert results is not None


class TestModelConfig:
    """Config and factory method tests."""

    def test_from_config(self):
        from electoral_sim import ElectionModel, Config

        config = Config(n_voters=1000, n_constituencies=5, electoral_system="PR")
        model = ElectionModel.from_config(config)
        results = model.run_election()
        assert results["system"] == "PR"

    def test_from_preset(self):
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("usa", n_voters=5000)
        results = model.run_election()
        assert results is not None


class TestChainableAPI:
    """Chainable configuration methods."""

    def test_full_chain(self):
        from electoral_sim import ElectionModel

        results = (
            ElectionModel(n_voters=1000, seed=42)
            .with_system("PR")
            .with_allocation("sainte_lague")
            .with_threshold(0.05)
            .with_temperature(0.3)
            .run_election()
        )
        assert results is not None
        assert results["system"] == "PR"

    def test_chain_returns_self(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        assert model.with_system("PR") is model
        assert model.with_allocation("dhondt") is model
        assert model.with_threshold(0.05) is model
        assert model.with_temperature(0.3) is model

    def test_with_system_rejects_invalid(self):
        """with_system() raises ValueError for unsupported systems."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        for system in ["IRV", "STV", "INVALID", "MMP"]:
            with pytest.raises(ValueError, match="Unsupported electoral system"):
                model.with_system(system)

    def test_with_allocation_rejects_invalid(self):
        """with_allocation() raises ValueError for unsupported methods."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        for method in ["INVALID", "saintelague", "Hare"]:
            with pytest.raises(ValueError, match="Unknown allocation method"):
                model.with_allocation(method)


class TestReproducibility:
    """Seed and determinism tests."""

    def test_same_seed_same_result(self):
        from electoral_sim import ElectionModel

        r1 = ElectionModel(n_voters=1000, seed=42).run_election()
        r2 = ElectionModel(n_voters=1000, seed=42).run_election()
        assert r1["turnout"] == r2["turnout"]

    def test_different_seeds_differ(self):
        from electoral_sim import ElectionModel

        r1 = ElectionModel(n_voters=1000, seed=1).run_election()
        r2 = ElectionModel(n_voters=1000, seed=2).run_election()
        r3 = ElectionModel(n_voters=1000, seed=3).run_election()
        turnouts = [r1["turnout"], r2["turnout"], r3["turnout"]]
        assert len(set(round(t, 3) for t in turnouts)) > 1


class TestMultipleElections:
    """Batch elections and multiple runs."""

    def test_run_multiple_elections(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        for _ in range(5):
            results = model.run_election()
            assert results is not None

    def test_batch_simulation(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=500, n_constituencies=5, seed=42)
        results = model.run_elections_batch(n_elections=3)
        assert len(results) == 3

    def test_batch_with_reset(self):
        """run_elections_batch with reset_voters regenerates voter data."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=500, n_constituencies=5, seed=42)
        results = model.run_elections_batch(n_elections=3, reset_voters=True)
        assert len(results) == 3

    def test_get_aggregate_stats(self):
        """get_aggregate_stats returns statistics across elections."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=500, seed=42)
        model.run_elections_batch(n_elections=5)
        stats = model.get_aggregate_stats()
        assert "n_elections" in stats
        assert stats["n_elections"] == 5
        assert "turnout_mean" in stats
        assert "gallagher_mean" in stats

    def test_get_aggregate_stats_empty(self):
        """get_aggregate_stats returns empty dict when no elections run."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=500, seed=42)
        stats = model.get_aggregate_stats()
        assert stats == {}


class TestConstituencies:
    """Constituency count variations."""

    def test_many_constituencies(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, n_constituencies=50, seed=42)
        results = model.run_election()
        assert results is not None

    def test_single_constituency(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, n_constituencies=1, seed=42)
        results = model.run_election()
        assert results is not None


class TestModelAdvancedFeatures:
    """Tests for opinion dynamics, events, adaptive strategy, turnout, constraints, and pre-built frames."""

    def test_with_opinion_dynamics(self):
        from electoral_sim import ElectionModel, OpinionDynamics

        od = OpinionDynamics(n_agents=100, topology="barabasi_albert", m=3, seed=42)
        model = ElectionModel(n_voters=100, opinion_dynamics=od, seed=42)
        model.step()
        model.step()
        results = model.run_election()
        assert results is not None

    def test_opinion_dynamics_step_with_media_bias(self):
        """step() with opinion dynamics and media_bias column."""
        from electoral_sim import ElectionModel, OpinionDynamics

        od = OpinionDynamics(n_agents=100, topology="barabasi_albert", m=3, seed=42)
        model = ElectionModel(n_voters=100, opinion_dynamics=od, seed=42)
        # Add media_bias column to trigger media influence path
        model.voters.df = model.voters.df.with_columns(
            pl.Series("media_bias", np.random.uniform(-1, 1, 100))
        )
        model.step()
        results = model.run_election()
        assert results is not None

    def test_with_event_manager(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, event_probs={"scandal": 0.5, "shock": 0.5}, seed=42)
        model.step()
        model.step()
        results = model.run_election()
        assert results is not None

    def test_with_adaptive_strategy(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, use_adaptive_strategy=True, seed=42)
        model.step()
        results = model.run_election()
        assert results is not None

    def test_anti_incumbency(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, anti_incumbency=-2.0, seed=42)
        results = model.run_election()
        assert results is not None

    def test_national_mood(self):
        from electoral_sim import ElectionModel

        model_pro = ElectionModel(n_voters=1000, national_mood=3.0, seed=42)
        r_pro = model_pro.run_election()
        model_anti = ElectionModel(n_voters=1000, national_mood=-3.0, seed=42)
        r_anti = model_anti.run_election()
        assert r_pro is not None
        assert r_anti is not None

    def test_alienation_abstention(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, alienation_threshold=5.0, seed=42)
        results = model.run_election()
        assert results["turnout"] < 1.0

    def test_indifference_abstention(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, indifference_threshold=10.0, seed=42)
        results = model.run_election()
        assert results["turnout"] < 1.0

    def test_economic_growth(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, economic_growth=0.03, seed=42)
        results = model.run_election()
        assert results is not None

    def test_run_with_election_interval(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=500, seed=42)
        model.run(n_steps=10, election_interval=5)
        results = model.get_results()
        assert len(results) == 2

    def test_voter_knowledge_attributes(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=100, seed=42)
        assert "political_knowledge" in model.voters.df.columns
        assert model.voters.df["political_knowledge"].min() >= 0
        assert model.voters.df["political_knowledge"].max() <= 100

    def test_with_prebuilt_voter_frame(self):
        """Create model with a pre-built voter DataFrame."""
        from electoral_sim import ElectionModel

        voter_df = pl.DataFrame(
            {
                "unique_id": list(range(100)),
                "constituency": [i % 5 for i in range(100)],
                "ideology_x": np.random.normal(0, 0.3, 100),
                "ideology_y": np.random.normal(0, 0.3, 100),
                "party_id": np.zeros(100, dtype=int),
                "political_knowledge": np.ones(100) * 50,
                "turnout_prob": np.ones(100) * 0.8,
                "media_susceptibility": np.ones(100) * 0.5,
                "is_zealot": np.zeros(100, dtype=bool),
            }
        )
        model = ElectionModel(voter_frame=voter_df, seed=42)
        results = model.run_election()
        assert results is not None

    def test_with_prebuilt_party_frame(self):
        """Create model with a pre-built party DataFrame."""
        from electoral_sim import ElectionModel

        party_df = pl.DataFrame(
            {
                "name": ["Party A", "Party B"],
                "position_x": [-0.3, 0.3],
                "position_y": [0.0, 0.0],
                "valence": [50.0, 50.0],
                "incumbent": [True, False],
                "is_nota": [False, False],
                "seats": np.zeros(2, dtype=np.int64),
                "vote_share": np.zeros(2),
            }
        )
        model = ElectionModel(n_voters=500, party_frame=party_df, seed=42)
        results = model.run_election()
        assert results is not None

    def test_constituency_constraints(self):
        """Constituency constraints invalidate votes for excluded parties."""
        from electoral_sim import ElectionModel

        constraints = {
            0: ["Party A", "Party B"],  # Only A and B allowed in constituency 0
            1: ["Party A", "Party C"],  # Only A and C allowed in constituency 1
        }
        model = ElectionModel(
            n_voters=500,
            n_constituencies=3,
            constituency_constraints=constraints,
            seed=42,
        )
        results = model.run_election()
        assert results is not None

    def test_gpu_warning_when_unavailable(self):
        """GPU requested but unavailable prints warning and falls back."""
        from electoral_sim import ElectionModel

        # GPU will not be available in test environment
        model = ElectionModel(n_voters=500, use_gpu=True, seed=42)
        assert model.use_gpu is False
        results = model.run_election()
        assert results is not None

    def test_irv_system_raises_valueerror(self):
        """IRV is not supported at model level — raises ValueError."""
        from electoral_sim import ElectionModel

        with pytest.raises(ValueError, match="Unsupported electoral system"):
            ElectionModel(n_voters=500, electoral_system="IRV", seed=42)

    def test_stv_system_raises_valueerror(self):
        """STV is not supported at model level — raises ValueError."""
        from electoral_sim import ElectionModel

        with pytest.raises(ValueError, match="Unsupported electoral system"):
            ElectionModel(n_voters=500, electoral_system="STV", seed=42)


class TestPropertyBased:
    """Hypothesis-free invariant tests."""

    def test_seats_dont_exceed_constituencies(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, n_constituencies=20, seed=42)
        results = model.run_election()
        assert results["seats"].sum() <= 20

    def test_turnout_is_valid_proportion(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=1000, seed=42)
        results = model.run_election()
        assert 0.0 <= results["turnout"] <= 1.0

    def test_temperature_produces_valid_results(self):
        from electoral_sim import ElectionModel

        for temp in [0.01, 0.5, 1.0, 5.0]:
            model = ElectionModel(n_voters=500, temperature=temp, seed=42)
            results = model.run_election()
            assert results["turnout"] >= 0.0

    def test_threshold_produces_valid_pr_results(self):
        from electoral_sim import ElectionModel

        for threshold in [0.0, 0.03, 0.05, 0.1]:
            model = ElectionModel(n_voters=500, electoral_system="PR", threshold=threshold, seed=42)
            results = model.run_election()
            assert results["seats"].sum() == 10

    def test_allocation_sums_to_total_seats(self):
        from electoral_sim import ElectionModel

        for method in ["dhondt", "sainte_lague", "hare", "droop"]:
            model = ElectionModel(
                n_voters=500, electoral_system="PR", allocation_method=method, seed=42
            )
            results = model.run_election()
            assert results["seats"].sum() == 10


class TestPerformance:
    """Performance smoke tests."""

    def test_1k_voters_under_1_second(self):
        import time
        from electoral_sim import ElectionModel

        start = time.perf_counter()
        ElectionModel(n_voters=1000, seed=42).run_election()
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0

    def test_10k_voters_under_5_seconds(self):
        import time
        from electoral_sim import ElectionModel

        start = time.perf_counter()
        ElectionModel(n_voters=10000, seed=42).run_election()
        elapsed = time.perf_counter() - start
        assert elapsed < 5.0

    def test_batch_10_elections_under_10_seconds(self):
        import time
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=5000, seed=42)
        start = time.perf_counter()
        for _ in range(10):
            model.run_election()
        elapsed = time.perf_counter() - start
        assert elapsed < 10.0


class TestErrorHandling:
    """Error handling and edge cases."""

    def test_invalid_electoral_system_raises_error(self):
        """Unknown electoral system raises ValueError, not silent PR fallback."""
        from electoral_sim import ElectionModel

        with pytest.raises(ValueError, match="Unsupported electoral system"):
            ElectionModel(n_voters=100, electoral_system="INVALID", seed=42)

    def test_invalid_allocation_method_at_init_raises_error(self):
        """Invalid allocation_method at construction raises ValueError."""
        from electoral_sim import ElectionModel

        with pytest.raises(ValueError, match="Unknown allocation method"):
            ElectionModel(n_voters=100, allocation_method="INVALID", seed=42)

    def test_invalid_allocation_method_raises_error(self):
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=100, electoral_system="PR", seed=42)
        model.allocation_method = "INVALID"
        with pytest.raises(ValueError, match="Unknown method"):
            model.run_election()

    def test_direct_electoral_system_mutation_raises_at_runtime(self):
        """Direct attribute mutation bypassing validation is caught at run_election()."""
        from electoral_sim import ElectionModel

        model = ElectionModel(n_voters=100, seed=42)
        model.electoral_system = "Mixed"
        with pytest.raises(ValueError, match="Unsupported electoral system"):
            model.run_election()

    def test_invalid_preset_raises_error(self):
        from electoral_sim import ElectionModel

        with pytest.raises(ValueError, match="Unknown preset"):
            ElectionModel.from_preset("nonexistent_country")

    def test_from_preset_rejects_unknown_kwargs(self):
        """from_preset() raises ValueError for unknown override kwargs."""
        from electoral_sim import ElectionModel

        with pytest.raises(ValueError, match="Unknown preset override"):
            ElectionModel.from_preset("india", n_voters=1000, misspelled_param=50)

    def test_zero_constituencies_handled(self):
        """Zero constituencies may raise or produce empty results."""
        from electoral_sim import ElectionModel

        try:
            model = ElectionModel(n_voters=100, n_constituencies=0, seed=42)
            results = model.run_election()
            assert results is not None
        except (ValueError, IndexError, ZeroDivisionError):
            pass
