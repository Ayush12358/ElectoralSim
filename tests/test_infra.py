"""Tests for infrastructure: CLI, EventManager, and Visualization."""

import sys

import numpy as np
import pytest


# =============================================================================
# CLI
# =============================================================================


class TestCLI:
    """CLI smoke tests."""

    def _run_cli(self, *args):
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "electoral_sim.core.cli", *args],
            capture_output=True, text=True,
        )
        return result

    def test_version(self):
        result = self._run_cli("--version")
        assert result.returncode == 0
        assert "0.1" in result.stdout

    def test_no_args_shows_help(self):
        result = self._run_cli()
        assert result.returncode == 0

    def test_list_presets(self):
        result = self._run_cli("list-presets")
        assert result.returncode == 0

    def test_run_help(self):
        result = self._run_cli("run", "--help")
        assert result.returncode == 0
        assert "--voters" in result.stdout or "--preset" in result.stdout

    def test_run_basic(self):
        result = self._run_cli("run", "--voters", "500", "--constituencies", "3")
        assert result.returncode == 0

    def test_invalid_command(self):
        result = self._run_cli("nonexistent_command")
        assert result.returncode != 0


# =============================================================================
# EVENT MANAGER
# =============================================================================


class TestEventManager:
    """EventManager lifecycle, modifiers, and expiry."""

    def test_event_end_step_property(self):
        from electoral_sim.events.event_manager import Event

        e = Event(id=1, type="scandal", start_step=10, duration=5, severity=20.0)
        assert e.end_step == 15

    def test_initial_state(self):
        from electoral_sim.events.event_manager import EventManager

        em = EventManager(np.random.default_rng(42))
        assert len(em.active_events) == 0
        assert em.current_step == 0

    def test_generates_scandal_when_prob_1(self):
        from electoral_sim.events.event_manager import EventManager

        em = EventManager(np.random.default_rng(42), prob_scandal=1.0, prob_shock=0.0)
        new = em.step(n_parties=5)
        assert len(new) == 1
        assert new[0].type == "scandal"

    def test_generates_shock_when_prob_1(self):
        from electoral_sim.events.event_manager import EventManager

        em = EventManager(np.random.default_rng(42), prob_scandal=0.0, prob_shock=1.0)
        new = em.step(n_parties=5)
        assert len(new) == 1
        assert new[0].type == "economic_shock"

    def test_no_events_when_probs_zero(self):
        from electoral_sim.events.event_manager import EventManager

        em = EventManager(np.random.default_rng(42), prob_scandal=0.0, prob_shock=0.0)
        new = em.step(n_parties=5)
        assert len(new) == 0

    def test_events_expire_after_duration(self):
        from electoral_sim.events.event_manager import Event, EventManager

        em = EventManager(np.random.default_rng(42), prob_scandal=0.0, prob_shock=0.0)
        e = Event(id=0, type="scandal", start_step=1, duration=3, severity=20.0, target_party_id=0)
        em.active_events.append(e)
        em.current_step = 1

        em.current_step = 2
        em.step(n_parties=5)  # step=3, end_step=4 > 3
        assert len(em.active_events) == 1

        em.current_step = 3
        em.step(n_parties=5)  # step=4, end_step=4 NOT > 4
        assert len(em.active_events) == 0

    def test_get_valence_modifiers_returns_penalties(self):
        from electoral_sim.events.event_manager import Event, EventManager

        em = EventManager(np.random.default_rng(42))
        e = Event(id=0, type="scandal", start_step=5, duration=10, severity=30.0, target_party_id=2)
        em.active_events.append(e)
        em.current_step = 5

        modifiers = em.get_valence_modifiers()
        assert 2 in modifiers
        assert modifiers[2] < 0
        assert abs(modifiers[2] + 30.0) < 0.01

    def test_valence_modifiers_decay(self):
        from electoral_sim.events.event_manager import Event, EventManager

        em = EventManager(np.random.default_rng(42))
        e = Event(id=0, type="scandal", start_step=5, duration=10, severity=30.0, target_party_id=2)
        em.active_events.append(e)
        em.current_step = 10  # halfway

        modifiers = em.get_valence_modifiers()
        assert abs(modifiers[2] + 15.0) < 0.01

    def test_get_economic_modifier(self):
        from electoral_sim.events.event_manager import Event, EventManager

        em = EventManager(np.random.default_rng(42))
        e = Event(id=0, type="economic_shock", start_step=5, duration=10, severity=-3.0)
        em.active_events.append(e)
        em.current_step = 5

        mod = em.get_economic_modifier()
        assert abs(mod + 3.0) < 0.01

    def test_event_counter_increments(self):
        from electoral_sim.events.event_manager import EventManager

        em = EventManager(np.random.default_rng(42), prob_scandal=1.0, prob_shock=0.0)
        em.step(n_parties=5)
        assert em.event_counter == 1
        em.step(n_parties=5)
        assert em.event_counter == 2


# =============================================================================
# VISUALIZATION
# =============================================================================


class TestVisualizationPlots:
    """Smoke tests for visualization plots."""

    @pytest.fixture
    def sample_results(self):
        return {
            "system": "FPTP",
            "seats": np.array([4, 2, 1, 0]),
            "vote_counts": np.array([3000, 2000, 1000, 500]),
            "n_constituencies": 7,
            "turnout": 0.75,
            "gallagher": 12.5,
        }

    @pytest.fixture
    def party_names(self):
        return ["Party A", "Party B", "Party C", "Party D"]

    def test_plot_seat_distribution(self, sample_results, party_names):
        from electoral_sim.visualization.plots import plot_seat_distribution

        fig = plot_seat_distribution(sample_results, party_names)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_plot_vote_shares(self, sample_results, party_names):
        from electoral_sim.visualization.plots import plot_vote_shares

        fig = plot_vote_shares(sample_results, party_names)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_plot_seats_vs_votes(self, sample_results, party_names):
        from electoral_sim.visualization.plots import plot_seats_vs_votes

        fig = plot_seats_vs_votes(sample_results, party_names)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_plot_ideological_space(self):
        from electoral_sim.visualization.plots import plot_ideological_space

        voter_positions = np.random.normal(0, 0.3, (200, 2))
        party_positions = np.array([[-0.5, -0.2], [0.3, 0.1], [0.0, 0.3]])
        fig = plot_ideological_space(voter_positions, party_positions, ["Left", "Center", "Right"])
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_plot_election_summary(self, sample_results, party_names):
        from electoral_sim.visualization.plots import plot_election_summary

        fig = plot_election_summary(sample_results, party_names)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_plot_with_custom_colors(self, sample_results, party_names):
        from electoral_sim.visualization.plots import plot_seat_distribution

        fig = plot_seat_distribution(sample_results, party_names, colors=["#FF0000", "#00FF00", "#0000FF", "#FFFF00"])
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)
