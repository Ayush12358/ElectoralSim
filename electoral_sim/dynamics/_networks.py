"""Social network generation and diagnostics.

Extracted from opinion_dynamics.py to keep each file under the 250-LOC ceiling.
"""

from typing import Literal

import numpy as np

try:
    import networkx as nx

    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    nx = None


def generate_network(
    n_agents: int,
    topology: Literal[
        "barabasi_albert", "watts_strogatz", "erdos_renyi", "random_regular"
    ] = "barabasi_albert",
    **kwargs,
) -> tuple[list[list[int]], "nx.Graph"]:
    """Generate a social network as adjacency list.

    Args:
        n_agents: Number of nodes
        topology: Network type
        **kwargs: Topology-specific parameters

    Returns:
        Adjacency list as array of neighbor lists, and NetworkX graph
    """
    if not NETWORKX_AVAILABLE:
        raise ImportError("NetworkX required for network generation. pip install networkx")

    if topology == "barabasi_albert":
        m = kwargs.get("m", 3)
        G = nx.barabasi_albert_graph(n_agents, m)
    elif topology == "watts_strogatz":
        k = kwargs.get("k", 4)
        p = kwargs.get("p", 0.1)
        G = nx.watts_strogatz_graph(n_agents, k, p)
    elif topology == "erdos_renyi":
        p = kwargs.get("p", 0.01)
        G = nx.erdos_renyi_graph(n_agents, p)
    elif topology == "random_regular":
        d = kwargs.get("d", 4)
        G = nx.random_regular_graph(d, n_agents)
    else:
        raise ValueError(f"Unknown topology: {topology}")

    adj_list = [list(G.neighbors(i)) for i in range(n_agents)]
    return adj_list, G


def network_stats(G) -> dict:
    """Compute basic network statistics."""
    if not NETWORKX_AVAILABLE:
        return {}

    degrees = [d for _, d in G.degree()]

    return {
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "avg_degree": np.mean(degrees),
        "max_degree": max(degrees),
        "clustering_coeff": nx.average_clustering(G),
    }


def network_diagnostics(G, opinions: np.ndarray | None = None) -> dict:
    """Comprehensive network diagnostics: degree distribution, clustering,
    connected components, homophily, and influence concentration.

    Args:
        G: NetworkX graph
        opinions: Optional opinion vector for homophily computation

    Returns:
        Dict with network metrics
    """
    if not NETWORKX_AVAILABLE:
        return {}

    degrees = [d for _, d in G.degree()]
    n = G.number_of_nodes()

    deg_array = np.array(degrees)
    degree_stats = {
        "mean": float(np.mean(deg_array)),
        "std": float(np.std(deg_array)),
        "median": float(np.median(deg_array)),
        "max": int(max(degrees)),
    }

    if G.is_directed():
        n_components = nx.number_weakly_connected_components(G)
        largest_cc = max(len(c) for c in nx.weakly_connected_components(G)) if n > 0 else 0
    else:
        n_components = nx.number_connected_components(G)
        largest_cc = max(len(c) for c in nx.connected_components(G)) if n > 0 else 0

    homophily = 0.0
    if opinions is not None and len(opinions) == n:
        edges = list(G.edges())
        if edges:
            same_count = sum(1 for u, v in edges if opinions[u] == opinions[v])
            homophily = same_count / len(edges)

    sorted_deg = np.sort(deg_array)
    index = np.arange(1, n + 1)
    influence_gini = float((2 * index - n - 1).dot(sorted_deg) / (n * sorted_deg.sum())) if sorted_deg.sum() > 0 else 0.0

    return {
        "degree_distribution": degree_stats,
        "clustering_coefficient": nx.average_clustering(G),
        "connected_components": n_components,
        "largest_component_size": largest_cc,
        "homophily": homophily,
        "influence_gini": influence_gini,
    }
