"""Tests for infrastructure: CLI, EventManager, and Visualization."""

import sys
import types

import numpy as np
import pytest

# =============================================================================
# CLI — Direct function tests (not subprocess, so coverage tracks)
# =============================================================================


class TestCLIDirect:
    """Test CLI functions directly for coverage tracking."""

    def test_list_presets(self, capsys):
        """list_presets() prints preset info."""
        from electoral_sim.core.cli import list_presets

        list_presets()
        output = capsys.readouterr().out
        assert "india" in output
        assert "usa" in output
        assert "Total:" in output

    def test_run_simulation_basic(self, capsys):
        """run_simulation() with basic args."""
        from electoral_sim.core.cli import run_simulation

        args = types.SimpleNamespace(
            preset=None,
            voters=500,
            constituencies=3,
            system="FPTP",
            allocation="dhondt",
            threshold=0.0,
            seed=42,
            output=None,
            quiet=False,
        )
        run_simulation(args)
        output = capsys.readouterr().out
        assert "Turnout" in output
        assert "Party Results" in output

    def test_run_simulation_quiet(self, capsys):
        """run_simulation() with quiet=True suppresses output."""
        from electoral_sim.core.cli import run_simulation

        args = types.SimpleNamespace(
            preset=None,
            voters=500,
            constituencies=3,
            system="FPTP",
            allocation="dhondt",
            threshold=0.0,
            seed=42,
            output=None,
            quiet=True,
        )
        run_simulation(args)
        output = capsys.readouterr().out
        assert output == ""

    def test_run_simulation_with_preset(self, capsys):
        """run_simulation() with a preset."""
        from electoral_sim.core.cli import run_simulation

        args = types.SimpleNamespace(
            preset="usa",
            voters=500,
            constituencies=10,
            system="FPTP",
            allocation="dhondt",
            threshold=0.0,
            seed=42,
            output=None,
            quiet=False,
        )
        run_simulation(args)
        output = capsys.readouterr().out
        assert "preset" in output.lower() or "Turnout" in output

    def test_run_simulation_with_output(self, tmp_path):
        """run_simulation() saves JSON to file."""
        from electoral_sim.core.cli import run_simulation

        outfile = str(tmp_path / "results.json")
        args = types.SimpleNamespace(
            preset=None,
            voters=500,
            constituencies=3,
            system="FPTP",
            allocation="dhondt",
            threshold=0.0,
            seed=42,
            output=outfile,
            quiet=True,
        )
        run_simulation(args)
        import json

        with open(outfile) as f:
            data = json.load(f)
        assert "results" in data
        assert "turnout" in data["results"]
        assert "parties" in data

    def test_run_simulation_with_pr(self, capsys):
        """run_simulation() with PR system."""
        from electoral_sim.core.cli import run_simulation

        args = types.SimpleNamespace(
            preset=None,
            voters=500,
            constituencies=3,
            system="PR",
            allocation="sainte_lague",
            threshold=0.05,
            seed=42,
            output=None,
            quiet=False,
        )
        run_simulation(args)
        output = capsys.readouterr().out
        assert "Turnout" in output

    def test_run_simulation_irv_rejected(self, capsys):
        """run_simulation() with IRV system exits with error."""
        from electoral_sim.core.cli import run_simulation

        args = types.SimpleNamespace(
            preset=None,
            voters=500,
            constituencies=3,
            system="IRV",
            allocation="dhondt",
            threshold=0.0,
            seed=42,
            output=None,
            quiet=False,
        )
        with pytest.raises(SystemExit):
            run_simulation(args)
        captured = capsys.readouterr()
        assert "Unsupported electoral system" in (captured.err + captured.out)

    def test_run_batch_no_config(self):
        """run_batch() without config exits with error."""
        from electoral_sim.core.cli import run_batch

        args = types.SimpleNamespace(
            config=None,
            output="out.csv",
            summary=None,
            jobs=1,
            quiet=True,
        )
        with pytest.raises(SystemExit):
            run_batch(args)

    def test_run_batch_with_config(self, tmp_path):
        """run_batch() with a JSON config file."""
        import json
        from electoral_sim.core.cli import run_batch

        config = {
            "parameters": {"n_voters": [500, 1000]},
            "fixed_params": {"n_constituencies": 3},
            "n_runs_per_config": 1,
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config))

        outfile = str(tmp_path / "results.csv")
        args = types.SimpleNamespace(
            config=str(config_file),
            output=outfile,
            summary=None,
            jobs=1,
            quiet=True,
        )
        run_batch(args)
        assert (tmp_path / "results.csv").exists()

    def test_run_batch_missing_config_file(self):
        """run_batch() with nonexistent config file exits."""
        from electoral_sim.core.cli import run_batch

        args = types.SimpleNamespace(
            config="/nonexistent/config.json",
            output="out.csv",
            summary=None,
            jobs=1,
            quiet=True,
        )
        with pytest.raises(SystemExit):
            run_batch(args)

    def test_main_list_presets(self, capsys):
        """main() with list-presets command."""
        from electoral_sim.core.cli import main

        old_argv = sys.argv
        try:
            sys.argv = ["electoral-sim", "list-presets"]
            main()
            output = capsys.readouterr().out
            assert "Available" in output or "india" in output
        finally:
            sys.argv = old_argv

    def test_main_no_args(self, capsys):
        """main() with no args shows help."""
        from electoral_sim.core.cli import main

        old_argv = sys.argv
        try:
            sys.argv = ["electoral-sim"]
            main()
            output = capsys.readouterr().out
            assert "electoral-sim" in output or "Usage" in output or "usage" in output
        finally:
            sys.argv = old_argv


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
        em.step(n_parties=5)
        assert len(em.active_events) == 1

        em.current_step = 3
        em.step(n_parties=5)
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
        em.current_step = 10

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

    matplotlib = pytest.importorskip("matplotlib")

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

        fig = plot_seat_distribution(
            sample_results, party_names, colors=["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]
        )
        assert fig is not None
        import matplotlib.pyplot as plt

        plt.close(fig)


@pytest.mark.skipif(
    "matplotlib" not in sys.modules,
    reason="matplotlib not installed",
)
class TestVisualizationSpecialized:
    """Tests for visualization/specialized.py (0% coverage)."""

    def test_animate_opinion_dynamics(self):
        """animate_opinion_dynamics creates animation."""
        import polars as pl
        from electoral_sim.visualization.specialized import animate_opinion_dynamics

        # Create minimal history
        history = []
        for _ in range(3):
            df = pl.DataFrame(
                {
                    "ideology_x": np.random.normal(0, 0.3, 50),
                    "ideology_y": np.random.normal(0, 0.3, 50),
                }
            )
            history.append(df)

        party_pos = np.array([[-0.5, -0.2], [0.3, 0.1]])
        party_names = ["Left", "Right"]

        ani = animate_opinion_dynamics(history, party_pos, party_names, interval=50)
        assert ani is not None

    def test_plot_swing_analysis(self):
        """plot_swing_analysis returns a plotly figure."""
        from electoral_sim.visualization.specialized import plot_swing_analysis

        results = {"seats": {"BJP": 300}}
        fig = plot_swing_analysis(results)
        assert fig is not None

    def test_plot_india_state_map(self):
        """plot_india_state_map returns a plotly figure."""
        from electoral_sim.visualization.specialized import plot_india_state_map

        results_summary = {
            "Uttar Pradesh": {"seats": {"BJP": 60, "SP": 15, "INC": 5}},
            "Maharashtra": {"seats": {"BJP": 25, "INC": 15, "Others": 8}},
            "Delhi": {"seats": {"BJP": 5, "AAP": 2}},
        }
        fig = plot_india_state_map(results_summary)
        assert fig is not None

    def test_plot_india_state_map_empty(self):
        """plot_india_state_map returns None for empty data."""
        from electoral_sim.visualization.specialized import plot_india_state_map

        fig = plot_india_state_map({})
        assert fig is None
