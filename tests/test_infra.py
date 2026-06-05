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

"""Tests for infrastructure: CLI, EventManager, and Visualization."""

import sys
import types
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

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

    def test_animate_opinion_dynamics_save(self, tmp_path):
        """animate_opinion_dynamics saves animation to file when filename provided."""
        import polars as pl
        from electoral_sim.visualization.specialized import animate_opinion_dynamics

        history = []
        for _ in range(2):
            df = pl.DataFrame(
                {
                    "ideology_x": np.random.normal(0, 0.3, 20),
                    "ideology_y": np.random.normal(0, 0.3, 20),
                }
            )
            history.append(df)

        party_pos = np.array([[-0.5, -0.2], [0.3, 0.1]])
        party_names = ["Left", "Right"]
        outfile = str(tmp_path / "test_animation.gif")

        ani = animate_opinion_dynamics(history, party_pos, party_names, filename=outfile)
        assert ani is not None
        import os

        assert os.path.exists(outfile)

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


class TestPackaging:
    """Package integrity tests."""

    def test_py_typed_marker_exists(self):
        """py.typed marker is present for PEP 561 compliance."""
        import electoral_sim

        pkg_dir = Path(electoral_sim.__file__).parent
        assert (pkg_dir / "py.typed").exists(), "py.typed marker missing"

    def test_py_typed_in_manifest(self):
        """py.typed is listed in MANIFEST.in for sdist inclusion."""
        manifest = REPO_ROOT / "MANIFEST.in"
        content = manifest.read_text()
        assert "py.typed" in content, "py.typed not in MANIFEST.in"


class TestVisualizationReturnTypes:
    """Verify visualization functions return correct types (Matplotlib vs Plotly)."""

    def test_seat_distribution_returns_matplotlib(self):
        """plot_seat_distribution returns matplotlib Figure, not Plotly."""
        import matplotlib.figure
        from electoral_sim.visualization.plots import plot_seat_distribution

        fig = plot_seat_distribution({"seats": np.array([100, 80, 30])}, ["A", "B", "C"])
        assert isinstance(fig, matplotlib.figure.Figure), (
            f"Expected matplotlib Figure, got {type(fig).__name__}. "
            "Use st.pyplot() not st.plotly_chart() in app.py."
        )

    def test_vote_shares_returns_matplotlib(self):
        """plot_vote_shares returns matplotlib Figure, not Plotly."""
        import matplotlib.figure
        from electoral_sim.visualization.plots import plot_vote_shares

        fig = plot_vote_shares({"vote_counts": np.array([100, 80, 30])}, ["A", "B", "C"])
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_seats_vs_votes_returns_matplotlib(self):
        """plot_seats_vs_votes returns matplotlib Figure, not Plotly."""
        import matplotlib.figure
        from electoral_sim.visualization.plots import plot_seats_vs_votes

        fig = plot_seats_vs_votes(
            {
                "vote_counts": np.array([100, 80, 30]),
                "seats": np.array([5, 3, 2]),
                "gallagher": 0.05,
            },
            ["A", "B", "C"],
        )
        assert isinstance(fig, matplotlib.figure.Figure)


class TestVisualRegressionSmoke:
    """Smoke tests verifying plots don't crash and produce non-empty figures."""

    def test_all_plots_non_empty_axes(self):
        """All standard plot functions return figures with non-empty axes."""
        import matplotlib.figure
        from electoral_sim.visualization.plots import (
            plot_seat_distribution,
            plot_vote_shares,
            plot_seats_vs_votes,
            plot_ideological_space,
        )

        data = {
            "seats": np.array([100, 80, 30]),
            "vote_counts": np.array([100, 80, 30]),
            "gallagher": 5.0,
        }
        names = ["A", "B", "C"]
        positions = np.array([[-0.5, -0.2], [0.3, 0.1], [0.0, 0.3]])

        for func, args in [
            (plot_seat_distribution, (data, names)),
            (plot_vote_shares, (data, names)),
            (plot_seats_vs_votes, (data, names)),
        ]:
            fig = func(*args)
            assert isinstance(fig, matplotlib.figure.Figure)
            assert len(fig.axes) > 0

        fig = plot_ideological_space(
            np.random.default_rng(42).normal(0, 0.3, (20, 2)), positions, names
        )
        assert isinstance(fig, matplotlib.figure.Figure)
        assert len(fig.axes) > 0


class TestBenchmarkSmoke:
    """CI smoke tests for benchmark code paths."""

    def test_benchmark_voter_creation_smoke(self):
        """benchmark_voter_creation runs without crash with small voter counts."""
        pytest.importorskip("benchmarks")
        from benchmarks.benchmark_core import benchmark_voter_creation

        result = benchmark_voter_creation(n_voters=500, n_constituencies=3)
        assert result["n_voters"] == 500
        assert result["time_ms"] > 0

    def test_benchmark_election_smoke(self):
        """benchmark_election runs without crash with small voter counts."""
        pytest.importorskip("benchmarks")
        from benchmarks.benchmark_core import benchmark_election

        result = benchmark_election(n_voters=500, system="FPTP")
        assert result["n_voters"] == 500
        assert result["time_ms"] > 0

    def test_benchmark_batch_throughput_smoke(self):
        """benchmark_batch_throughput runs without crash with small voter counts."""
        pytest.importorskip("benchmarks")
        from benchmarks.benchmark_core import benchmark_batch_throughput

        result = benchmark_batch_throughput(n_voters=500, n_elections=3)
        assert result is not None


class TestOptionalDependencyBoundaries:
    """Verify graceful degradation when optional dependencies are missing."""

    def test_viz_availability_flag(self):
        """electoral_sim sets _VIZ_AVAILABLE flag correctly."""
        import electoral_sim

        assert hasattr(electoral_sim, "_VIZ_AVAILABLE")
        assert isinstance(electoral_sim._VIZ_AVAILABLE, bool)

    def test_numba_fallback_available(self):
        """Numba acceleration module has NUMBA_AVAILABLE flag."""
        from electoral_sim.engine.numba_accel import NUMBA_AVAILABLE

        assert isinstance(NUMBA_AVAILABLE, bool)

    def test_networkx_fallback_available(self):
        """Opinion dynamics module has NETWORKX_AVAILABLE flag."""
        from electoral_sim.dynamics.opinion_dynamics import NETWORKX_AVAILABLE

        assert isinstance(NETWORKX_AVAILABLE, bool)

    def test_gpu_gating_graceful(self):
        """GPU gating function returns bool without crashing."""
        from electoral_sim.engine.gpu_accel import is_gpu_available

        result = is_gpu_available()
        assert isinstance(result, bool)

    def test_election_timeline_step(self):
        """ElectionTimeline triggers events at scheduled steps."""
        from electoral_sim.events.timeline import ElectionTimeline

        tl = ElectionTimeline(total_steps=30, debate_steps=[10], poll_steps=[15])
        for _ in range(30):
            result = tl.step()
            if result["step"] == 10:
                assert any(e["event"] == "debate" for e in result["events"])
            if result["step"] == 30:
                assert any(e["event"] == "election_day" for e in result["events"])
        assert tl.is_election_day()

    def test_poll_generator(self):
        """PollGenerator creates polls with house effects and sampling error."""
        from electoral_sim.events.timeline import PollGenerator

        pg = PollGenerator(sample_size=1000, house_effect=0.02)
        result = pg.generate_poll(np.array([0.4, 0.35, 0.25]), rng=np.random.default_rng(42))
        assert abs(result["poll_shares"].sum() - 1.0) < 0.01
        assert len(result["poll_shares"]) == 3
        assert "house_effect" in result
