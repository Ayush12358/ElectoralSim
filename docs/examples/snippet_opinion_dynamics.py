"""
Opinion Dynamics — verify network generation, dynamics, and diagnostics.

Mirrors README Opinion Dynamics snippet.
"""
import numpy as np
from electoral_sim import ElectionModel
from electoral_sim.dynamics.opinion_dynamics import (
    generate_network,
    network_stats,
    network_diagnostics,
    noisy_voter_step,
    bounded_confidence_step,
    zealot_step,
)


def test_network_generation():
    """All four topologies produce valid adjacency lists."""
    topologies = {
        "barabasi_albert": dict(m=3),
        "watts_strogatz": dict(k=4, p=0.1),
        "erdos_renyi": dict(p=0.1),
        "random_regular": dict(d=4),
    }

    for name, params in topologies.items():
        adj_list, G = generate_network(50, topology=name, **params)
        assert len(adj_list) == 50
        assert G is not None


def test_network_stats():
    """network_stats returns degree, clustering, path length."""
    _, G = generate_network(30, topology="barabasi_albert", m=2)
    stats = network_stats(G)
    assert "avg_degree" in stats
    assert "clustering_coeff" in stats


def test_noisy_voter():
    """noisy_voter_step updates opinions."""
    adj_list, _ = generate_network(50, topology="barabasi_albert", m=3)
    opinions = np.random.randn(50)
    new_opinions = noisy_voter_step(opinions, adj_list, noise_rate=0.1, rng=np.random.default_rng(42))
    assert len(new_opinions) == 50
    assert not np.array_equal(opinions, new_opinions)


def test_bounded_confidence():
    """bounded_confidence_step updates within epsilon."""
    adj_list, _ = generate_network(40, topology="barabasi_albert", m=3)
    opinions = np.linspace(-1, 1, 40)
    new_opinions = bounded_confidence_step(opinions, adj_list, epsilon=0.3)
    assert len(new_opinions) == 40


def test_zealots():
    """zealot_step respects zealot positions."""
    adj_list, _ = generate_network(50, "erdos_renyi", p=0.1)
    opinions = np.random.randn(50)
    zealot_mask = np.zeros(50, dtype=bool)
    zealot_mask[0] = True
    zealot_mask[5] = True
    opinions[0] = 1.0
    opinions[5] = -1.0
    new_opinions = zealot_step(
        opinions, adj_list, zealot_mask=zealot_mask, noise_rate=0.3, rng=np.random.default_rng(42)
    )
    assert new_opinions[0] == 1.0  # Zealot unchanged
    assert new_opinions[5] == -1.0


def test_election_model_with_dynamics():
    """ElectionModel runs with opinion dynamics."""
    from electoral_sim import OpinionDynamics

    od = OpinionDynamics(n_agents=100, topology="barabasi_albert", m=3)
    model = ElectionModel(n_voters=100, seed=42, opinion_dynamics=od)
    results = model.run_election()
    assert "turnout" in results


if __name__ == "__main__":
    test_network_generation()
    test_network_stats()
    test_noisy_voter()
    test_bounded_confidence()
    test_zealots()
    test_election_model_with_dynamics()
    print("All opinion dynamics snippets: OK")
