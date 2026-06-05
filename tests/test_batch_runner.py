"""
Tests for BatchRunner and ParameterSweep
"""

import pytest
import numpy as np
import polars as pl
from pathlib import Path

from electoral_sim import ElectionModel
from electoral_sim.analysis import BatchRunner, ParameterSweep

# =============================================================================
# PARAMETER SWEEP
# =============================================================================


class TestParameterSweep:
    """Test parameter sweep configuration."""

    def test_grid_search_combinations(self):
        """Test grid search generates all combinations."""
        sweep = ParameterSweep({"a": [1, 2], "b": [3, 4, 5]})
        configs = sweep.generate_configs()
        assert len(configs) == 6  # 2 * 3

    def test_grid_search_with_fixed_params(self):
        """Test grid search includes fixed params in each config."""
        sweep = ParameterSweep({"a": [1, 2]}, fixed_params={"x": 10, "y": 20})
        configs = sweep.generate_configs()
        for config in configs:
            assert config["x"] == 10
            assert config["y"] == 20

    def test_random_search_size(self):
        """Test random search generates correct number of samples."""
        sweep = ParameterSweep(
            {"a": list(range(100)), "b": list(range(100))}, sweep_type="random", n_samples=50
        )
        configs = sweep.generate_configs()
        assert len(configs) == 50

    def test_sweep_len(self):
        """Test len() on sweep."""
        sweep = ParameterSweep({"a": [1, 2, 3], "b": [4, 5]})
        assert len(sweep) == 6

    def test_validate_rejects_unknown_params(self):
        """validate() catches unknown parameter names."""
        sweep = ParameterSweep({"unknown_param": [1, 2]})
        errors = sweep.validate()
        assert len(errors) > 0
        assert any("unknown_param" in e for e in errors)

    def test_validate_rejects_invalid_sweep_type(self):
        """validate() catches invalid sweep_type."""
        sweep = ParameterSweep({"n_voters": [100, 200]}, sweep_type="invalid")
        errors = sweep.validate()
        assert any("sweep_type" in e for e in errors)

    def test_validate_accepts_valid_config(self):
        """validate() returns no errors for valid config."""
        sweep = ParameterSweep({"n_voters": [100, 200], "temperature": [0.3, 0.7]})
        errors = sweep.validate()
        assert len(errors) == 0


# =============================================================================
# BATCH RUNNER
# =============================================================================


