"""
Voter Generation Module

Contains functions for generating voter DataFrames with demographics,
ideology, and behavioral attributes.
"""

import numpy as np
import polars as pl


def generate_voter_frame(
    n_voters: int,
    n_constituencies: int,
    rng: np.random.Generator,
) -> pl.DataFrame:
    """
    Generate initial voter DataFrame with full demographics.
    
    Includes:
        - Demographics: age, gender, education, income, religion
        - Party ID: 7-point scale (-3 to +3)
        - Ideology: 2D position
        - Turnout probability
        
    Args:
        n_voters: Number of voters to generate
        n_constituencies: Number of constituencies to distribute voters across
        rng: NumPy random generator
        
    Returns:
        Polars DataFrame with all voter attributes
    """
    # Demographics
    age = rng.integers(18, 90, size=n_voters)  # Voting age population
    gender = rng.choice([0, 1], size=n_voters)  # 0=Male, 1=Female
    
    # Education: 0=None, 1=Primary, 2=Secondary, 3=Graduate, 4=Post-grad
    education = rng.choice([0, 1, 2, 3, 4], size=n_voters, p=[0.15, 0.25, 0.30, 0.20, 0.10])
    
    # Income percentile (0-100)
    income = np.clip(rng.lognormal(3.5, 0.8, n_voters), 0, 100)
    
    # Religion: simplified categories (0-5)
    religion = rng.choice([0, 1, 2, 3, 4, 5], size=n_voters, p=[0.65, 0.14, 0.10, 0.05, 0.03, 0.03])
    
    # 7-point Party ID scale: -3=Strong Left, 0=Independent, +3=Strong Right
    # Normally distributed, clipped to range
    party_id_7pt = np.clip(np.round(rng.normal(0, 1.2, n_voters)), -3, 3).astype(int)
    
    # Ideology influenced by demographics
    # Age: older slightly more conservative
    # Education: higher ed slightly more liberal on social issues
    # Income: higher income slightly more conservative on economic
    base_ideology_x = rng.normal(0, 0.3, n_voters)
    base_ideology_y = rng.normal(0, 0.3, n_voters)
    
    ideology_x = np.clip(
        base_ideology_x + 0.005 * (income - 50) + 0.003 * (age - 50),
        -1, 1
    )
    ideology_y = np.clip(
        base_ideology_y - 0.02 * (education - 2) + 0.005 * (age - 50),
        -1, 1
    )
    
    # Political knowledge (0-100) - Beta distribution
    # Higher knowledge correlates with higher turnout
    political_knowledge = rng.beta(2, 5, n_voters) * 100
    
    # Misinformation susceptibility (0-1) - inversely related to education and knowledge
    # Higher susceptibility = more easily influenced by false information
    misinfo_susceptibility = np.clip(
        rng.beta(2, 3, n_voters) - 0.1 * (education / 4) - 0.1 * (political_knowledge / 100),
        0.05, 0.95
    )
    
    # Affective polarization (0-1) - in-group/out-group favorability gap
    # 0 = neutral toward all parties, 1 = highly polarized (loves own party, hates others)
    # Right-skewed: most voters are moderate, fewer are highly polarized
    # Correlates positively with party_id strength
    party_id_strength = np.abs(party_id_7pt) / 3.0  # 0 to 1
    affective_polarization = np.clip(
        rng.beta(2, 5, n_voters) + 0.3 * party_id_strength,
        0, 1
    )
    
    # Economic perception type (0-1): 0 = pocketbook, 1 = sociotropic
    # Higher education correlates with more sociotropic (national) evaluation
    economic_perception = np.clip(
        rng.beta(2, 3, n_voters) + 0.15 * (education / 4),
        0, 1
    )
    
    # Turnout influenced by education, age, and political knowledge
    base_turnout = rng.beta(5, 2, n_voters)
    turnout_prob = np.clip(
        base_turnout + 0.02 * education + 0.002 * np.minimum(age - 18, 50) + 0.002 * (political_knowledge / 100),
        0.1, 0.95
    )
    
    return pl.DataFrame({
        # Demographics
        "constituency": rng.integers(0, n_constituencies, size=n_voters),
        "age": age,
        "gender": gender,
        "education": education,
        "income": income.astype(np.float64),
        "religion": religion,
        # Political identity
        "party_id_7pt": party_id_7pt,  # -3 to +3 scale
        "ideology_x": ideology_x,
        "ideology_y": ideology_y,
        # Knowledge & Behavior
        "political_knowledge": political_knowledge.astype(np.float64),
        "misinfo_susceptibility": misinfo_susceptibility.astype(np.float64),
        "affective_polarization": affective_polarization.astype(np.float64),
        "economic_perception": economic_perception.astype(np.float64),
        "turnout_prob": turnout_prob,
    })


def generate_party_frame(
    parties: list[dict],
    include_nota: bool = False,
) -> pl.DataFrame:
    """
    Generate party DataFrame from configuration.
    
    Args:
        parties: List of party configuration dicts
        include_nota: Whether to add NOTA (None of the Above) option
        
    Returns:
        Polars DataFrame with party attributes
    """
    party_data = [
        {
            "name": p.get("name", f"Party {i}"),
            "position_x": float(p.get("position_x", 0.0)),
            "position_y": float(p.get("position_y", 0.0)),
            "valence": float(p.get("valence", 50.0)),
            "incumbent": bool(p.get("incumbent", False)),
            "is_nota": False
        }
        for i, p in enumerate(parties)
    ]
    
    # Add NOTA if requested
    if include_nota:
        party_data.append({
            "name": "NOTA",
            "position_x": 0.0,
            "position_y": 0.0,
            "valence": 0.0,  # No appeal
            "incumbent": False,
            "is_nota": True,
        })
    
    return pl.DataFrame(party_data)
