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

    ideology_x = np.clip(base_ideology_x + 0.005 * (income - 50) + 0.003 * (age - 50), -1, 1)
    ideology_y = np.clip(base_ideology_y - 0.02 * (education - 2) + 0.005 * (age - 50), -1, 1)

    # Political knowledge (0-100) - Beta distribution
    # Higher knowledge correlates with higher turnout
    political_knowledge = rng.beta(2, 5, n_voters) * 100

    # Misinformation susceptibility (0-1) - inversely related to education and knowledge
    # Higher susceptibility = more easily influenced by false information
    misinfo_susceptibility = np.clip(
        rng.beta(2, 3, n_voters) - 0.1 * (education / 4) - 0.1 * (political_knowledge / 100),
        0.05,
        0.95,
    )

    # Affective polarization (0-1) - in-group/out-group favorability gap
    # 0 = neutral toward all parties, 1 = highly polarized (loves own party, hates others)
    # Right-skewed: most voters are moderate, fewer are highly polarized
    # Correlates positively with party_id strength
    party_id_strength = np.abs(party_id_7pt) / 3.0  # 0 to 1
    affective_polarization = np.clip(rng.beta(2, 5, n_voters) + 0.3 * party_id_strength, 0, 1)

    # Economic perception type (0-1): 0 = pocketbook, 1 = sociotropic
    # Higher education correlates with more sociotropic (national) evaluation
    economic_perception = np.clip(rng.beta(2, 3, n_voters) + 0.15 * (education / 4), 0, 1)

    # =========================================================================
    # BIG FIVE PERSONALITY (OCEAN) - 0 to 1 scale
    # =========================================================================
    # Research shows personality correlates with political orientation:
    # - Openness: positively correlates with liberal/left views
    # - Conscientiousness: positively correlates with conservative/right views
    # - Extraversion: higher political engagement
    # - Agreeableness: moderate views, conflict avoidance
    # - Neuroticism: anxiety, can increase political engagement or withdrawal

    # Openness to Experience (O)
    # Higher O → more liberal, open to change, diversity
    openness = np.clip(rng.beta(5, 5, n_voters), 0, 1)

    # Conscientiousness (C)
    # Higher C → more conservative, orderly, traditional
    conscientiousness = np.clip(rng.beta(5, 5, n_voters), 0, 1)

    # Extraversion (E)
    # Higher E → more political participation
    extraversion = np.clip(rng.beta(5, 5, n_voters), 0, 1)

    # Agreeableness (A)
    # Higher A → more moderate, cooperative
    agreeableness = np.clip(rng.beta(5, 5, n_voters), 0, 1)

    # Neuroticism (N)
    # Higher N → more anxiety-driven political behavior
    neuroticism = np.clip(
        rng.beta(4, 6, n_voters), 0, 1
    )  # Slightly right-skewed (most people moderate)

    # Adjust ideology based on personality (research-based correlations)
    # Openness → liberal (negative x), Conscientiousness → conservative (positive x)
    personality_ideology_shift = 0.15 * (conscientiousness - openness)
    ideology_x = np.clip(ideology_x + personality_ideology_shift, -1, 1)

    # =========================================================================
    # MORAL FOUNDATIONS (Haidt) - 0 to 1 scale
    # =========================================================================
    # 5 foundations that vary by political orientation:
    # Liberals: Care, Fairness (individualizing foundations)
    # Conservatives: Loyalty, Authority, Sanctity (binding foundations)

    # Care/Harm: sensitivity to suffering, empathy
    # Liberals score higher on average
    mf_care = np.clip(
        rng.beta(6, 4, n_voters) - 0.1 * (ideology_x + 1) / 2, 0, 1  # Higher for liberals
    )

    # Fairness/Cheating: justice, equality, proportionality
    # Both sides value but interpret differently
    mf_fairness = np.clip(rng.beta(6, 4, n_voters), 0, 1)

    # Loyalty/Betrayal: in-group loyalty, patriotism
    # Conservatives score higher
    mf_loyalty = np.clip(
        rng.beta(5, 5, n_voters) + 0.15 * (ideology_x + 1) / 2, 0, 1  # Higher for conservatives
    )

    # Authority/Subversion: respect for hierarchy, tradition
    # Conservatives score higher
    mf_authority = np.clip(
        rng.beta(5, 5, n_voters) + 0.15 * (ideology_x + 1) / 2, 0, 1  # Higher for conservatives
    )

    # Sanctity/Degradation: purity, disgust sensitivity
    # Conservatives score higher
    mf_sanctity = np.clip(
        rng.beta(4, 5, n_voters) + 0.2 * (ideology_x + 1) / 2, 0, 1  # Higher for conservatives
    )

    # =========================================================================
    # MEDIA DIET - Selective Exposure
    # =========================================================================
    # Voters tend to consume media that aligns with their existing views (echo chamber).
    # Define 4 generic media sources:
    # 0: Left-leaning (-0.5)
    # 1: Centrist (0.0)
    # 2: Right-leaning (0.5)
    # 3: Alternative/Extreme (skewed based on sub-population, usually anti-establishment)

    # Calculate distance to each source
    dist_left = np.abs(ideology_x - (-0.5))
    dist_center = np.abs(ideology_x - 0.0)
    dist_right = np.abs(ideology_x - 0.5)

    # Assign primary source based on proximity (probabilistic to allow some cross-cutting)
    # We use a simple argmin for the primary source, but add noise
    media_noise = rng.normal(0, 0.2, n_voters)
    noisy_x = ideology_x + media_noise

    # 0=Left, 1=Center, 2=Right
    media_choice_idx = np.zeros(n_voters, dtype=int)

    # Vectorized assignment
    conditions = [(noisy_x < -0.25), (noisy_x >= -0.25) & (noisy_x <= 0.25), (noisy_x > 0.25)]
    choices = [0, 1, 2]
    media_choice_idx = np.select(conditions, choices)

    # Assign bias values
    media_bias_values = np.zeros(n_voters)
    media_bias_values[media_choice_idx == 0] = -0.5
    media_bias_values[media_choice_idx == 1] = 0.0
    media_bias_values[media_choice_idx == 2] = 0.5

    # Turnout influenced by education, age, political knowledge, and extraversion
    base_turnout = rng.beta(5, 2, n_voters)
    turnout_prob = np.clip(
        base_turnout
        + 0.02 * education
        + 0.002 * np.minimum(age - 18, 50)
        + 0.002 * (political_knowledge / 100)
        + 0.05 * extraversion  # Extraverts more likely to participate
        - 0.03 * neuroticism,  # High neuroticism can reduce turnout
        0.1,
        0.95,
    )

    return pl.DataFrame(
        {
            # Demographics
            "constituency": rng.integers(0, n_constituencies, size=n_voters).astype(np.int32),
            "age": age.astype(np.int8),
            "gender": gender.astype(np.int8),
            "education": education.astype(np.int8),
            "income": income.astype(np.float32),
            "religion": religion.astype(np.int8),
            # Political identity
            "party_id_7pt": party_id_7pt.astype(np.int8),  # -3 to +3 scale
            "ideology_x": ideology_x.astype(np.float32),
            "ideology_y": ideology_y.astype(np.float32),
            # Big Five (OCEAN)
            "openness": openness.astype(np.float32),
            "conscientiousness": conscientiousness.astype(np.float32),
            "extraversion": extraversion.astype(np.float32),
            "agreeableness": agreeableness.astype(np.float32),
            "neuroticism": neuroticism.astype(np.float32),
            # Moral Foundations
            "mf_care": mf_care.astype(np.float32),
            "mf_fairness": mf_fairness.astype(np.float32),
            "mf_loyalty": mf_loyalty.astype(np.float32),
            "mf_authority": mf_authority.astype(np.float32),
            "mf_sanctity": mf_sanctity.astype(np.float32),
            # Media Diet
            "media_source_id": media_choice_idx.astype(np.int8),
            "media_bias": media_bias_values.astype(np.float32),
            # Knowledge & Behavior
            "political_knowledge": political_knowledge.astype(np.float32),
            "misinfo_susceptibility": misinfo_susceptibility.astype(np.float32),
            "affective_polarization": affective_polarization.astype(np.float32),
            "economic_perception": economic_perception.astype(np.float32),
            "turnout_prob": turnout_prob.astype(np.float32),
        }
    )


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
            "is_nota": False,
        }
        for i, p in enumerate(parties)
    ]

    # Add NOTA if requested
    if include_nota:
        party_data.append(
            {
                "name": "NOTA",
                "position_x": 0.0,
                "position_y": 0.0,
                "valence": 0.0,  # No appeal
                "incumbent": False,
                "is_nota": True,
            }
        )

    return pl.DataFrame(party_data)
