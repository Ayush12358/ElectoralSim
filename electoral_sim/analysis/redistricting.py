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
        self.populations = (
            populations if populations is not None else np.ones(n_precincts, dtype=int)
        )
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


def recom_proposal(
    graph: PrecinctGraph,
    dist_a: int,
    dist_b: int,
    rng: np.random.Generator | None = None,
) -> np.ndarray | None:
    """
    ReCom-style spanning-tree recombination for adjacent districts.

    Merges two adjacent districts, builds a spanning tree over the merged
    region, and cuts a balanced edge to create a new district assignment.

    Args:
        graph: PrecinctGraph with current district assignments
        dist_a: First district ID
        dist_b: Second (adjacent) district ID
        rng: Random generator

    Returns:
        New assignment array, or None if recombination fails
    """
    if rng is None:
        rng = np.random.default_rng()

    # Collect precincts from both districts
    merged = np.where((graph.assignment == dist_a) | (graph.assignment == dist_b))[0]
    if len(merged) == 0:
        return None

    # Build adjacency within merged region
    merged_set = set(merged)
    internal_adj = {}
    for p in merged:
        internal_adj[p] = [n for n in graph.adj_list[p] if n in merged_set]

    # Random spanning tree via BFS
    root = int(rng.choice(merged))
    tree_edges = []
    visited = {root}
    queue = [root]

    while queue:
        node = queue.pop(rng.integers(len(queue)))
        neighbors = [n for n in internal_adj[node] if n not in visited]
        rng.shuffle(neighbors)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                tree_edges.append((node, neighbor))
                queue.append(neighbor)

    if len(tree_edges) == 0:
        return None

    # Cut a random edge to balance populations
    edge_idx = rng.integers(len(tree_edges))
    tree_edges.pop(edge_idx)

    # Build tree adjacency from remaining edges (after cut)
    tree_adj = {p: [] for p in merged}
    for u, v in tree_edges:
        tree_adj[u].append(v)
        tree_adj[v].append(u)

    # Reconstruct districts from cut tree (BFS from root)
    new_assignment = graph.assignment.copy()
    new_a = set()
    bfs_visited = {root}
    queue = [root]

    while queue:
        node = queue.pop(0)
        new_a.add(node)
        new_assignment[node] = dist_a
        for neighbor in tree_adj[node]:
            if neighbor not in bfs_visited:
                bfs_visited.add(neighbor)
                queue.append(neighbor)

    # Remaining merged precincts go to dist_b
    for p in merged:
        if p not in new_a:
            new_assignment[p] = dist_b

    return new_assignment


from electoral_sim.analysis._ensemble import ensemble_analysis  # noqa: E402, F401
