"""
Duverger's Law Simulation/Analysis

Simulates repeated elections to demonstrate that Plurality (FPTP) rules
tend towards a two-party system (effective number of parties ~ 2),
while PR systems maintain multi-party diversity.

Duverger's Law mechanics rely on:
1. Mechanical Effect: High threshold for representation in FPTP.
2. Psychological Effect: Strategic voting to avoid wasted votes.
"""

from typing import Literal

import numpy as np

from electoral_sim.behavior.voter_behavior import BehaviorEngine, ProximityModel, WastedVoteModel
from electoral_sim.core.model import ElectionModel


def run_duverger_experiment(
    n_voters: int = 2000,
    n_parties: int = 5,
    n_steps: int = 10,
    system: Literal["FPTP", "PR"] = "FPTP",
    seed: int = 42,
    strategic_penalty: float = 50.0,  # Massive penalty
    viability_threshold: float = 0.15,  # Higher threshold
    temperature: float = 0.1,  # Lower temperature for sharper choices
) -> list[dict]:
    """
    Run a multi-step election simulation with strategic voting.

    Args:
        n_voters: Number of voters
        n_parties: Number of initial parties
        n_steps: Number of elections
        system: Electoral System
        seed: Random seed
        strategic_penalty: Utility penalty for voting for unviable parties
        viability_threshold: Viability threshold
        temperature: Logit temperature (tau)

    Returns:
        List of result dicts containing 'enp', 'vote_shares', etc.
    """
    # 1. Setup Model

    # Custom Behavior Engine with Strategic Voting
    engine = BehaviorEngine()
    engine.add_model(ProximityModel(weight=1.0))
    # Add WastedVoteModel (Strategic Voting)
    engine.add_model(
        WastedVoteModel(penalty=strategic_penalty, viability_threshold=viability_threshold)
    )

    # Manually set parties to ensure they are the same
    positions = np.linspace(-0.8, 0.8, n_parties)
    parties_list = []
    for i, pos in enumerate(positions):
        parties_list.append(
            {"name": f"Party {i+1}", "position_x": pos, "position_y": 0.0, "valence": 50}
        )

    model = ElectionModel(
        n_voters=n_voters,
        electoral_system=system,
        seed=seed,
        behavior_engine=engine,
        temperature=temperature,  # Set temperature
        parties=parties_list,
    )

    history = []

    # Initial viability: All equal (or random?)
    # Assume equal to start so no one is wasted immediately.
    current_viability = np.ones(n_parties) / n_parties

    for step in range(n_steps):
        # Run Election passing 'viability' for WastedVoteModel
        results = model.run_election(viability=current_viability)

        # Calculate ENP (Effective Number of Parties)
        # 1 / Sum(shares^2)
        vote_shares = np.array(results["vote_counts"]) / np.sum(results["vote_counts"])
        enp = 1.0 / np.sum(vote_shares**2)

        history.append(
            {
                "step": step,
                "enp": float(enp),
                "vote_shares": list(vote_shares),
                "winner": int(np.argmax(vote_shares)),
            }
        )

        # Update viability for next round based on this result
        # Only persistent viability matters for strategic calculation
        current_viability = vote_shares

    return history
