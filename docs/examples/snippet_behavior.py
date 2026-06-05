"""
Behavior Engine — verify custom behavior composition.

Mirrors README Custom Behavior Engine snippet.
"""

from electoral_sim import (
    ElectionModel,
    BehaviorEngine,
    ProximityModel,
    ValenceModel,
    StrategicVotingModel,
    RetrospectiveModel,
)


def test_behavior_engine_creation():
    """BehaviorEngine can be created with multiple models."""
    engine = BehaviorEngine()
    assert len(engine.models) == 0

    engine.add_model(ProximityModel(weight=1.0))
    engine.add_model(ValenceModel(weight=0.5))
    engine.add_model(StrategicVotingModel(sensitivity=2.0))
    assert len(engine.models) == 3


def test_behavior_engine_in_election():
    """Custom BehaviorEngine works inside ElectionModel."""
    engine = BehaviorEngine()
    engine.add_model(ProximityModel(weight=1.0))
    engine.add_model(ValenceModel(weight=0.5))
    engine.add_model(RetrospectiveModel(weight=1.0))

    model = ElectionModel(n_voters=2000, seed=42, behavior_engine=engine)
    results = model.run_election()
    assert "turnout" in results


if __name__ == "__main__":
    test_behavior_engine_creation()
    test_behavior_engine_in_election()
    print("All behavior engine snippets: OK")
