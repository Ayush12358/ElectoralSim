"""Basic smoke tests for electoral_sim package."""

import pytest


class TestImports:
    """Test that all main modules can be imported."""

    def test_import_main_package(self):
        """Test importing the main package."""
        import electoral_sim

        assert hasattr(electoral_sim, "__version__")
        assert hasattr(electoral_sim, "ElectionModel")

    def test_import_config(self):
        """Test importing configuration classes."""
        from electoral_sim import Config, PartyConfig

        assert Config is not None
        assert PartyConfig is not None

    def test_import_presets(self):
        """Test importing country presets."""
        from electoral_sim import PRESETS

        assert "india" in PRESETS
        assert "usa" in PRESETS
        assert "uk" in PRESETS


class TestBasicModel:
    """Basic model tests that don't require heavy computation."""

    def test_create_simple_model(self):
        """Test creating a basic election model."""
        from electoral_sim import ElectionModel

        model = ElectionModel(
            n_voters=100,
            n_parties=3,
            electoral_system="fptp",
        )
        assert model is not None
        assert model.n_voters == 100
        assert model.n_parties == 3

    def test_run_simple_election(self):
        """Test running a simple election."""
        from electoral_sim import ElectionModel

        model = ElectionModel(
            n_voters=100,
            n_parties=3,
            electoral_system="fptp",
        )
        results = model.run_election()
        assert results is not None
        assert "seats" in results
        assert "votes" in results


class TestVersion:
    """Test version information."""

    def test_version_format(self):
        """Test that version is properly formatted."""
        from electoral_sim import __version__

        parts = __version__.split(".")
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()
