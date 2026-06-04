"""
Campaign Finance Model for ElectoralSim.

Models spending, fundraising, ad saturation, diminishing returns,
incumbency fundraising advantage, and district targeting effects.
Campaign effects connect to valence/media exposure rather than
direct vote overrides.
"""

import numpy as np


class CampaignFinance:
    """
    Campaign finance model with spending-to-valence conversion.

    Models the effect of campaign spending on party valence with
    diminishing returns. Incumbents have a fundraising advantage.
    """

    def __init__(
        self,
        base_spending: float = 1_000_000.0,
        incumbent_advantage: float = 1.5,
        diminishing_factor: float = 0.5,
    ):
        """
        Args:
            base_spending: Base campaign spending per party (monetary units)
            incumbent_advantage: Multiplier for incumbent fundraising
            diminishing_factor: Diminishing returns exponent (<1 = steeper curve)
        """
        self.base_spending = base_spending
        self.incumbent_advantage = incumbent_advantage
        self.diminishing_factor = diminishing_factor

    def compute_spending(
        self,
        n_parties: int,
        incumbents: np.ndarray | None = None,
        rng: np.random.Generator | None = None,
    ) -> np.ndarray:
        """
        Compute campaign spending per party.

        Args:
            n_parties: Number of parties
            incumbents: Boolean array indicating incumbent parties
            rng: Random generator for spending variation

        Returns:
            Array of spending per party
        """
        if rng is None:
            rng = np.random.default_rng()

        spending = np.full(n_parties, self.base_spending, dtype=float)

        if incumbents is not None:
            spending[incumbents] *= self.incumbent_advantage

        spending *= rng.uniform(0.8, 1.2, n_parties)
        return spending

    def spending_to_valence(
        self,
        spending: np.ndarray,
    ) -> np.ndarray:
        """
        Convert campaign spending to valence boost with diminishing returns.

        Args:
            spending: Per-party campaign spending

        Returns:
            Valence boost per party (additive to base valence)
        """
        return np.log1p(spending) ** self.diminishing_factor * 5.0

    def district_targeting(
        self,
        spending: np.ndarray,
        n_districts: int,
        marginal_seats: np.ndarray | None = None,
    ) -> np.ndarray:
        """
        Allocate campaign spending across districts.

        Parties allocate more resources to marginal (competitive) districts.

        Args:
            spending: Per-party total spending
            n_districts: Number of districts
            marginal_seats: (n_parties, n_districts) marginality scores (0-1)

        Returns:
            (n_parties, n_districts) spending allocation matrix
        """
        n_parties = len(spending)
        if marginal_seats is None:
            allocation = np.ones((n_parties, n_districts)) / n_districts
        else:
            allocation = marginal_seats / (marginal_seats.sum(axis=1, keepdims=True) + 1e-10)

        return spending[:, np.newaxis] * allocation


class MediaEnvironment:
    """
    Media environment model: tracks party exposure, sentiment, reach,
    and misinformation susceptibility with time decay.
    """

    def __init__(
        self,
        base_exposure: float = 0.5,
        sentiment_bias: float = 0.0,
        reach_decay: float = 0.95,
    ):
        """
        Args:
            base_exposure: Base media exposure level (0-1)
            sentiment_bias: Media sentiment bias (-1=anti-incumbent, +1=pro-incumbent)
            reach_decay: Time-decay factor for past media effects (<1 = fading)
        """
        self.base_exposure = base_exposure
        self.sentiment_bias = sentiment_bias
        self.reach_decay = reach_decay
        self.history: list[dict] = []

    def step(
        self,
        n_parties: int,
        incumbents: np.ndarray | None = None,
        rng: np.random.Generator | None = None,
    ) -> dict:
        """
        Advance one media cycle, generating new exposure and sentiment data.

        Returns dict with exposure, sentiment, and reach per party.
        """
        if rng is None:
            rng = np.random.default_rng()

        exposure = np.full(n_parties, self.base_exposure, dtype=float)
        sentiment = np.full(n_parties, self.sentiment_bias, dtype=float)

        if incumbents is not None:
            sentiment[incumbents] += 0.1  # Slight incumbency attention

        # Simulate media coverage randomness
        exposure *= rng.uniform(0.7, 1.3, n_parties)
        sentiment += rng.uniform(-0.1, 0.1, n_parties)

        # Apply time decay to previous history
        decayed_reach = 1.0
        for past in self.history:
            decayed_reach *= self.reach_decay

        result = {
            "exposure": exposure,
            "sentiment": sentiment,
            "reach": decayed_reach,
        }
        self.history.append(result)
        return result

    def misinformation_susceptibility(
        self,
        media_diet: np.ndarray | None = None,
    ) -> float:
        """
        Estimate population-level susceptibility to misinformation.

        Lower media diet diversity → higher susceptibility.

        Args:
            media_diet: (n_voters,) media diet quality scores (0-1)

        Returns:
            Misinformation susceptibility (0-1)
        """
        if media_diet is None:
            return 0.3  # Default moderate susceptibility
        return float(1.0 - np.mean(media_diet))


