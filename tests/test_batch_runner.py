"""
Tests for BatchRunner and ParameterSweep
"""

import pytest
import numpy as np
import polars as pl
from pathlib import Path

from electoral_sim import ElectionModel
from electoral_sim.analysis import BatchRunner, ParameterSweep


class TestParameterSweep:
    """Test ParameterSweep class."""

    def test_grid_search_combinations(self):
        """Test that grid search generates all combinations."""
        sweep = ParameterSweep({"a": [1, 2], "b": [10, 20, 30]}, sweep_type="grid")

        configs = sweep.generate_configs()

        assert len(configs) == 6  # 2 * 3 = 6 combinations
        assert all("a" in c and "b" in c for c in configs)

        # Verify all combinations are present
        expected = [
            {"a": 1, "b": 10},
            {"a": 1, "b": 20},
            {"a": 1, "b": 30},
            {"a": 2, "b": 10},
            {"a": 2, "b": 20},
            {"a": 2, "b": 30},
        ]
        assert configs == expected

    def test_grid_search_with_fixed_params(self):
        """Test that fixed parameters are included."""
        sweep = ParameterSweep(parameters={"a": [1, 2]}, fixed_params={"b": 100, "c": "fixed"})

        configs = sweep.generate_configs()

        assert all(c["b"] == 100 and c["c"] == "fixed" for c in configs)

    def test_random_search_size(self):
        """Test that random search generates correct number of samples."""
        sweep = ParameterSweep(
            parameters={"a": [1, 2, 3], "b": [10, 20]}, sweep_type="random", n_samples=50
        )

        configs = sweep.generate_configs()

        assert len(configs) == 50
        assert all("a" in c and "b" in c for c in configs)

    def test_sweep_len(self):
        """Test __len__ method."""
        grid_sweep = ParameterSweep({"a": [1, 2], "b": [10, 20, 30]}, sweep_type="grid")
        assert len(grid_sweep) == 6

        random_sweep = ParameterSweep({"a": [1, 2]}, sweep_type="random", n_samples=100)
        assert len(random_sweep) == 100


class TestBatchRunner:
    """Test BatchRunner class."""

    def test_basic_batch_run(self):
        """Test basic batch run with small parameters."""
        sweep = ParameterSweep(
            {"n_voters": [1000, 2000], "temperature": [0.3, 0.5]},
            fixed_params={"n_constituencies": 5, "electoral_system": "FPTP"},
        )

        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=2,
            n_jobs=1,  # Sequential for reproducibility
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

        # Results should be identical
        assert results1["turnout"].to_list() == results2["turnout"].to_list()
        assert results1["gallagher"].to_list() == results2["gallagher"].to_list()

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

        # Check summary structure
        assert isinstance(summary, pl.DataFrame)
        assert len(summary) == 2  # 2 configs

        # Check summary columns
        expected_cols = [
            "config_idx",
            "n_voters",
            "turnout_mean",
            "turnout_std",
            "gallagher_mean",
            "n_runs",
        ]
        for col in expected_cols:
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

        # Export to CSV
        output_file = tmp_path / "results.csv"
        runner.export_results(str(output_file))

        assert output_file.exists()

        # Verify can read back
        df_read = pl.read_csv(output_file)
        assert len(df_read) == 2

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

        # Export summary
        summary_file = tmp_path / "summary.csv"
        runner.export_summary(str(summary_file))

        assert summary_file.exists()

        # Verify can read back
        df_read = pl.read_csv(summary_file)
        assert len(df_read) == 2

    def test_parallel_execution(self):
        """Test parallel execution produces valid results."""
        sweep = ParameterSweep({"n_voters": [1000, 2000]}, fixed_params={"n_constituencies": 3})

        # Note: Can't guarantee determinism with parallel execution
        # but we can verify the structure and validity
        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=3,
            n_jobs=2,  # Use 2 workers
            seed=42,
            verbose=False,
        )

        results_df = runner.run()

        # Check all runs completed
        assert len(results_df) == 2 * 3  # 2 configs * 3 runs

        # Check all turnouts are valid (between 0 and 1)
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

        with pytest.raises(ValueError, match="No results available"):
            runner.get_summary_stats()
