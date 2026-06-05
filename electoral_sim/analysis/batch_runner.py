# Copyright 2025 Ayush Maurya
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

"""
BatchRunner - Parameter sweeping and batch execution for ElectoralSim

This module provides advanced batch execution capabilities including:
- Parameter sweeps (grid search, random search)
- Parallel execution using multiprocessing
- Results aggregation to Polars DataFrames
- Export to CSV, JSON, and Parquet formats
"""

import multiprocessing
import os
from typing import Any, Callable, Type
from dataclasses import dataclass, field
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import polars as pl

from tqdm import tqdm

from electoral_sim.analysis._sweep import ParameterSweep  # noqa: F401 — re-exported backward compat


class BatchRunner:
    """
    Execute multiple simulations with varying parameters.

    Features:
    - Parameter sweeps (grid or random)
    - Parallel execution
    - Results aggregation
    - Export to multiple formats

    Example:
        >>> from electoral_sim import ElectionModel, BatchRunner, ParameterSweep
        >>>
        >>> sweep = ParameterSweep({
        ...     'n_voters': [10_000, 50_000],
        ...     'temperature': [0.3, 0.5, 0.7],
        ...     'economic_growth': [-0.02, 0.0, 0.02]
        ... })
        >>>
        >>> runner = BatchRunner(
        ...     model_class=ElectionModel,
        ...     parameter_sweep=sweep,
        ...     n_runs_per_config=10,
        ...     n_jobs=4
        ... )
        >>>
        >>> results_df = runner.run()
        >>> runner.export_results('results.csv')
    """

    def __init__(
        self,
        model_class: Type,
        parameter_sweep: ParameterSweep,
        n_runs_per_config: int = 1,
        n_jobs: int = 1,
        election_kwargs: dict[str, Any] = None,
        seed: int = None,
        verbose: bool = True,
    ):
        """
        Initialize BatchRunner.

        Args:
            model_class: ElectionModel or compatible class
            parameter_sweep: ParameterSweep instance
            n_runs_per_config: Monte Carlo iterations per configuration
            n_jobs: Number of parallel workers (1 = sequential)
            election_kwargs: Extra kwargs passed to run_election()
            seed: Random seed for reproducibility
            verbose: Show progress bars
        """
        self.model_class = model_class
        self.parameter_sweep = parameter_sweep
        self.n_runs_per_config = n_runs_per_config
        self.n_jobs = n_jobs
        self.election_kwargs = election_kwargs or {}
        self.seed = seed
        self.verbose = verbose

        self.results: list[dict] = []
        self.results_df: pl.DataFrame = None

    def run(self) -> pl.DataFrame:
        """
        Execute the batch run.

        Returns:
            Polars DataFrame with all results
        """
        configs = self.parameter_sweep.generate_configs()
        total_runs = len(configs) * self.n_runs_per_config

        if self.verbose:
            print(
                f"Running {len(configs)} configurations × {self.n_runs_per_config} runs = {total_runs} total simulations"
            )

        if self.n_jobs == 1:
            self.results = self._run_sequential(configs)
        else:
            self.results = self._run_parallel(configs)

        # Convert to DataFrame
        self.results_df = pl.DataFrame(self.results)
        return self.results_df

    def _run_sequential(self, configs: list[dict]) -> list[dict]:
        """Run simulations sequentially."""
        all_results = []

        iterator = tqdm(configs, desc="Configurations") if self.verbose else configs

        for config_idx, config in enumerate(iterator):
            for run_idx in range(self.n_runs_per_config):
                # Generate unique seed for reproducibility
                run_seed = self._get_run_seed(config_idx, run_idx)

                result = self._run_single_simulation(config, config_idx, run_idx, run_seed)
                all_results.append(result)

        return all_results

    def _run_parallel(self, configs: list[dict]) -> list[dict]:
        """Run simulations in parallel using ProcessPoolExecutor."""
        all_results = []

        # Create all jobs
        jobs = []
        for config_idx, config in enumerate(configs):
            for run_idx in range(self.n_runs_per_config):
                run_seed = self._get_run_seed(config_idx, run_idx)
                jobs.append((config, config_idx, run_idx, run_seed))

        # Execute in parallel using spawn context to avoid Numba/OpenMP fork() conflict
        # Ref: Numba's OpenMP threading layer is unsafe with Linux default fork() multiprocessing
        try:
            mp_context = multiprocessing.get_context("spawn")
        except (ValueError, RuntimeError):
            mp_context = None  # fall back to default on platforms where spawn is unavailable

        with ProcessPoolExecutor(max_workers=self.n_jobs, mp_context=mp_context) as executor:
            futures = {
                executor.submit(
                    _run_simulation_worker,
                    self.model_class,
                    config,
                    config_idx,
                    run_idx,
                    run_seed,
                    self.election_kwargs,
                ): (config_idx, run_idx)
                for config, config_idx, run_idx, run_seed in jobs
            }

            iterator = (
                tqdm(as_completed(futures), total=len(futures), desc="Simulations")
                if self.verbose
                else as_completed(futures)
            )

            for future in iterator:
                result = future.result()
                all_results.append(result)

        # Sort by config_idx and run_idx
        all_results.sort(key=lambda x: (x["config_idx"], x["run_idx"]))

        return all_results

    def _run_single_simulation(
        self, config: dict, config_idx: int, run_idx: int, run_seed: int
    ) -> dict:
        """Run a single simulation and return results."""
        # Create model with config parameters
        model = self.model_class(**config, seed=run_seed)

        # Run election
        election_results = model.run_election(**self.election_kwargs)

        # Flatten results
        result = {
            "config_idx": config_idx,
            "run_idx": run_idx,
            "seed": run_seed,
            **config,
            **self._extract_metrics(election_results),
        }

        return result

    def _extract_metrics(self, election_results: dict) -> dict:
        """Extract key metrics from election results."""
        metrics = {
            "turnout": election_results.get("turnout", 0.0),
            "gallagher": election_results.get("gallagher", 0.0),
            "enp_votes": election_results.get("enp_votes", 0.0),
            "enp_seats": election_results.get("enp_seats", 0.0),
            "vse": election_results.get("vse", 0.0),
        }

        # Don't include arrays in results to avoid CSV export issues
        # Users can access full results via the model if needed

        return metrics

    def _get_run_seed(self, config_idx: int, run_idx: int) -> int:
        """Generate deterministic seed for each run."""
        if self.seed is None:
            return None
        return self.seed + config_idx * 10000 + run_idx

    def get_summary_stats(self) -> pl.DataFrame:
        """
        Aggregate statistics across runs for each configuration.

        Returns:
            DataFrame with mean, std, min, max for each config
        """
        if self.results_df is None:
            raise ValueError("No results available. Run `run()` first.")

        # Group by config_idx and aggregate
        param_cols = list(self.parameter_sweep.parameters.keys())

        summary = self.results_df.group_by("config_idx").agg(
            [
                *[pl.col(p).first().alias(p) for p in param_cols],
                pl.col("turnout").mean().alias("turnout_mean"),
                pl.col("turnout").std().alias("turnout_std"),
                pl.col("turnout").quantile(0.25).alias("turnout_q25"),
                pl.col("turnout").quantile(0.75).alias("turnout_q75"),
                (pl.col("turnout").std() / pl.col("turnout").count().sqrt()).alias("turnout_mcse"),
                pl.col("gallagher").mean().alias("gallagher_mean"),
                pl.col("gallagher").std().alias("gallagher_std"),
                pl.col("gallagher").quantile(0.25).alias("gallagher_q25"),
                pl.col("gallagher").quantile(0.75).alias("gallagher_q75"),
                (pl.col("gallagher").std() / pl.col("gallagher").count().sqrt()).alias(
                    "gallagher_mcse"
                ),
                pl.col("enp_votes").mean().alias("enp_votes_mean"),
                pl.col("enp_votes").std().alias("enp_votes_std"),
                pl.col("enp_seats").mean().alias("enp_seats_mean"),
                pl.col("enp_seats").std().alias("enp_seats_std"),
                pl.col("vse").mean().alias("vse_mean"),
                pl.col("vse").std().alias("vse_std"),
                pl.len().alias("n_runs"),
            ]
        )

        # Add 95% CI bounds (mean ± 1.96 * SE) for key metrics
        for metric in ["turnout", "gallagher"]:
            summary = summary.with_columns(
                (pl.col(f"{metric}_mean") - 1.96 * pl.col(f"{metric}_mcse")).alias(
                    f"{metric}_ci_lower"
                ),
                (pl.col(f"{metric}_mean") + 1.96 * pl.col(f"{metric}_mcse")).alias(
                    f"{metric}_ci_upper"
                ),
            )

        return summary

    def export_results(self, filepath: str, format: str = "auto"):
        """
        Export results to file.

        Args:
            filepath: Output file path
            format: 'csv', 'parquet', 'json', or 'auto' (infer from extension)
        """
        if self.results_df is None:
            raise ValueError("No results available. Run `run()` first.")

        if format == "auto":
            if filepath.endswith(".csv"):
                format = "csv"
            elif filepath.endswith(".parquet"):
                format = "parquet"
            elif filepath.endswith(".json"):
                format = "json"
            else:
                format = "csv"

        if format == "csv":
            self.results_df.write_csv(filepath)
        elif format == "parquet":
            self.results_df.write_parquet(filepath)
        elif format == "json":
            self.results_df.write_json(filepath)
        else:
            raise ValueError(f"Unknown format: {format}")

        if self.verbose:
            print(f"Results exported to {filepath}")

        # Write reproducibility manifest alongside data file
        manifest = self._build_manifest()
        manifest_path = f"{filepath}.manifest.json"
        import json as _json

        with open(manifest_path, "w") as f:
            _json.dump(manifest, f, indent=2)
        if self.verbose:
            print(f"Manifest exported to {manifest_path}")

    def _build_manifest(self) -> dict:
        """Build reproducibility manifest for the batch run.

        Returns dict with version, git commit, Python version,
        dependency versions, CPU/GPU info, seed hierarchy, and config hash.
        """
        import hashlib
        import json
        import platform
        import sys

        from electoral_sim import __version__

        # Git commit (best-effort)
        git_commit = None
        try:
            import subprocess

            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                git_commit = result.stdout.strip()
        except Exception:
            pass

        # Dependency versions
        deps = {}
        for pkg in ["mesa", "polars", "numpy", "numba", "networkx"]:
            try:
                mod = __import__(pkg)
                deps[pkg] = getattr(mod, "__version__", "unknown")
            except ImportError:
                deps[pkg] = "not installed"

        # Config hash for identifying unique configurations
        config_str = json.dumps(self.parameter_sweep.parameters, sort_keys=True)
        config_hash = hashlib.sha256(config_str.encode()).hexdigest()[:12]

        return {
            "package": "electoral-sim",
            "version": __version__,
            "git_commit": git_commit,
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "dependencies": deps,
            "seed_hierarchy": {
                "base_seed": self.seed,
                "n_runs_per_config": self.n_runs_per_config,
            },
            "config_hash": config_hash,
            "n_configs": len(self.parameter_sweep),
            "n_jobs": self.n_jobs,
            "model_class": self.model_class.__name__,
        }

    def export_summary(self, filepath: str, format: str = "auto"):
        """Export summary statistics to file."""
        summary = self.get_summary_stats()

        if format == "auto":
            format = "csv" if filepath.endswith(".csv") else "csv"

        if format == "csv":
            summary.write_csv(filepath)
        elif format == "parquet":
            summary.write_parquet(filepath)
        elif format == "json":
            summary.write_json(filepath)
        else:
            raise ValueError(f"Unknown format: {format}")

        if self.verbose:
            print(f"Summary exported to {filepath}")


def _run_simulation_worker(
    model_class: Type,
    config: dict,
    config_idx: int,
    run_idx: int,
    run_seed: int,
    election_kwargs: dict,
) -> dict:
    """Worker function for parallel execution."""
    # Prevent Numba OpenMP threads from conflicting with multiprocessing
    # Set to 1 in worker process to avoid nested parallelism issues
    os.environ.setdefault("OMP_NUM_THREADS", "1")

    # Create model
    model = model_class(**config, seed=run_seed)

    # Run election
    election_results = model.run_election(**election_kwargs)

    # Extract metrics (without nested arrays)
    metrics = {
        "turnout": election_results.get("turnout", 0.0),
        "gallagher": election_results.get("gallagher", 0.0),
        "enp_votes": election_results.get("enp_votes", 0.0),
        "enp_seats": election_results.get("enp_seats", 0.0),
        "vse": election_results.get("vse", 0.0),
    }

    # Combine
    result = {"config_idx": config_idx, "run_idx": run_idx, "seed": run_seed, **config, **metrics}

    return result
