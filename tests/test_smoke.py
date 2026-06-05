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

"""Minimal smoke tests that don't require heavy dependencies."""

import pytest


class TestPackageStructure:
    """Test that the package is properly structured."""

    def test_version_exists(self):
        """Test that __version__ is defined."""
        from electoral_sim import __version__

        assert __version__ is not None
        assert isinstance(__version__, str)
        parts = __version__.split(".")
        assert len(parts) == 3

    def test_main_exports_exist(self):
        """Test that main exports are defined in __init__.py."""
        import electoral_sim

        # Check essential exports exist
        assert hasattr(electoral_sim, "ElectionModel")
        assert hasattr(electoral_sim, "Config")
        assert hasattr(electoral_sim, "PartyConfig")
        assert hasattr(electoral_sim, "PRESETS")

    def test_presets_available(self):
        """Test that PRESETS dictionary is populated."""
        from electoral_sim import PRESETS

        assert isinstance(PRESETS, dict)
        assert len(PRESETS) > 0
        assert "india" in PRESETS


class TestSubmodules:
    """Test that submodules can be imported."""

    def test_import_core(self):
        """Test importing core submodule."""
        from electoral_sim import core

        assert core is not None

    def test_import_behavior(self):
        """Test importing behavior submodule."""
        from electoral_sim import behavior

        assert behavior is not None

    def test_import_systems(self):
        """Test importing systems submodule."""
        from electoral_sim import systems

        assert systems is not None

    def test_import_metrics(self):
        """Test importing metrics submodule."""
        from electoral_sim import metrics

        assert metrics is not None