class VoterRegistration:
    """
    Voter registration and eligibility model.

    Models eligible population, registration status, turnout probability,
    age/citizenship constraints, and registration deadlines.
    """

    def __init__(
        self,
        eligible_rate: float = 0.85,
        registration_rate: float = 0.75,
        base_turnout: float = 0.65,
        age_effect: float = 0.1,
    ):
        """
        Args:
            eligible_rate: Proportion of population eligible to vote
            registration_rate: Proportion of eligible who register
            base_turnout: Base turnout probability among registered voters
            age_effect: Additional turnout probability change per decade from median
        """
        self.eligible_rate = eligible_rate
        self.registration_rate = registration_rate
        self.base_turnout = base_turnout
        self.age_effect = age_effect

    def compute_eligibility(
        self,
        n_voters: int,
        age: np.ndarray | None = None,
        rng: np.random.Generator | None = None,
    ) -> dict[str, np.ndarray]:
        """
        Compute eligible population, registered voters, and likely voters.

        Args:
            n_voters: Total population
            age: (n_voters,) voter ages (used for turnout modulation)
            rng: Random generator

        Returns:
            Dict with 'eligible', 'registered', 'will_vote' boolean arrays
        """
        if rng is None:
            rng = np.random.default_rng()

        eligible = rng.random(n_voters) < self.eligible_rate
        registered = eligible & (rng.random(n_voters) < self.registration_rate)

        turnout_prob = np.full(n_voters, self.base_turnout)
        if age is not None:
            age_norm = (age - np.median(age)) / 10.0
            turnout_prob += self.age_effect * age_norm
        turnout_prob = np.clip(turnout_prob, 0.0, 1.0)

        will_vote = registered & (rng.random(n_voters) < turnout_prob)

        return {
            "eligible": eligible,
            "registered": registered,
            "will_vote": will_vote,
        }


class CampaignTargeting:
    """
    Local campaign targeting: parties allocate resources across
    constituencies based on marginal-seat value with budget constraints
    and diminishing returns on persuasion.
    """

    def __init__(
        self,
        total_budget: float = 100.0,
        marginal_weight: float = 0.7,
        persuasion_decay: float = 0.5,
    ):
        """
        Args:
            total_budget: Total campaign resources per party
            marginal_weight: Weight given to marginal (competitive) districts
            persuasion_decay: Diminishing returns on additional spending
        """
        self.total_budget = total_budget
        self.marginal_weight = marginal_weight
        self.persuasion_decay = persuasion_decay

    def allocate_resources(
        self,
        marginality: np.ndarray,
    ) -> np.ndarray:
        """
        Allocate campaign resources across districts proportional to marginality.

        Args:
            marginality: (n_districts,) marginality scores (0-1, higher=more competitive)

        Returns:
            (n_districts,) resource allocation per district
        """
        weights = self.marginal_weight * marginality + (1 - self.marginal_weight) * 0.5
        weights = weights / weights.sum()
        return self.total_budget * weights

    def persuasion_effect(
        self,
        spending: np.ndarray,
    ) -> np.ndarray:
        """
        Convert campaign spending to persuasion (vote-share swing) with diminishing returns.

        Args:
            spending: Per-district spending

        Returns:
            (n_districts,) persuasion effect (vote share change)
        """
        return (spending ** self.persuasion_decay) * 0.01
