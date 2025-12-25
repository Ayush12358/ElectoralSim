"""
Social Networks and Opinion Dynamics

Implements:
- Network generation (Barabási-Albert, Watts-Strogatz)
- Noisy voter model
- Zealots (fixed-opinion agents)
- Bounded confidence model
"""

from typing import Literal

import numpy as np

try:
    import networkx as nx

    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    nx = None

try:
    from numba import jit, prange

    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False

    def jit(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    prange = range


# =============================================================================
# NETWORK GENERATION
# =============================================================================


def generate_network(
    n_agents: int,
    topology: Literal[
        "barabasi_albert", "watts_strogatz", "erdos_renyi", "random_regular"
    ] = "barabasi_albert",
    **kwargs,
) -> np.ndarray:
    """
    Generate a social network as adjacency list.

    Args:
        n_agents: Number of nodes
        topology: Network type
        **kwargs: Topology-specific parameters

    Returns:
        Adjacency list as array of neighbor lists
    """
    if not NETWORKX_AVAILABLE:
        raise ImportError("NetworkX required for network generation. pip install networkx")

    if topology == "barabasi_albert":
        m = kwargs.get("m", 3)  # Edges to attach per new node
        G = nx.barabasi_albert_graph(n_agents, m)

    elif topology == "watts_strogatz":
        k = kwargs.get("k", 4)  # Each node connected to k nearest neighbors
        p = kwargs.get("p", 0.1)  # Rewiring probability
        G = nx.watts_strogatz_graph(n_agents, k, p)

    elif topology == "erdos_renyi":
        p = kwargs.get("p", 0.01)  # Edge probability
        G = nx.erdos_renyi_graph(n_agents, p)

    elif topology == "random_regular":
        d = kwargs.get("d", 4)  # Degree
        G = nx.random_regular_graph(d, n_agents)

    else:
        raise ValueError(f"Unknown topology: {topology}")

    # Convert to adjacency list
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


# =============================================================================
# OPINION DYNAMICS MODELS
# =============================================================================


def noisy_voter_step(
    opinions: np.ndarray,
    adj_list: list[list[int]],
    noise_rate: float = 0.01,
    rng: np.random.Generator = None,
) -> np.ndarray:
    """
    Noisy voter model: agents copy random neighbor with probability (1-noise).
    With probability noise, they adopt a random opinion.

    Args:
        opinions: Current opinion array (party indices or -1 for undecided)
        adj_list: Adjacency list from network
        noise_rate: Probability of random mutation
        rng: Random generator

    Returns:
        Updated opinions array
    """
    if rng is None:
        rng = np.random.default_rng()

    n_agents = len(opinions)
    n_parties = int(opinions.max()) + 1
    new_opinions = opinions.copy()

    for i in range(n_agents):
        neighbors = adj_list[i]
        if len(neighbors) == 0:
            continue

        if rng.random() < noise_rate:
            # Random mutation
            new_opinions[i] = rng.integers(0, n_parties)
        else:
            # Copy random neighbor
            neighbor = neighbors[rng.integers(len(neighbors))]
            new_opinions[i] = opinions[neighbor]

    return new_opinions


def bounded_confidence_step(
    opinions: np.ndarray,
    adj_list: list[list[int]],
    epsilon: float = 0.3,
    mu: float = 0.5,
    rng: np.random.Generator = None,
) -> np.ndarray:
    """
    Bounded confidence model (Deffuant-Weisbuch):
    Agents only interact if their opinion difference < epsilon.

    Args:
        opinions: Continuous opinions in [-1, 1]
        adj_list: Network adjacency list
        epsilon: Confidence bound
        mu: Convergence rate
        rng: Random generator

    Returns:
        Updated opinions
    """
    if rng is None:
        rng = np.random.default_rng()

    n_agents = len(opinions)
    new_opinions = opinions.copy()

    for i in range(n_agents):
        neighbors = adj_list[i]
        if len(neighbors) == 0:
            continue

        # Pick random neighbor
        j = neighbors[rng.integers(len(neighbors))]

        # Only interact if opinions are close enough
        if abs(opinions[i] - opinions[j]) < epsilon:
            # Move opinions toward each other
            new_opinions[i] += mu * (opinions[j] - opinions[i])
            new_opinions[j] += mu * (opinions[i] - opinions[j])

    return np.clip(new_opinions, -1, 1)


def zealot_step(
    opinions: np.ndarray,
    adj_list: list[list[int]],
    zealot_mask: np.ndarray,
    noise_rate: float = 0.01,
    rng: np.random.Generator = None,
) -> np.ndarray:
    """
    Noisy voter with zealots (fixed-opinion agents).

    Zealots never change their opinion but influence neighbors.

    Args:
        opinions: Current opinions
        adj_list: Network adjacency list
        zealot_mask: Boolean array (True = zealot, fixed opinion)
        noise_rate: Mutation probability for non-zealots
        rng: Random generator

    Returns:
        Updated opinions
    """
    if rng is None:
        rng = np.random.default_rng()

    new_opinions = noisy_voter_step(opinions, adj_list, noise_rate, rng)

    # Restore zealot opinions
    new_opinions[zealot_mask] = opinions[zealot_mask]

    return new_opinions


# =============================================================================
# NUMBA-ACCELERATED VERSIONS
# =============================================================================


@jit(nopython=True, cache=True)
def _noisy_voter_numba(
    opinions: np.ndarray,
    neighbor_starts: np.ndarray,
    neighbor_ends: np.ndarray,
    neighbors_flat: np.ndarray,
    noise_rate: float,
    n_parties: int,
    random_vals: np.ndarray,
    random_neighbors: np.ndarray,
    random_mutations: np.ndarray,
) -> np.ndarray:
    """Numba-accelerated noisy voter step."""
    n_agents = len(opinions)
    new_opinions = opinions.copy()

    for i in range(n_agents):
        start = neighbor_starts[i]
        end = neighbor_ends[i]
        n_neighbors = end - start

        if n_neighbors == 0:
            continue

        if random_vals[i] < noise_rate:
            # Random mutation
            new_opinions[i] = random_mutations[i] % n_parties
        else:
            # Copy neighbor
            neighbor_idx = start + (random_neighbors[i] % n_neighbors)
            neighbor = neighbors_flat[neighbor_idx]
            new_opinions[i] = opinions[neighbor]

    return new_opinions


class OpinionDynamics:
    """
    Manages opinion dynamics simulation.

    Example:
        od = OpinionDynamics(n_agents=10000, topology="barabasi_albert")
        opinions = np.random.randint(0, 3, 10000)

        for _ in range(100):
            opinions = od.step(opinions, model="noisy_voter")
    """

    def __init__(
        self,
        n_agents: int,
        topology: str = "barabasi_albert",
        seed: int | None = None,
        **network_kwargs,
    ):
        self.n_agents = n_agents
        self.rng = np.random.default_rng(seed)

        # Generate network
        self.adj_list, self.graph = generate_network(n_agents, topology, **network_kwargs)
        self.stats = network_stats(self.graph)

        # Precompute flat neighbor arrays for Numba
        self._precompute_neighbor_arrays()

        # Zealot tracking
        self.zealot_mask = np.zeros(n_agents, dtype=bool)

    def _precompute_neighbor_arrays(self) -> None:
        """Convert adjacency list to flat arrays for Numba."""
        neighbor_starts = []
        neighbor_ends = []
        neighbors_flat = []

        pos = 0
        for neighbors in self.adj_list:
            neighbor_starts.append(pos)
            neighbors_flat.extend(neighbors)
            pos += len(neighbors)
            neighbor_ends.append(pos)

        self.neighbor_starts = np.array(neighbor_starts, dtype=np.int64)
        self.neighbor_ends = np.array(neighbor_ends, dtype=np.int64)
        self.neighbors_flat = np.array(neighbors_flat, dtype=np.int64)

    def set_zealots(self, indices: np.ndarray | list, opinions: np.ndarray) -> None:
        """
        Mark certain agents as zealots with fixed opinions.

        Args:
            indices: Agent indices to mark as zealots
            opinions: Current opinion array (zealots keep their current opinion)
        """
        self.zealot_mask[:] = False
        self.zealot_mask[indices] = True
        self.zealot_opinions = opinions[indices].copy()

    def step(
        self,
        opinions: np.ndarray,
        model: Literal["noisy_voter", "bounded_confidence"] = "noisy_voter",
        noise_rate: float = 0.01,
        epsilon: float = 0.3,
        use_zealots: bool = False,
        media_bias: float = 0.0,
        media_strength: float = 0.0,
        system: str = "PR",  # NEW: 'FPTP' or 'PR' (affects susceptibility)
    ) -> np.ndarray:
        """
        Run one step of opinion dynamics.

        Args:
            opinions: Current opinion array
            model: "noisy_voter" or "bounded_confidence"
            noise_rate: Mutation probability (noisy voter)
            epsilon: Confidence bound (bounded confidence)
            use_zealots: Whether to apply zealot constraints
            media_bias: Broadcast media position (-1 to +1)
            media_strength: How strongly media shifts opinions (0-1)
            system: "FPTP" or "PR". Raducha et al. suggest Plurality systems
                   are more susceptible to polarization/waves.

        Returns:
            Updated opinions
        """
        # Apply Electoral System Susceptibility (Raducha et al.)
        # Plurality (FPTP) systems are more susceptible to mobilization/media effects
        # due to the "mechanical effect" amplifying perceived swings.
        effective_media_strength = media_strength
        if system == "FPTP":
            effective_media_strength *= 1.5  # Higher susceptibility in Plurality

        # Apply media influence first (for continuous opinions models)
        if effective_media_strength > 0 and model == "bounded_confidence":
            # Media pulls opinions toward the broadcast position
            media_pull = effective_media_strength * (media_bias - opinions)
            opinions = opinions + media_pull
            opinions = np.clip(opinions, -1, 1)

        if model == "noisy_voter":
            n_parties = int(opinions.max()) + 1

            # For discrete opinions, media bias increases probability of switching to favored party
            if effective_media_strength > 0:
                # Media-influenced random mutations favor the party closest to media_bias
                # (Party 0 = left, higher = right in a left-right spectrum)
                # This is a simplified model: mutation targets the media-favored party more often
                pass  # Discrete media effect handled through zealots or separate mechanism

            if NUMBA_AVAILABLE and len(opinions) > 1000:
                # Use Numba version
                random_vals = self.rng.random(self.n_agents)
                random_neighbors = self.rng.integers(0, 1000, self.n_agents)
                random_mutations = self.rng.integers(0, n_parties, self.n_agents)

                new_opinions = _noisy_voter_numba(
                    opinions.astype(np.int64),
                    self.neighbor_starts,
                    self.neighbor_ends,
                    self.neighbors_flat,
                    noise_rate,
                    n_parties,
                    random_vals,
                    random_neighbors,
                    random_mutations,
                )
            else:
                new_opinions = noisy_voter_step(opinions, self.adj_list, noise_rate, self.rng)

        elif model == "bounded_confidence":
            new_opinions = bounded_confidence_step(opinions, self.adj_list, epsilon, rng=self.rng)
        else:
            raise ValueError(f"Unknown model: {model}")

        # Apply zealot constraints
        if use_zealots and self.zealot_mask.any():
            new_opinions[self.zealot_mask] = self.zealot_opinions

        return new_opinions

    def simulate(
        self,
        initial_opinions: np.ndarray,
        n_steps: int = 100,
        model: str = "noisy_voter",
        **kwargs,
    ) -> list[np.ndarray]:
        """
        Run multiple steps and return opinion history.

        Returns:
            List of opinion arrays at each step
        """
        history = [initial_opinions.copy()]
        opinions = initial_opinions.copy()

        for _ in range(n_steps):
            opinions = self.step(opinions, model, **kwargs)
            history.append(opinions.copy())

        return history

    def get_opinion_shares(self, opinions: np.ndarray, n_parties: int) -> np.ndarray:
        """Calculate share of each opinion/party."""
        counts = np.bincount(opinions.astype(int), minlength=n_parties)
        return counts / len(opinions)


# =============================================================================
# QUICK TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Opinion Dynamics Test")
    print("=" * 50)

    # Create network
    od = OpinionDynamics(n_agents=10_000, topology="barabasi_albert", m=3, seed=42)
    print("\nNetwork stats:")
    for k, v in od.stats.items():
        print(f"  {k}: {v:.2f}" if isinstance(v, float) else f"  {k}: {v}")

    # Initialize opinions (3 parties)
    opinions = od.rng.integers(0, 3, od.n_agents)
    print(f"\nInitial shares: {od.get_opinion_shares(opinions, 3)}")

    # Add zealots (5% of population)
    zealot_indices = od.rng.choice(od.n_agents, size=500, replace=False)
    od.set_zealots(zealot_indices, opinions)

    # Run simulation
    for step in range(50):
        opinions = od.step(opinions, model="noisy_voter", noise_rate=0.01, use_zealots=True)

    print(f"After 50 steps: {od.get_opinion_shares(opinions, 3)}")
    print("=" * 50)
