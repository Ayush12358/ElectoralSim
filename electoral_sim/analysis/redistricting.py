"""
Redistricting Module — inspired by GerryChain.

Provides precinct/constituency graph representation, district assignment
tracking, population balance checking, contiguity validation, and
election result updaters. Heavy GIS dependencies are kept optional
under a 'geo' extra.
"""

from __future__ import annotations

import numpy as np


class PrecinctGraph:
    """
    Represents a precinct/constituency adjacency graph for redistricting.

    Nodes are precincts, edges represent geographic adjacency.
    Districts are assignments of precincts to district IDs.
    """

    def __init__(
        self,
        n_precincts: int,
        adj_list: list[list[int]] | None = None,
        populations: np.ndarray | None = None,
    ):
        """
        Args:
            n_precincts: Number of precincts
            adj_list: Adjacency list (list of neighbor indices per precinct)
            populations: Precinct populations
        """
        self.n_precincts = n_precincts
        self.adj_list = adj_list if adj_list is not None else [[] for _ in range(n_precincts)]
        self.populations = populations if populations is not None else np.ones(n_precincts, dtype=int)
        self.assignment = np.full(n_precincts, -1, dtype=int)

    def assign_districts(self, assignment: np.ndarray):
        """Set the district assignment for all precincts."""
        if len(assignment) != self.n_precincts:
            raise ValueError(f"Assignment length {len(assignment)} != {self.n_precincts}")
        self.assignment = assignment.copy()

    def population_balance(self, n_districts: int) -> dict[str, float]:
        """
        Compute population balance statistics.

        Args:
            n_districts: Number of districts

        Returns:
            Dict with 'max_deviation', 'min_deviation', 'ideal_population'
        """
        if self.assignment.min() < 0:
            raise ValueError("District assignment not complete")

        total_pop = self.populations.sum()
        ideal = total_pop / n_districts

        district_pops = np.zeros(n_districts)
        for d in range(n_districts):
            mask = self.assignment == d
            district_pops[d] = self.populations[mask].sum()

        deviations = (district_pops - ideal) / ideal
        return {
            "ideal_population": float(ideal),
            "max_deviation": float(np.max(np.abs(deviations))),
            "min_deviation": float(np.min(deviations)),
            "total_population": int(total_pop),
        }

    def check_contiguity(self) -> list[int]:
        """
        Check which precincts are disconnected from their district's main component.

        Returns:
            List of disconnected precincts
        """
        disconnected = []
        visited = set()

        for p in range(self.n_precincts):
            if p in visited or self.assignment[p] < 0:
                continue

            d = self.assignment[p]
            component = self._flood_fill(p, visited)
            # Any precinct in this district not in the component is disconnected
            for q in range(self.n_precincts):
                if q not in component and self.assignment[q] == d:
                    disconnected.append(q)

        return disconnected

    def _flood_fill(self, start: int, visited: set[int]) -> set[int]:
        """BFS flood-fill from start, returning connected component."""
        component = {start}
        queue = [start]
        visited.add(start)

        while queue:
            node = queue.pop(0)
            for neighbor in self.adj_list[node]:
                if neighbor not in visited and self.assignment[neighbor] == self.assignment[start]:
                    visited.add(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)

        return component
