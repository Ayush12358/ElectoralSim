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
Basic Election — verify ElectionModel creation, run, and result keys.

Mirrors README Quick Start snippet. Run in CI to prevent signature drift.
"""

from electoral_sim import ElectionModel


def test_basic_election():
    """Basic election with 100K voters returns expected result keys."""
    model = ElectionModel(n_voters=100_000, seed=42)
    results = model.run_election()

    assert hasattr(results, "__getitem__")  # dict or ElectionResult
    assert "turnout" in results
    assert "gallagher" in results
    assert "enp_votes" in results


def test_chainable_api():
    """Chainable API: with_system + with_allocation + with_threshold."""
    results = (
        ElectionModel(n_voters=50_000, seed=42)
        .with_system("PR")
        .with_allocation("sainte_lague")
        .with_threshold(0.05)
        .run_election()
    )
    assert hasattr(results, "__getitem__")  # dict or ElectionResult
    assert results.get("system") == "PR" or "seats" in results


def test_preset_loading():
    """from_preset loads country configs and runs simulation."""
    for preset in ["germany", "uk", "usa", "brazil"]:
        try:
            model = ElectionModel.from_preset(preset, n_voters=1000, seed=42)
            results = model.run_election()
            assert hasattr(results, "__getitem__")  # dict or ElectionResult
            assert "seats" in results or "turnout" in results
        except Exception as e:
            raise AssertionError(f"Preset {preset} failed: {e}")


if __name__ == "__main__":
    test_basic_election()
    test_chainable_api()
    test_preset_loading()
    print("All basic election snippets: OK")
