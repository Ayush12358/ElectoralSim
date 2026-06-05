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

"""
Calibration Framework for ElectoralSim.

Provides tools for calibrating simulation parameters against
historical election results using loss functions and grid search.
"""

from itertools import product

import numpy as np

# Target metrics that can be calibrated against
TARGET_METRICS = ["gallagher", "turnout", "enp_votes", "enp_seats"]


def mse_loss(
    model_class,
    params: dict,
    targets: dict[str, float],
    metric_weights: dict[str, float] | None = None,
    n_runs: int = 5,
    seed: int = 42,
) -> float:
    """
    Mean Squared Error between simulation outputs and historical targets.

    Args:
        model_class: ElectionModel class
        params: Simulation parameters
        targets: Dict mapping metric names to target values
        metric_weights: Dict mapping metric names to weight in loss (default: equal)
        n_runs: Runs for averaging
        seed: Base random seed

    Returns:
        MSE loss (lower = better fit)
    """
    if metric_weights is None:
        metric_weights = {m: 1.0 for m in targets}

    predictions = {m: [] for m in targets}
    for i in range(n_runs):
        model = model_class(**params, seed=seed + i)
        result = model.run_election()
        for metric in targets:
            predictions[metric].append(result.get(metric, 0.0))

    loss = 0.0
    for metric, target in targets.items():
        pred_mean = np.mean(predictions[metric])
        weight = metric_weights.get(metric, 1.0)
        loss += weight * (pred_mean - target) ** 2

    return loss


def grid_search_calibration(
    model_class,
    param_grid: dict[str, list],
    targets: dict[str, float],
    metric_weights: dict[str, float] | None = None,
    n_runs: int = 3,
    seed: int = 42,
) -> list[dict]:
    """
    Grid-search calibration across parameter space.

    Args:
        model_class: ElectionModel class
        param_grid: Dict mapping param names to lists of values to search
        targets: Target metric values from historical data
        metric_weights: Optional per-metric weights
        n_runs: Simulation runs per parameter combo
        seed: Base seed

    Returns:
        List of result dicts sorted by loss (best first), each containing
        params, loss, and per-metric predictions
    """
    results = []
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())

    for combo in product(*param_values):
        params = dict(zip(param_names, combo))
        loss = mse_loss(model_class, params, targets, metric_weights, n_runs, seed)
        results.append({"params": params, "loss": loss})

    results.sort(key=lambda r: r["loss"])
    return results


def generate_calibration_report(
    results: list[dict],
    targets: dict[str, float],
) -> str:
    """
    Generate a human-readable calibration report.

    Args:
        results: Calibration results from grid_search_calibration()
        targets: Target metric values for reference

    Returns:
        Formatted report string
    """
    lines = ["=" * 60]
    lines.append("CALIBRATION REPORT")
    lines.append("=" * 60)
    lines.append(f"\nTargets: {targets}")
    lines.append(f"\nBest configuration (loss={results[0]['loss']:.4f}):")
    lines.append(f"  {results[0]['params']}")

    if len(results) > 1:
        lines.append("\nTop 5 configurations:")
        for i, r in enumerate(results[:5], 1):
            lines.append(f"  {i}. loss={r['loss']:.4f} params={r['params']}")

    return "\n".join(lines)
