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

from __future__ import annotations

import numpy as np


def coalition_strain(
    positions: np.ndarray,
    weights: np.ndarray | None = None,
) -> float:
    """
    Calculate policy strain within a coalition.

    Strain = weighted average of pairwise policy distances.
    Higher strain = less stable coalition.

    Args:
        positions: Policy positions of coalition members (n_members x n_dimensions)
        weights: Optional weights (e.g., seat shares). Default: equal weights.

    Returns:
        Strain value (0 = perfect agreement, higher = more tension)
    """
    if positions.ndim == 1:
        positions = positions.reshape(-1, 1)

    n = len(positions)
    if n < 2:
        return 0.0

    if weights is None:
        weights = np.ones(n)

    weight_sum = weights.sum()
    if weight_sum == 0:
        return 0.0

    normalized_weights = weights / weight_sum

    total_strain = 0.0
    total_weight = 0.0

    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(positions[i] - positions[j])
            pair_weight = normalized_weights[i] * normalized_weights[j]
            total_strain += dist * pair_weight
            total_weight += pair_weight

    if total_weight == 0:
        return 0.0

    return total_strain / total_weight
