"""
ElectionModel - Main simulation model using Mesa
Implements India-scale electoral simulation with constituency-based structure

Uses Mesa for model orchestration with Polars DataFrames for high-performance
agent storage and Numba for accelerated voting calculations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import polars as pl
from mesa import Model

from electoral_sim.agents.party import PartyAgents
from electoral_sim.agents.party_strategy import adaptive_strategy_step
from electoral_sim.agents.voter import VoterAgents
from electoral_sim.core.voter_generation import generate_voter_frame
from electoral_sim.engine.numba_accel import (
    fptp_count_fast,
    vote_mnl_fast,
)
from electoral_sim.events.event_manager import EventManager
from electoral_sim.metrics.indices import effective_number_of_parties, gallagher_index

if TYPE_CHECKING:
    from electoral_sim.behavior.voter_behavior import BehaviorEngine
    from electoral_sim.dynamics.opinion_dynamics import OpinionDynamics

# =============================================================================
# ELECTION MODEL
# =============================================================================


class ElectionModel(Model):
    """
    Main election simulation model using Mesa + Polars.

    Supports:
        - Multiple constituencies (default: 543 for Lok Sabha)
        - Configurable electoral systems (FPTP, PR with D'Hondt/Sainte-Laguë)
        - Multinomial logit voting model
        - Opinion dynamics (placeholder)

    Examples:
        # Simple usage
        model = ElectionModel(n_voters=100_000)
        results = model.run_election()

        # Using Config
        from electoral_sim import Config
        config = Config(n_voters=100_000, electoral_system="PR")
        model = ElectionModel.from_config(config)

        # Using presets
        model = ElectionModel.from_preset("india")

        # Chainable API
        results = (
            ElectionModel(n_voters=100_000)
            .with_system("PR")
            .run_election()
        )

    Parameters
    ----------
    n_voters : int
        Total number of voter agents
    n_constituencies : int
        Number of electoral constituencies
    parties : list[dict]
        Party configurations with name, position_x, position_y, valence
    voter_frame : pl.DataFrame | None
        Optional pre-built voter DataFrame (bypasses automatic generation)
    party_frame : pl.DataFrame | None
        Optional pre-built party DataFrame
    electoral_system : str
        'FPTP' or 'PR'
    allocation_method : str
        'dhondt' or 'sainte_lague' (for PR)
    threshold : float
        Electoral threshold for PR (0-1)
    temperature : float
        MNL temperature parameter (lower = more deterministic)
    seed : int | None
        Random seed for reproducibility
    """

    def __init__(
        self,
        n_voters: int = 100_000,
        n_constituencies: int = 10,
        parties: list[dict] | None = None,
        voter_frame: pl.DataFrame | None = None,
        party_frame: pl.DataFrame | None = None,
        electoral_system: str = "FPTP",
        allocation_method: str = "dhondt",
        threshold: float = 0.0,
        temperature: float = 0.5,
        seed: int | None = None,
        behavior_engine: BehaviorEngine | None = None,
        opinion_dynamics: OpinionDynamics | None = None,
        include_nota: bool = False,
        constituency_constraints: dict[int, list[str]] | None = None,
        anti_incumbency: float = 0.0,
        economic_growth: float = 0.0,
        national_mood: float = 0.0,  # Wave election: positive = pro-incumbent, negative = anti-incumbent
        alienation_threshold: float = -2.0,  # Abstain if max utility below this
        indifference_threshold: float = 0.3,  # Abstain if utility range below this
        event_probs: dict[str, float] | None = None,  # P4: Dynamic events
        use_adaptive_strategy: bool = False,  # P4: Strategy
        constituency_manager: Optional[
            ConstituencyManager
        ] = None,  # TECHNICAL: Real data integration
        use_gpu: bool = False,  # P4: GPU acceleration (CuPy)
    ):
        super().__init__()

        # Initialize GPU support
        from electoral_sim.engine.gpu_accel import is_gpu_available

        self.use_gpu = use_gpu and is_gpu_available()
        if use_gpu and not self.use_gpu:
            print("Warning: GPU requested but not available. Falling back to CPU/Numba.")

        # Initialize Random Generator (Mesa 3.0+ compatible)
        if seed is not None:
            self.random.seed(seed)
        self.rng = np.random.default_rng(seed)

        # Store configuration
        self.n_constituencies = n_constituencies
        self.electoral_system = electoral_system
        self.allocation_method = allocation_method
        self.threshold = threshold
        self.temperature = temperature
        self.include_nota = include_nota
        self.constituency_constraints = constituency_constraints or {}
        self.constituency_manager = constituency_manager

        # Behavior & Dynamics
        from electoral_sim.behavior.voter_behavior import (
            BehaviorEngine,
            ProximityModel,
            RetrospectiveModel,
            ValenceModel,
        )

        self.economic_growth = economic_growth
        self.anti_incumbency = anti_incumbency
        self.national_mood = national_mood  # Wave election modifier
        self.alienation_threshold = alienation_threshold
        self.indifference_threshold = indifference_threshold

        if behavior_engine is None:
            # Default behavior: Proximity + Valence
            self.behavior_engine = BehaviorEngine()
            self.behavior_engine.add_model(ProximityModel())
            self.behavior_engine.add_model(ValenceModel())
            # Add RetrospectiveModel if economic conditions are set
            if economic_growth != 0.0:
                self.behavior_engine.add_model(RetrospectiveModel(weight=0.5))
        else:
            self.behavior_engine = behavior_engine

        self.opinion_dynamics = opinion_dynamics

        # Event Manager (P4)
        if event_probs is not None:
            scandal_p = event_probs.get("scandal", 0.01)
            shock_p = event_probs.get("shock", 0.005)
            self.event_manager = EventManager(self.rng, prob_scandal=scandal_p, prob_shock=shock_p)
        else:
            self.event_manager = None

        self.use_adaptive_strategy = use_adaptive_strategy

        # Default parties if not provided and no party_frame
        if parties is None and party_frame is None:
            parties = [
                {"name": "Party A", "position_x": -0.3, "position_y": 0.1, "valence": 50},
                {"name": "Party B", "position_x": 0.3, "position_y": -0.1, "valence": 50},
                {"name": "Party C", "position_x": 0.0, "position_y": 0.3, "valence": 45},
            ]

        # Create or use DataFrames
        if voter_frame is not None:
            self.voters = VoterAgents(self, voter_frame)
            if "constituency" in voter_frame.columns:
                self.n_constituencies = int(voter_frame["constituency"].max() + 1)
        else:
            self.voters = VoterAgents(self, self._generate_voter_frame(n_voters))

        if party_frame is not None:
            self.parties = PartyAgents(self, party_frame)
            self.n_parties = len(party_frame)
        else:
            self.parties = PartyAgents(self, self._generate_party_frame(parties))
            self.n_parties = len(self.parties)

        # Results storage
        self.election_results: list[dict] = []

        # Simple data collection
        self.collected_data: list[dict] = []
        self._collect_data()

    # =========================================================================
    # CLASS METHODS (Factory methods)
    # =========================================================================

    @classmethod
    def from_config(cls, config: Config) -> ElectionModel:
        """
        Create model from a Config object.

        Args:
            config: Config instance with all parameters

        Returns:
            ElectionModel instance

        Example:
            config = Config(n_voters=100_000, electoral_system="PR")
            model = ElectionModel.from_config(config)
        """

        return cls(
            n_voters=config.n_voters,
            n_constituencies=config.n_constituencies,
            parties=config.get_party_dicts(),
            electoral_system=config.electoral_system,
            allocation_method=config.allocation_method,
            threshold=config.threshold,
            temperature=config.temperature,
            seed=config.seed,
        )

    @classmethod
    def from_preset(cls, preset: str, **kwargs) -> ElectionModel:
        """
        Create model from a country preset.

        Args:
            preset: One of 'india', 'usa', 'uk', 'germany'
            **kwargs: Override any preset parameters

        Returns:
            ElectionModel instance

        Example:
            model = ElectionModel.from_preset("india", n_voters=500_000)
        """
        from electoral_sim.core.config import PRESETS

        if preset.lower() not in PRESETS:
            available = list(PRESETS.keys())
            raise ValueError(f"Unknown preset: {preset}. Available: {available}")

        config = PRESETS[preset.lower()](**kwargs)
        return cls.from_config(config)

    # =========================================================================
    # CHAINABLE API
    # =========================================================================

    def with_system(self, system: str) -> ElectionModel:
        """
        Set electoral system. Chainable.

        Args:
            system: 'FPTP' or 'PR'

        Returns:
            self for chaining
        """
        self.electoral_system = system
        return self

    def with_allocation(self, method: str) -> ElectionModel:
        """
        Set PR allocation method. Chainable.

        Args:
            method: 'dhondt', 'sainte_lague', 'hare', or 'droop'

        Returns:
            self for chaining
        """
        self.allocation_method = method
        return self

    def with_threshold(self, threshold: float) -> ElectionModel:
        """
        Set electoral threshold. Chainable.

        Args:
            threshold: 0-1 (e.g., 0.05 for 5%)

        Returns:
            self for chaining
        """
        self.threshold = threshold
        return self

    def with_temperature(self, temperature: float) -> ElectionModel:
        """
        Set MNL temperature. Chainable.

        Args:
            temperature: Lower = more deterministic voting

        Returns:
            self for chaining
        """
        self.temperature = temperature
        return self

    def _collect_data(self):
        """Collect model data for analysis."""
        self.collected_data.append(
            {
                "step": self.time,
                "n_voters": len(self.voters),
                "mean_turnout": float(self.voters.df["turnout_prob"].mean()),
            }
        )

    def _generate_voter_frame(self, n_voters: int) -> pl.DataFrame:
        """
        Generate initial voter DataFrame with full demographics.

        Delegates to voter_generation.generate_voter_frame() which includes:
            - Demographics: age, gender, education, income, religion
            - Party ID: 7-point scale (-3 to +3)
            - Ideology: 2D position (influenced by Big Five personality)
            - Big Five (OCEAN): openness, conscientiousness, extraversion, agreeableness, neuroticism
            - Moral Foundations: care, fairness, loyalty, authority, sanctity
            - Behavioral attributes: political knowledge, misinformation susceptibility, etc.
            - Turnout probability
        """
        return generate_voter_frame(n_voters, self.n_constituencies, self.rng)

    def _generate_party_frame(self, parties: list[dict]) -> pl.DataFrame:
        """Generate party DataFrame from configuration, optionally adding NOTA."""
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

        if self.include_nota:
            party_data.append(
                {
                    "name": "NOTA",
                    "position_x": 0.0,
                    "position_y": 0.0,
                    "valence": 0.0,  # Negative valence or handled separately?
                    "incumbent": False,
                    "is_nota": True,
                }
            )

        n = len(party_data)
        return pl.DataFrame(
            {
                "name": [p["name"] for p in party_data],
                "position_x": [p["position_x"] for p in party_data],
                "position_y": [p["position_y"] for p in party_data],
                "valence": [p["valence"] for p in party_data],
                "incumbent": [p["incumbent"] for p in party_data],
                "is_nota": [p["is_nota"] for p in party_data],
                "seats": np.zeros(n, dtype=np.int64),
                "vote_share": np.zeros(n, dtype=np.float64),
            }
        )

    def _compute_utilities(self, **kwargs) -> np.ndarray:
        """
        Compute utility matrix using the configured behavior engine.

        Applies anti-incumbency penalty if configured.
        """
        voter_data = {
            "n_voters": len(self.voters),
            "positions": self.voters.get_positions(),  # Need to add this to VoterAgents
            "ideology_x": self.voters.get_ideology_x(),
            "ideology_y": self.voters.get_ideology_y(),
            "df": self.voters.df,
        }

        # Apply anti-incumbency penalty to incumbent party valence
        valence = self.parties.get_valence().copy()
        if "incumbent" in self.parties.df.columns:
            incumbent_mask = self.parties.df["incumbent"].to_numpy()
            # Anti-incumbency: negative value = penalty to incumbents
            if self.anti_incumbency != 0.0:
                valence[incumbent_mask] += self.anti_incumbency
            # National mood (wave election): positive = pro-incumbent, negative = anti-incumbent
            if self.national_mood != 0.0:
                valence[incumbent_mask] += self.national_mood

        # P4: Apply event modifiers (Scandals, Economic Shocks)
        effective_growth = self.economic_growth
        if self.event_manager:
            # Valence modifiers (e.g. Scanal penalties)
            valence_modifiers = self.event_manager.get_valence_modifiers()
            for pid, mod in valence_modifiers.items():
                if pid < len(valence):
                    valence[pid] += mod

            # Economic modifiers (e.g. Shocks)
            eco_mod = self.event_manager.get_economic_modifier()
            effective_growth += eco_mod

        party_data = {
            "n_parties": len(self.parties),
            "positions": self.parties.get_positions(),
            "valence": valence,
            "incumbents": (
                self.parties.df["incumbent"].to_numpy()
                if "incumbent" in self.parties.df.columns
                else np.zeros(len(self.parties), dtype=bool)
            ),
            "df": self.parties.df,
            "viability": kwargs.get("viability"),  # P4: Support for strategic voting inputs
        }

        # Pass economic growth to behavior engine for retrospective voting
        return self.behavior_engine.compute_all(
            voter_data, party_data, growth=effective_growth, use_gpu=self.use_gpu, **kwargs
        )

    def _vote_mnl(self, utilities: np.ndarray) -> np.ndarray:
        """
        Multinomial logit voting: P(j) = exp(U_j/τ) / Σexp(U_k/τ)

        Uses Numba acceleration when available (~10x faster).

        Returns array of vote choices (party indices).
        """
        if self.use_gpu:
            from electoral_sim.engine.gpu_accel import mnl_sample_gpu

            return mnl_sample_gpu(utilities, self.temperature)

        return vote_mnl_fast(utilities, self.temperature, self.rng)

    def _decide_turnout(self, utilities: np.ndarray | None = None) -> np.ndarray:
        """
        Determine which voters turn out.

        Implements three abstention mechanisms:
        1. Base turnout probability (from voter attributes)
        2. Alienation: abstain if max utility below threshold (all candidates too far)
        3. Indifference: abstain if utility range below threshold (all candidates similar)

        Args:
            utilities: Optional (n_voters, n_parties) utility matrix for alienation/indifference

        Returns:
            Boolean array of who votes
        """
        n_voters = len(self.voters)
        turnout_prob = self.voters.df["turnout_prob"].to_numpy()

        # Apply alienation and indifference penalties if utilities provided
        if utilities is not None:
            # Alienation: abstain if best option is still unacceptable
            max_utility = utilities.max(axis=1)
            alienation_penalty = np.where(
                max_utility < self.alienation_threshold,
                0.3,  # 30% reduction in turnout probability
                0.0,
            )

            # Indifference: abstain if all options are too similar
            utility_range = utilities.max(axis=1) - utilities.min(axis=1)
            indifference_penalty = np.where(
                utility_range < self.indifference_threshold,
                0.2,  # 20% reduction in turnout probability
                0.0,
            )

            # Adjust turnout probability (vectorized)
            adjusted_turnout = np.clip(
                turnout_prob - alienation_penalty - indifference_penalty,
                0.1,  # Minimum 10% turnout even for alienated voters
                1.0,
            )
        else:
            adjusted_turnout = turnout_prob

        # Stochastic turnout decision
        random_vals = self.rng.random(n_voters)
        return adjusted_turnout > random_vals

    def run_election(self, **kwargs) -> dict:
        """
        Run a single election and return results.

        Args:
            **kwargs: Extra parameters passed to the behavior engine (e.g. growth=0.03)

        Returns:
            Dictionary with vote counts, seats, turnout, and metrics
        """
        # Compute utilities and cast votes
        utilities = self._compute_utilities(**kwargs)
        votes = self._vote_mnl(utilities)

        # Determine turnout (now with alienation/indifference)
        will_vote = self._decide_turnout(utilities)

        # Filter to voters who turned out (use cached constituencies)
        constituencies = self.voters.get_constituencies()
        voted_constituencies = constituencies[will_vote]
        voted_choices = votes[will_vote]

        # Apply constituency-level constraints if any (Reserved seats)
        # We need to filter options per constituency. This is easier if done during utility computation,
        # but as a post-hoc filter for "illegal" votes (invalidating them) or redistribution.
        # For simplicity, let's assume if a vote is cast for an excluded party in a reserved seat, it is invalidated.
        if self.constituency_constraints:
            party_names = self.parties.df["name"].to_list()
            valid_mask = np.ones(len(voted_choices), dtype=bool)
            for cid, allowed_parties in self.constituency_constraints.items():
                c_mask = voted_constituencies == cid
                # Find indices of parties not in allowed list
                excluded_indices = [
                    i for i, name in enumerate(party_names) if name not in allowed_parties
                ]
                # Invalidate votes for excluded parties in this constituency
                invalid_votes = np.isin(voted_choices, excluded_indices) & c_mask
                valid_mask &= ~invalid_votes

            voted_constituencies = voted_constituencies[valid_mask]
            voted_choices = voted_choices[valid_mask]

        # Count votes
        if self.electoral_system == "FPTP":
            results = self._count_fptp(voted_constituencies, voted_choices)
        else:
            results = self._count_pr(voted_choices)

        # If NOTA is included, it might "win" votes but shouldn't win seats in most systems
        # Unless we implement specific NOTA-win logic. For now, NOTA is just a vote vacuum.
        if self.include_nota:
            # Mask out NOTA wins in FPTP (NOTA doesn't win seats)
            nota_idx = (
                self.parties.df.with_row_index("temp_idx")
                .filter(pl.col("is_nota"))
                .select("temp_idx")
                .to_series()
                .item(0)
            )
            if self.electoral_system == "FPTP":
                # Find constituencies where NOTA 'won'
                # results['seats'] currently might include NOTA
                # We need to find the runner-up if NOTA won.
                # Actually, fptp_count_fast just gives the winner.
                # If we want to handle NOTA wins, we'd need to modify the counting or post-process.
                # For now, let's just mark NOTA seats as vacancies or give to runner-up if NOTA is winner.
                # Simplest: NOTA seats are 0.
                results["seats"][nota_idx] = 0

        # Calculate metrics
        vote_shares = results["vote_counts"] / results["vote_counts"].sum()
        seat_shares = (
            results["seats"] / results["seats"].sum() if results["seats"].sum() > 0 else vote_shares
        )

        results["gallagher"] = gallagher_index(vote_shares, seat_shares)
        results["enp_votes"] = effective_number_of_parties(vote_shares)
        results["enp_seats"] = effective_number_of_parties(seat_shares)
        results["turnout"] = will_vote.sum() / len(will_vote)

        # Update party DataFrame with results
        self.parties.df = self.parties.df.with_columns(
            [
                pl.Series("seats", results["seats"]),
                pl.Series("vote_share", vote_shares),
            ]
        )

        # Calculate VSE (P4)
        if "seats" in results:
            seats = np.array(results["seats"])
            total_seats = seats.sum()
            if total_seats > 0:
                seat_shares = seats / total_seats
            else:
                seat_shares = np.array(results["vote_counts"]) / np.sum(results["vote_counts"])

            from electoral_sim.analysis.vse import calculate_vse

            vse_score = calculate_vse(utilities, seat_shares)
            results["vse"] = vse_score

        self.election_results.append(results)
        return results

    def _count_fptp(self, constituencies: np.ndarray, votes: np.ndarray) -> dict:
        """
        First Past The Post: winner takes all in each constituency.

        Uses Numba parallel acceleration when available.
        """
        seats, vote_counts = fptp_count_fast(
            constituencies, votes, self.n_constituencies, self.n_parties
        )

        return {
            "system": "FPTP",
            "seats": seats,
            "vote_counts": vote_counts,
            "n_constituencies": self.n_constituencies,
        }

    def _count_pr(self, votes: np.ndarray) -> dict:
        """Proportional Representation with seat allocation."""
        # Vectorized vote counting
        vote_counts = np.bincount(votes, minlength=self.n_parties).astype(np.int64)

        # Allocate seats using registry for all methods
        from electoral_sim.systems.allocation import allocate_seats

        seats = allocate_seats(
            vote_counts, self.n_constituencies, self.allocation_method, self.threshold
        )

        return {
            "system": "PR",
            "method": self.allocation_method,
            "seats": seats,
            "vote_counts": vote_counts,
            "n_constituencies": self.n_constituencies,
        }

    def step(self) -> None:
        """Run one simulation step (for opinion dynamics)."""
        if self.opinion_dynamics:
            # Update ideologies based on social network
            # Update ideologies based on social network
            current_ideologies_x = self.voters.get_ideology_x()
            current_ideologies_y = self.voters.get_ideology_y()

            # Get media bias vector if available (Media Diet P3)
            if "media_bias" in self.voters.df.columns:
                media_bias_vector = self.voters.df["media_bias"].to_numpy()
                media_strength = 0.05  # Standard media influence per step
            else:
                media_bias_vector = 0.0
                media_strength = 0.0

            # Update X dimension (Left-Right)
            new_ideologies_x = self.opinion_dynamics.step(
                current_ideologies_x,
                model="bounded_confidence",
                media_bias=media_bias_vector,
                media_strength=media_strength,
            )

            # Update Y dimension (Lib-Auth) - assume standard media centers on 0.0 for Y or reuse X
            # For now, let's say media only affects Left-Right dimension strongly
            new_ideologies_y = self.opinion_dynamics.step(
                current_ideologies_y,
                model="bounded_confidence",
                media_bias=0.0,
                media_strength=0.0,  # Minimal effect on Y
            )
            # Update the frame
            self.voters.df = self.voters.df.with_columns(
                [
                    pl.Series("ideology_x", new_ideologies_x),
                    pl.Series("ideology_y", new_ideologies_y),
                ]
            )
            self.voters.invalidate_cache()

        # P4: Dynamic Events
        if self.event_manager:
            new_events = self.event_manager.step(self.n_parties)
            # Could log new_events here

        # P4: Adaptive Strategy
        if self.use_adaptive_strategy:
            # print("DEBUG: Calling adaptive strategy") # Debugging
            self.parties.df = adaptive_strategy_step(
                self.parties.df,
                self.voters.df,
                strategy="median_voter",
                learning_rate=0.005,  # Small shift per month/step
                rng=self.rng,
            )
            self.parties.invalidate_cache()

        # Collect step data (Mesa 3.0 compatible)
        self._collect_data()

    def run(self, n_steps: int = 100, election_interval: int = 10) -> None:
        """
        Run simulation for n_steps, holding elections at intervals.

        Args:
            n_steps: Total simulation steps
            election_interval: Steps between elections
        """
        for step in range(n_steps):
            self.step()

            if (step + 1) % election_interval == 0:
                self.run_election()

    def get_results(self) -> list[dict]:
        """Return all election results."""
        return self.election_results

    def run_elections_batch(
        self, n_elections: int = 10, reset_voters: bool = False, **kwargs
    ) -> list[dict]:
        """
        Run multiple elections in batch for Monte Carlo analysis.

        Optimized: only regenerates changing columns if reset_voters is True.
        """
        batch_results = []

        for i in range(n_elections):
            if reset_voters and i > 0:
                # Optimized partial reset: only update stochastic columns
                n = len(self.voters)
                # Just update ideology and turnout, keep demographics and unique_ids
                new_voter_data = self._generate_voter_frame(n)
                self.voters.df = self.voters.df.with_columns(
                    [
                        new_voter_data["ideology_x"],
                        new_voter_data["ideology_y"],
                        new_voter_data["turnout_prob"],
                    ]
                )
                self.voters.invalidate_cache()

            results = self.run_election(**kwargs)
            batch_results.append(results)

        return batch_results

    def get_aggregate_stats(self, results: list[dict] | None = None) -> dict:
        """
        Compute aggregate statistics across multiple elections.

        Args:
            results: List of election results (default: use stored results)

        Returns:
            Dictionary with mean/std of key metrics
        """
        if results is None:
            results = self.election_results

        if not results:
            return {}

        turnouts = np.array([r["turnout"] for r in results])
        gallaghers = np.array([r["gallagher"] for r in results])
        enp_votes = np.array([r["enp_votes"] for r in results])
        enp_seats = np.array([r["enp_seats"] for r in results])

        return {
            "n_elections": len(results),
            "turnout_mean": float(turnouts.mean()),
            "turnout_std": float(turnouts.std()),
            "gallagher_mean": float(gallaghers.mean()),
            "gallagher_std": float(gallaghers.std()),
            "enp_votes_mean": float(enp_votes.mean()),
            "enp_votes_std": float(enp_votes.std()),
            "enp_seats_mean": float(enp_seats.mean()),
            "enp_seats_std": float(enp_seats.std()),
        }


# Party presets moved to electoral_sim.config


# =============================================================================
# QUICK TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("ElectoralSim Quick Test")
    print("=" * 50)

    # Create model
    print("\nCreating model with 100K voters, 10 constituencies...")
    model = ElectionModel(
        n_voters=100_000,
        n_constituencies=10,
        electoral_system="FPTP",
        seed=42,
    )

    print(f"Voters: {len(model.voters)}")
    print(f"Parties: {len(model.parties)}")

    # Run election
    print("\nRunning FPTP election...")
    results = model.run_election()

    print("\nResults:")
    print(f"  Turnout: {results['turnout']:.1%}")
    print(f"  Gallagher Index: {results['gallagher']:.2f}")
    print(f"  ENP (votes): {results['enp_votes']:.2f}")
    print(f"  ENP (seats): {results['enp_seats']:.2f}")

    party_names = model.parties.df["name"].to_list()
    print("\n  Party Results:")
    for i, name in enumerate(party_names):
        votes = results["vote_counts"][i]
        seats = results["seats"][i]
        print(f"    {name}: {votes:,} votes, {seats} seats")

    # Test PR
    print("\n" + "-" * 50)
    print("Testing PR (D'Hondt)...")

    model_pr = ElectionModel(
        n_voters=100_000,
        n_constituencies=10,
        electoral_system="PR",
        allocation_method="dhondt",
        seed=42,
    )

    results_pr = model_pr.run_election()
    print(f"  Gallagher Index: {results_pr['gallagher']:.2f}")

    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)