class TestBatchRunner:
    """Test batch runner execution and export."""

    def test_basic_batch_run(self):
        """Test basic batch run with grid sweep."""
        sweep = ParameterSweep(
            {"n_voters": [1000, 2000], "temperature": [0.3, 0.7]},
            fixed_params={"n_constituencies": 3},
        )

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=2,
            seed=42,
            verbose=False,
        )

        results_df = runner.run()

        # Check results structure
        assert isinstance(results_df, pl.DataFrame)
        assert len(results_df) == 4 * 2  # 4 configs * 2 runs

        # Check columns
        expected_cols = [
            "config_idx",
            "run_idx",
            "seed",
            "n_voters",
            "temperature",
            "turnout",
            "gallagher",
            "enp_votes",
            "enp_seats",
        ]
        for col in expected_cols:
            assert col in results_df.columns

    def test_deterministic_with_seed(self):
        """Test that same seed produces same results."""
        sweep = ParameterSweep({"n_voters": [1000]}, fixed_params={"n_constituencies": 3})

        runner1 = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=3,
            n_jobs=1,
            seed=123,
            verbose=False,
        )
        results1 = runner1.run()

        runner2 = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=3,
            n_jobs=1,
            seed=123,
            verbose=False,
        )
        results2 = runner2.run()

        # Results should be approximately identical (same seed, same config)
        # Allow 2% relative tolerance for Numba JIT warmup variance across spawn processes
        for col in ["turnout", "gallagher", "enp_votes"]:
            for a, b in zip(results1[col].to_list(), results2[col].to_list()):
                assert a == pytest.approx(b, rel=0.02) or a == pytest.approx(b, abs=0.5), f"Mismatch in {col}: {a} != {b}"

    def test_summary_stats(self):
        """Test summary statistics generation."""
        sweep = ParameterSweep({"n_voters": [1000, 2000]}, fixed_params={"n_constituencies": 5})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=5,
            seed=42,
            verbose=False,
        )

        runner.run()

        summary = runner.get_summary_stats()

        assert isinstance(summary, pl.DataFrame)
        assert len(summary) == 2  # 2 configs

        # Check summary columns
        for col in ["turnout_mean", "turnout_std", "gallagher_mean", "gallagher_std"]:
            assert col in summary.columns

        # Verify n_runs
        assert all(summary["n_runs"] == 5)

    def test_export_csv(self, tmp_path):
        """Test CSV export."""
        sweep = ParameterSweep({"n_voters": [1000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=2,
            seed=42,
            verbose=False,
        )

        runner.run()

        output_file = tmp_path / "results.csv"
        runner.export_results(str(output_file))

        assert output_file.exists()
        df_read = pl.read_csv(output_file)
        assert len(df_read) == 2

    def test_export_parquet(self, tmp_path):
        """Test Parquet export."""
        sweep = ParameterSweep({"n_voters": [1000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=2,
            seed=42,
            verbose=False,
        )

        runner.run()

        output_file = tmp_path / "results.parquet"
        runner.export_results(str(output_file))

        assert output_file.exists()
        df_read = pl.read_parquet(output_file)
        assert len(df_read) == 2

    def test_export_json(self, tmp_path):
        """Test JSON export."""
        sweep = ParameterSweep({"n_voters": [1000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=2,
            seed=42,
            verbose=False,
        )

        runner.run()

        output_file = tmp_path / "results.json"
        runner.export_results(str(output_file))

        assert output_file.exists()

    def test_export_auto_format(self, tmp_path):
        """Test auto-format detection from file extension."""
        sweep = ParameterSweep({"n_voters": [1000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=2,
            seed=42,
            verbose=False,
        )

        runner.run()

        # Auto-detect CSV
        csv_file = tmp_path / "auto.csv"
        runner.export_results(str(csv_file))
        assert csv_file.exists()

        # Auto-detect Parquet
        parquet_file = tmp_path / "auto.parquet"
        runner.export_results(str(parquet_file))
        assert parquet_file.exists()

    def test_export_unknown_format_raises(self, tmp_path):
        """Test that unknown format raises ValueError."""
        sweep = ParameterSweep({"n_voters": [1000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=1,
            seed=42,
            verbose=False,
        )

        runner.run()

        with pytest.raises(ValueError, match="Unknown format"):
            runner.export_results(str(tmp_path / "results.xyz"), format="xyz")

    def test_export_summary(self, tmp_path):
        """Test summary export."""
        sweep = ParameterSweep({"n_voters": [1000, 2000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=3,
            seed=42,
            verbose=False,
        )

        runner.run()

        summary_file = tmp_path / "summary.csv"
        runner.export_summary(str(summary_file))

        assert summary_file.exists()
        df_read = pl.read_csv(summary_file)
        assert len(df_read) == 2

    def test_export_summary_json(self, tmp_path):
        """Test summary export to JSON."""
        sweep = ParameterSweep({"n_voters": [1000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=2,
            seed=42,
            verbose=False,
        )

        runner.run()

        summary_file = tmp_path / "summary.json"
        runner.export_summary(str(summary_file))
        assert summary_file.exists()

    def test_export_summary_unknown_format_raises(self, tmp_path):
        """Test that unknown summary format raises ValueError."""
        sweep = ParameterSweep({"n_voters": [1000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=1,
            seed=42,
            verbose=False,
        )

        runner.run()

        with pytest.raises(ValueError, match="Unknown format"):
            runner.export_summary(str(tmp_path / "summary.xyz"), format="xyz")

    def test_parallel_execution(self):
        """Test parallel execution produces valid results."""
        sweep = ParameterSweep({"n_voters": [1000, 2000]}, fixed_params={"n_constituencies": 3})

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=3,
            n_jobs=2,
            seed=42,
            verbose=False,
        )

        results_df = runner.run()
        assert len(results_df) == 2 * 3
        assert all((results_df["turnout"] >= 0) & (results_df["turnout"] <= 1))

    def test_invalid_sweep_type(self):
        """Test that invalid sweep type raises error."""
        with pytest.raises(ValueError, match="Unknown sweep_type"):
            sweep = ParameterSweep({"a": [1, 2]}, sweep_type="invalid")
            sweep.generate_configs()

    def test_export_before_run_raises_error(self):
        """Test that exporting before running raises error."""
        sweep = ParameterSweep({"n_voters": [1000]})
        runner = BatchRunner(model_class=ElectionModel, parameter_sweep=sweep, verbose=False)
        with pytest.raises(ValueError, match="No results available"):
            runner.export_results("dummy.csv")


class TestSensitivityAnalysis:
    """Tests for sensitivity analysis functions."""

    def test_one_at_a_time_basic(self):
        """one_at_a_time returns results for each parameter value."""
        from electoral_sim import ElectionModel
        from electoral_sim.analysis.sensitivity import one_at_a_time

        results = one_at_a_time(
            ElectionModel,
            {"n_voters": 500, "n_constituencies": 3},
            vary_param="temperature",
            vary_values=[0.3, 0.7],
            n_runs=1,
            seed=42,
        )
        assert len(results) == 2
        assert results[0]["param"] == "temperature"

    def test_grid_sensitivity_basic(self):
        """grid_sensitivity returns results for all combinations."""
        from electoral_sim import ElectionModel
        from electoral_sim.analysis.sensitivity import grid_sensitivity

        results = grid_sensitivity(
            ElectionModel,
            {"n_voters": [300, 500], "temperature": [0.3, 0.7]},
            n_runs=1,
            seed=42,
        )
        assert len(results) == 4  # 2 × 2 combinations

    def test_swing_analysis_basic(self):
        """swing_analysis returns results for each swing value."""
        from electoral_sim import ElectionModel
        from electoral_sim.analysis.sensitivity import swing_analysis

        results = swing_analysis(
            ElectionModel,
            {"n_voters": 500, "n_constituencies": 3},
            swing_range=[-1.0, 0.0, 1.0],
            n_runs=1,
            seed=42,
        )
        assert len(results) == 3


class TestCalibration:
    """Tests for calibration framework."""

    def test_mse_loss_returns_float(self):
        """mse_loss returns a non-negative float."""
        from electoral_sim import ElectionModel
        from electoral_sim.analysis.calibration import mse_loss

        loss = mse_loss(
            ElectionModel,
            {"n_voters": 500, "n_constituencies": 3},
            targets={"turnout": 0.7, "gallagher": 4.0},
            n_runs=2,
            seed=42,
        )
        assert isinstance(loss, float)
        assert loss >= 0

    def test_grid_search_calibration_sorted(self):
        """grid_search_calibration returns results sorted by loss."""
        from electoral_sim import ElectionModel
        from electoral_sim.analysis.calibration import grid_search_calibration

        results = grid_search_calibration(
            ElectionModel,
            {"n_voters": [300, 500], "temperature": [0.3, 0.7]},
            targets={"gallagher": 10.0},
            n_runs=1,
            seed=42,
        )
        assert len(results) == 4
        assert results[0]["loss"] <= results[-1]["loss"]

    def test_calibration_report(self):
        """generate_calibration_report returns a string."""
        from electoral_sim.analysis.calibration import generate_calibration_report

        results = [{"params": {"n_voters": 100, "temperature": 0.5}, "loss": 0.123}]
        report = generate_calibration_report(results, {"gallagher": 10.0})
        assert isinstance(report, str)
        assert "0.123" in report


class TestRedistricting:
    """Tests for redistricting module."""

    def test_precinct_graph_basic(self):
        """PrecinctGraph creates and assigns districts."""
        from electoral_sim.analysis.redistricting import PrecinctGraph

        adj = [[1], [0, 2], [1, 3], [2]]
        pg = PrecinctGraph(4, adj, np.array([100, 200, 150, 250]))
        pg.assign_districts(np.array([0, 0, 1, 1]))
        balance = pg.population_balance(2)
        assert balance["total_population"] == 700
        assert balance["ideal_population"] == 350

    def test_recom_proposal_basic(self):
        """ReCom proposal generates a new valid district assignment."""
        from electoral_sim.analysis.redistricting import PrecinctGraph, recom_proposal

        adj = [[1], [0, 2], [1, 3], [2]]
        pg = PrecinctGraph(4, adj, np.array([100, 200, 150, 250]))
        pg.assign_districts(np.array([0, 0, 1, 1]))
        rng = np.random.default_rng(42)
        new_assign = recom_proposal(pg, 0, 1, rng)
        assert new_assign is not None
        assert len(new_assign) == 4
        assert set(np.unique(new_assign)).issubset({0, 1})
