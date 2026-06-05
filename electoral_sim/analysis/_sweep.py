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

"""ParameterSweep — grid/random parameter sweep definitions for BatchRunner."""

import itertools
from typing import Any
from dataclasses import dataclass, field

import numpy as np


@dataclass
class ParameterSweep:
    """Defines a parameter sweep for batch simulations.

    Args:
        parameters: Dictionary mapping parameter names to lists of values
        sweep_type: 'grid' for all combinations, 'random' for random sampling
        n_samples: Number of random samples (for sweep_type='random')
        fixed_params: Parameters that don't change
    """

    parameters: dict[str, list[Any]]
    sweep_type: str = "grid"
    n_samples: int = 100
    fixed_params: dict[str, Any] = field(default_factory=dict)

    def generate_configs(self) -> list[dict[str, Any]]:
        """Generate all parameter configurations."""
        if self.sweep_type == "grid":
            return self._grid_search()
        elif self.sweep_type == "random":
            return self._random_search()
        else:
            raise ValueError(f"Unknown sweep_type: {self.sweep_type}")

    def _grid_search(self) -> list[dict[str, Any]]:
        """Generate all combinations of parameters (grid search)."""
        param_names = list(self.parameters.keys())
        param_values = list(self.parameters.values())

        configs = []
        for combo in itertools.product(*param_values):
            config = dict(zip(param_names, combo))
            config.update(self.fixed_params)
            configs.append(config)

        return configs

    def _random_search(self) -> list[dict[str, Any]]:
        """Generate random parameter combinations."""
        param_names = list(self.parameters.keys())
        param_values = list(self.parameters.values())

        configs = []
        rng = np.random.default_rng()

        for _ in range(self.n_samples):
            config = {}
            for name, values in zip(param_names, param_values):
                config[name] = rng.choice(values)
            config.update(self.fixed_params)
            configs.append(config)

        return configs

    def __len__(self) -> int:
        """Return number of configurations."""
        if self.sweep_type == "grid":
            return int(np.prod([len(v) for v in self.parameters.values()]))
        else:
            return self.n_samples

    def validate(self) -> list[str]:
        """Validate parameter names and values, returning all errors (not just first).

        Returns:
            List of error strings (empty if valid).
        """
        KNOWN_PARAMS = frozenset(
            {
                "n_voters",
                "n_constituencies",
                "electoral_system",
                "allocation_method",
                "threshold",
                "temperature",
                "seed",
                "economic_growth",
                "national_mood",
                "anti_incumbency",
                "include_nota",
                "use_adaptive_strategy",
                "use_gpu",
            }
        )
        errors = []

        all_params = set(self.parameters.keys()) | set(self.fixed_params.keys())
        unknown = all_params - KNOWN_PARAMS
        if unknown:
            errors.append(f"Unknown parameters: {sorted(unknown)}. Known: {sorted(KNOWN_PARAMS)}")

        for name, values in self.parameters.items():
            if not isinstance(values, list) or len(values) == 0:
                errors.append(
                    f"Parameter '{name}' must be a non-empty list, got {type(values).__name__}"
                )
            if name == "n_voters" and any(v <= 0 for v in values if isinstance(v, (int, float))):
                errors.append("Parameter 'n_voters' values must be positive")
            if name == "temperature" and any(v <= 0 for v in values if isinstance(v, (int, float))):
                errors.append("Parameter 'temperature' values must be positive")

        if self.sweep_type not in ("grid", "random"):
            errors.append(f"Invalid sweep_type '{self.sweep_type}', expected 'grid' or 'random'")

        return errors
