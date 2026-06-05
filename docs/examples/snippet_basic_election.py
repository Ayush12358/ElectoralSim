"""
Basic Election — verify ElectionModel creation, run, and result keys.

Mirrors README Quick Start snippet. Run in CI to prevent signature drift.
"""

from electoral_sim import ElectionModel


def test_basic_election():
    """Basic election with 100K voters returns expected result keys."""
    model = ElectionModel(n_voters=100_000, seed=42)
    results = model.run_election()

    assert isinstance(results, dict)
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
    assert isinstance(results, dict)
    assert results.get("system") == "PR" or "seats" in results


def test_preset_loading():
    """from_preset loads country configs and runs simulation."""
    for preset in ["germany", "uk", "usa", "brazil"]:
        try:
            model = ElectionModel.from_preset(preset, n_voters=1000, seed=42)
            results = model.run_election()
    assert hasattr(results, '__getitem__')  # dict or ElectionResult
            assert "seats" in results or "turnout" in results
        except Exception as e:
            raise AssertionError(f"Preset {preset} failed: {e}")


if __name__ == "__main__":
    test_basic_election()
    test_chainable_api()
    test_preset_loading()
    print("All basic election snippets: OK")
