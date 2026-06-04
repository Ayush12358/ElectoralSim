"""Tests for opinion dynamics, social networks, and related models."""

import pytest
import numpy as np


class TestNetworkGeneration:
    """All 4 network topologies + stats."""

    def test_barabasi_albert(self):
        from electoral_sim.dynamics.opinion_dynamics import generate_network

        adj_list, G = generate_network(50, topology="barabasi_albert", m=3)
        assert len(adj_list) == 50

    def test_watts_strogatz(self):
        from electoral_sim.dynamics.opinion_dynamics import generate_network

        adj_list, G = generate_network(50, topology="watts_strogatz", k=4, p=0.1)
        assert len(adj_list) == 50

    def test_erdos_renyi(self):
        from electoral_sim.dynamics.opinion_dynamics import generate_network

        adj_list, G = generate_network(50, topology="erdos_renyi", p=0.1)
        assert len(adj_list) == 50
        assert G.number_of_nodes() == 50

    def test_random_regular(self):
        from electoral_sim.dynamics.opinion_dynamics import generate_network

        adj_list, G = generate_network(20, topology="random_regular", d=4)
        assert len(adj_list) == 20

    def test_unknown_topology_raises(self):
        from electoral_sim.dynamics.opinion_dynamics import generate_network

        with pytest.raises(ValueError, match="Unknown topology"):
            generate_network(50, topology="nonexistent")

    def test_network_stats(self):
        from electoral_sim.dynamics.opinion_dynamics import generate_network, network_stats

        _, G = generate_network(30, topology="barabasi_albert", m=2)
        stats = network_stats(G)
        for key in ["n_nodes", "n_edges", "avg_degree", "max_degree", "clustering_coeff"]:
            assert key in stats


class TestOpinionModels:
    """Noisy voter and bounded confidence models."""

    def test_noisy_voter_step(self):
        from electoral_sim.dynamics.opinion_dynamics import generate_network, noisy_voter_step

        adj_list, _ = generate_network(50, topology="barabasi_albert", m=3)
        opinions = np.random.randint(0, 3, 50)
        new = noisy_voter_step(opinions, adj_list, noise_rate=0.01)
        assert len(new) == 50

    def test_noisy_voter_preserves_range(self):
        from electoral_sim.dynamics.opinion_dynamics import generate_network, noisy_voter_step

        adj_list, _ = generate_network(30, topology="barabasi_albert", m=3)
        opinions = np.random.randint(0, 3, 30)
        new = noisy_voter_step(opinions, adj_list, noise_rate=0.5)
        assert new.min() >= 0
        assert new.max() <= 2

    def test_bounded_confidence_step(self):
        from electoral_sim.dynamics.opinion_dynamics import bounded_confidence_step, generate_network

        adj_list, _ = generate_network(30, topology="barabasi_albert", m=3)
        opinions = np.random.uniform(-1, 1, 30)
        new = bounded_confidence_step(opinions, adj_list, epsilon=0.3)
        assert len(new) == 30


class TestOpinionDynamicsClass:
    """OpinionDynamics class: step, simulate, zealots, media, FPTP susceptibility."""

    def test_step_noisy_voter(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=100, topology="barabasi_albert", m=3, seed=42)
        opinions = np.random.randint(0, 3, 100)
        new = od.step(opinions, model="noisy_voter", noise_rate=0.01)
        assert len(new) == 100

    def test_step_bounded_confidence(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=100, topology="barabasi_albert", m=3, seed=42)
        opinions = np.random.uniform(-1, 1, 100)
        new = od.step(opinions, model="bounded_confidence", epsilon=0.3)
        assert len(new) == 100

    def test_invalid_model_raises(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=50, topology="barabasi_albert", m=2, seed=42)
        opinions = np.random.randint(0, 3, 50)
        with pytest.raises(ValueError, match="Unknown model"):
            od.step(opinions, model="nonexistent_model")

    def test_set_zealots_and_step(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=100, topology="barabasi_albert", m=3, seed=42)
        opinions = np.random.randint(0, 3, 100)
        od.set_zealots(np.array([0, 1, 2]), opinions)
        new = od.step(opinions, model="noisy_voter", use_zealots=True)
        assert new[0] == opinions[0]
        assert new[1] == opinions[1]
        assert new[2] == opinions[2]

    def test_simulate_returns_history(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=50, topology="barabasi_albert", m=2, seed=42)
        opinions = np.random.randint(0, 3, 50)
        history = od.simulate(opinions, n_steps=5, model="noisy_voter")
        assert len(history) == 6  # initial + 5 steps

    def test_get_opinion_shares(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=100, topology="barabasi_albert", m=3, seed=42)
        opinions = np.random.randint(0, 4, 100)
        shares = od.get_opinion_shares(opinions, n_parties=4)
        assert abs(shares.sum() - 1.0) < 0.01

    def test_media_influence_bounded_confidence(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=200, topology="barabasi_albert", m=3, seed=42)
        opinions = np.zeros(200)
        new = od.step(opinions, model="bounded_confidence", media_bias=0.8, media_strength=0.3)
        assert new.mean() > opinions.mean()

    def test_fptp_system_susceptibility(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=200, topology="barabasi_albert", m=3, seed=42)
        opinions = np.zeros(200)
        new_pr = od.step(opinions.copy(), model="bounded_confidence",
                         media_bias=0.8, media_strength=0.2, system="PR")
        new_fptp = od.step(opinions.copy(), model="bounded_confidence",
                           media_bias=0.8, media_strength=0.2, system="FPTP")
        assert abs(new_fptp.mean()) >= abs(new_pr.mean())

    def test_precompute_neighbor_arrays(self):
        from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

        od = OpinionDynamics(n_agents=100, topology="barabasi_albert", m=3, seed=42)
        assert len(od.neighbor_starts) == 100
        assert len(od.neighbor_ends) == 100
        assert len(od.neighbors_flat) > 0
