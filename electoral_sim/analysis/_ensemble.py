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

import numpy as np
from electoral_sim.analysis.redistricting import PrecinctGraph, recom_proposal


def ensemble_analysis(
    graph: PrecinctGraph,
    enacted_assignment: np.ndarray,
    n_plans: int = 100,
    rng: np.random.Generator | None = None,
) -> dict:
    """
    Compare an enacted district plan against a simulated ensemble.

    Args:
        graph: PrecinctGraph with population data
        enacted_assignment: The actual/enacted district assignment
        n_plans: Number of simulated plans to generate
        rng: Random generator

    Returns:
        Dict with enacted metrics, ensemble mean/std, and percentile rank
    """
    if rng is None:
        rng = np.random.default_rng()

    n_districts = int(enacted_assignment.max()) + 1
    graph.assign_districts(enacted_assignment.copy())
    enacted_balance = graph.population_balance(n_districts)

    # Generate ensemble
    ensemble_deviations = []
    for _ in range(n_plans):
        graph.assign_districts(enacted_assignment.copy())
        for i in range(10):
            d1 = int(rng.integers(n_districts))
            d2 = int(rng.integers(n_districts))
            if d1 != d2:
                new = recom_proposal(graph, d1, d2, rng)
                if new is not None and new.min() >= 0:
                    graph.assign_districts(new)
        try:
            balance = graph.population_balance(n_districts)
            ensemble_deviations.append(balance["max_deviation"])
        except ValueError:
            continue

    ensemble_arr = np.array(ensemble_deviations) if ensemble_deviations else np.array([enacted_dev])
    enacted_dev = enacted_balance["max_deviation"]

    # Percentile rank of enacted plan within ensemble
    rank = float(np.sum(ensemble_arr < enacted_dev)) / n_plans

    return {
        "enacted_max_deviation": enacted_dev,
        "ensemble_mean": float(np.mean(ensemble_arr)),
        "ensemble_std": float(np.std(ensemble_arr)),
        "ensemble_min": float(np.min(ensemble_arr)),
        "ensemble_max": float(np.max(ensemble_arr)),
        "enacted_percentile": rank,
        "n_plans": n_plans,
    }
