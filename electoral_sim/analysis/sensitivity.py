"""
Sensitivity Analysis for ElectoralSim.

Provides one-at-a-time (OAT) and grid-based sensitivity analysis
for exploring how parameter changes affect simulation outcomes.
"""

from itertools import product

import numpy as np


def one_at_a_time(
    model_class,
    base_params: dict,
    vary_param: str,
    vary_values: list,
    metric: str = "gallagher",
    n_runs: int = 3,
    **model_kwargs,
) -> list[dict]:
    """
    One-at-a-time (OAT) sensitivity: vary one parameter while fixing others.

    Args:
        model_class: ElectionModel class (or compatible)
        base_params: Dictionary of default parameter values
        vary_param: Name of the parameter to vary
        vary_values: List of values to test for the varying parameter
        metric: Metric to track (default 'gallagher')
        n_runs: Runs per parameter value for averaging
        **model_kwargs: Additional kwargs passed to model_class

    Returns:
        List of dicts with param value, metric mean, and metric std
    """
    results = []
    for value in vary_values:
        params = {**base_params, vary_param: value}
        metrics = []
        for _ in range(n_runs):
            model = model_class(**params, **model_kwargs)
            result = model.run_election()
            metrics.append(result.get(metric, 0.0))
        results.append(
            {
                "param": vary_param,
                "value": value,
                f"{metric}_mean": float(np.mean(metrics)),
                f"{metric}_std": float(np.std(metrics)),
                "n_runs": n_runs,
            }
        )
    return results


def grid_sensitivity(
    model_class,
    param_grid: dict[str, list],
    metric: str = "gallagher",
    n_runs: int = 3,
    **model_kwargs,
) -> list[dict]:
    """
    Grid-based sensitivity: evaluate all combinations of parameter values.

    Args:
        model_class: ElectionModel class
        param_grid: Dict mapping param names to lists of values
        metric: Metric to track (default 'gallagher')
        n_runs: Runs per configuration
        **model_kwargs: Additional kwargs passed to model_class

    Returns:
        List of dicts with param values, metric mean, and metric std
    """
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    results = []

    for combo in product(*param_values):
        params = dict(zip(param_names, combo))
        metrics = []
        for _ in range(n_runs):
            model = model_class(**params, **model_kwargs)
            result = model.run_election()
            metrics.append(result.get(metric, 0.0))
        entry = {
            **params,
            f"{metric}_mean": float(np.mean(metrics)),
            f"{metric}_std": float(np.std(metrics)),
            "n_runs": n_runs,
        }
        results.append(entry)

    return results


def swing_analysis(
    model_class,
    base_params: dict,
    swing_param: str = "national_mood",
    swing_range: list[float] | None = None,
    metric: str = "gallagher",
    n_runs: int = 3,
    seed: int = 42,
    **model_kwargs,
) -> list[dict]:
    """
    Swing-state/district analysis: perturb a parameter and track seat tipping points.

    Args:
        model_class: ElectionModel class
        base_params: Dictionary of default parameter values
        swing_param: Parameter to perturb (default 'national_mood')
        swing_range: Values to test (default: -3 to +3 in 0.5 steps)
        metric: Metric to track
        n_runs: Runs per swing value
        seed: Base seed
        **model_kwargs: Additional kwargs for model_class

    Returns:
        List of dicts with swing value, metric mean/std, and tipping detection
    """
    if swing_range is None:
        swing_range = [x * 0.5 for x in range(-6, 7)]  # -3.0 to +3.0

    results = []
    prev_sign = None

    for value in swing_range:
        params = {**base_params, swing_param: value}
        metrics = []
        for i in range(n_runs):
            model = model_class(**params, seed=seed + i, **model_kwargs)
            result = model.run_election()
            metrics.append(result.get(metric, 0.0))

        mean_val = float(np.mean(metrics))
        results.append(
            {
                "swing_param": swing_param,
                "swing_value": value,
                f"{metric}_mean": mean_val,
                f"{metric}_std": float(np.std(metrics)),
            }
        )

    return results
