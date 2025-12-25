"""
Party Strategy Module

Implements adaptive strategies for political parties to update
their policy positions based on voter distribution and polling.
"""

from typing import Literal

import numpy as np
import polars as pl


def adaptive_strategy_step(
    parties_df: pl.DataFrame,
    voters_df: pl.DataFrame,
    strategy: Literal["median_voter", "stick_to_base", "random_walk"] = "median_voter",
    learning_rate: float = 0.01,
    noise: float = 0.0,
    rng: np.random.Generator | None = None,
) -> pl.DataFrame:
    """
    Update party positions based on strategy.

    Args:
        parties_df: Party DataFrame
        voters_df: Voter DataFrame
        strategy:
            - "median_voter": Move towards median voter
            - "stick_to_base": Move towards party supporters mean (requires voting history)
            - "random_walk": Random movement
        learning_rate: How much to move per step (0-1)
        noise: Random noise added to movement
        rng: Random generator

    Returns:
        Updated parties DataFrame
    """
    if rng is None:
        rng = np.random.default_rng()

    n_parties = len(parties_df)

    # Extract current positions
    # We handle potential missing columns gracefully
    has_x = "position_x" in parties_df.columns
    has_y = "position_y" in parties_df.columns

    if not has_x:
        return parties_df

    pos_x = parties_df["position_x"].to_numpy().copy()
    pos_y = parties_df["position_y"].to_numpy().copy() if has_y else np.zeros(n_parties)

    if strategy == "median_voter":
        # Calculate Voter Centroid (Median Voter Theorem)
        # Using median is more robust than mean for stability
        voter_median_x = voters_df["ideology_x"].median()
        voter_median_y = (
            voters_df["ideology_y"].median() if "ideology_y" in voters_df.columns else 0.0
        )

        # Calculate vector to median
        dx = voter_median_x - pos_x
        dy = voter_median_y - pos_y

        # Move towards median
        pos_x += learning_rate * dx
        pos_y += learning_rate * dy

    elif strategy == "random_walk":
        # Just drift
        pos_x += rng.normal(0, learning_rate, n_parties)
        pos_y += rng.normal(0, learning_rate, n_parties)

    # Add noise
    if noise > 0:
        pos_x += rng.normal(0, noise, n_parties)
        pos_y += rng.normal(0, noise, n_parties)

    # Clip to bounds [-1, 1]
    pos_x = np.clip(pos_x, -1, 1)
    pos_y = np.clip(pos_y, -1, 1)

    # Update DataFrame
    update_dict = {"position_x": pos_x}
    if has_y:
        update_dict["position_y"] = pos_y

    return parties_df.with_columns([pl.Series(k, v) for k, v in update_dict.items()])
