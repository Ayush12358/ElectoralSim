"""
India General Election Simulator

Simulates Lok Sabha elections with:
- 543 constituencies across 36 states/UTs
- 19 national and regional parties
- State-wise party strength weights
- State-specific ideology distributions
- Uses Numba-accelerated FPTP counting engine

The state-by-state approach is necessary because each state has different
regional parties, different local weights, and different ideological leanings.
This is inherently a batch of independent state elections.
"""

import time
from dataclasses import dataclass, field

import numpy as np
import polars as pl

from electoral_sim.behavior.voter_behavior import (
    BehaviorEngine,
    ProximityModel,
    ValenceModel,
)
from electoral_sim.core.voter_generation import generate_voter_frame
from electoral_sim.engine.numba_accel import fptp_count_fast, vote_mnl_fast
from electoral_sim.metrics.indices import effective_number_of_parties, gallagher_index
from electoral_sim.presets.india.data import (
    DEFAULT_WEIGHTS,
    INDIA_BLOC_PARTIES,
    INDIA_ELECTION_PHASES,
    INDIA_PARTIES,
    INDIA_STATES,
    NDA_PARTIES,
    STATE_IDEOLOGY_SHIFTS,
    STATE_PARTY_WEIGHTS,
)


def get_phase_states() -> dict[int, list[str]]:
    """Get states voting in each phase."""
    return INDIA_ELECTION_PHASES.copy()


@dataclass
class IndiaElectionResult:
    """Results of India general election simulation."""

    seats: dict[str, int]
    vote_shares: dict[str, float]
    state_results: dict[str, dict]
    turnout: float
    gallagher_index: float
    enp_votes: float
    enp_seats: float
    nda_seats: int
    india_seats: int
    others_seats: int
    nota_contested_seats: int = 0
    nota_contested_list: list[str] = field(default_factory=list)
    voter_df: pl.DataFrame | None = None
    party_positions: np.ndarray | None = None

    def __str__(self):
        lines = ["=" * 60]
        lines.append("INDIA GENERAL ELECTION RESULTS")
        lines.append("=" * 60)
        lines.append(f"\nTurnout: {self.turnout:.1%}")
        lines.append(f"Gallagher Index: {self.gallagher_index:.2f}")
        lines.append(f"ENP (votes): {self.enp_votes:.2f}")
        lines.append(f"ENP (seats): {self.enp_seats:.2f}")
        lines.append(f"\n{'Party':15} {'Seats':>8} {'Vote %':>8}")
        lines.append("-" * 35)

        sorted_parties = sorted(self.seats.items(), key=lambda x: -x[1])
        for party, seats in sorted_parties:
            if seats > 0:
                vote_pct = self.vote_shares.get(party, 0) * 100
                lines.append(f"{party:15} {seats:>8} {vote_pct:>7.1f}%")

        lines.append("\n" + "-" * 35)
        lines.append(f"{'NDA Total':15} {self.nda_seats:>8}")
        lines.append(f"{'INDIA Total':15} {self.india_seats:>8}")
        lines.append(f"{'Others Total':15} {self.others_seats:>8}")
        lines.append("-" * 35)
        lines.append(f"{'TOTAL':15} {sum(self.seats.values()):>8}")
        lines.append("\nMajority mark: 272")

        if self.nda_seats >= 272:
            lines.append("🏆 NDA wins majority!")
        elif self.india_seats >= 272:
            lines.append("🏆 INDIA bloc wins majority!")
        else:
            lines.append("⚖️ Hung Parliament - Coalition needed")

        if self.nota_contested_seats > 0:
            lines.append(f"\n⚠️ NOTA contested races: {self.nota_contested_seats}")

        return "\n".join(lines)


def generate_state_voter_frame(
    n_voters_per_constituency: int,
    n_constituencies: int,
    state: str,
    rng: np.random.Generator,
) -> pl.DataFrame:
    """
    Generate a voter DataFrame for a single state with state-specific ideology shifts.
    """
    n_voters = n_voters_per_constituency * n_constituencies
    df = generate_voter_frame(n_voters, n_constituencies, rng)

    shift = STATE_IDEOLOGY_SHIFTS.get(state, (0.0, 0.0))
    if shift != (0.0, 0.0):
        df = df.with_columns(
            [
                (pl.col("ideology_x") + shift[0]).clip(-1, 1).alias("ideology_x"),
                (pl.col("ideology_y") + shift[1]).clip(-1, 1).alias("ideology_y"),
            ]
        )

    return df


def compute_state_party_utilities(
    df: pl.DataFrame,
    party_names: list[str],
    state_weights: dict[str, float],
) -> np.ndarray:
    """
    Compute utility matrix for voters in a state using BehaviorEngine + state weights.

    Uses ProximityModel(-dist * 0.3) + ValenceModel(0.005 * val) via BehaviorEngine,
    with per-state party weight bonus on top.
    """
    n_voters = len(df)
    n_parties = len(party_names)

    # Build party positions and valence arrays for BehaviorEngine
    party_positions = np.zeros((n_parties, 2), dtype=np.float64)
    party_valence = np.zeros(n_parties, dtype=np.float64)
    for p, party in enumerate(party_names):
        pd_data = INDIA_PARTIES.get(party, {})
        party_positions[p, 0] = pd_data.get("position_x", 0.0)
        party_positions[p, 1] = pd_data.get("position_y", 0.0)
        party_valence[p] = pd_data.get("valence", 25)

    # Compute base utilities via BehaviorEngine
    voter_data = {
        "n_voters": n_voters,
        "positions": np.column_stack(
            [df["ideology_x"].to_numpy(), df["ideology_y"].to_numpy()]
        ),
    }
    party_data = {
        "n_parties": n_parties,
        "positions": party_positions,
        "valence": party_valence,
    }

    engine = BehaviorEngine()
    engine.add_model(ProximityModel(weight=0.3))
    engine.add_model(ValenceModel(weight=0.005))
    utilities = engine.compute_all(voter_data, party_data)

    # Add India-specific per-state party weight bonus
    for p, party in enumerate(party_names):
        weight = state_weights.get(party, 0.05)
        utilities[:, p] += weight * 3.0

    return utilities


def simulate_india_election(
    n_voters_per_constituency: int = 10000,
    seed: int | None = None,
    verbose: bool = True,
    include_nota: bool = False,
    use_real_names: bool = True,
    historical_data_path: str | None = None,
) -> IndiaElectionResult:
    """
    Simulate India General Election.

    Each state is simulated independently with its own voter distribution,
    party weights, and constituency assignments, using Numba-accelerated
    MNL voting and FPTP counting.

    Args:
        n_voters_per_constituency: Voters per constituency
        seed: Random seed
        verbose: Print progress
        include_nota: Include NOTA option
        use_real_names: Use real PC names
        historical_data_path: Path to CSV with previous results

    Returns:
        IndiaElectionResult with full results
    """
    from electoral_sim.data.india_pc import get_india_constituencies
    from electoral_sim.data.loaders import HistoricalDataLoader

    manager = get_india_constituencies() if use_real_names else None

    viability_seeding = None
    incumbent_parties = set()
    if historical_data_path:
        loader = HistoricalDataLoader(historical_data_path)
        viability_seeding = loader.get_viability_weights()
        incumbent_parties = set(loader.get_incumbents())
        if verbose:
            print(f"  Seeded with historical data from {historical_data_path}")

    rng = np.random.default_rng(seed)

    party_names = list(INDIA_PARTIES.keys())
    party_list = [
        {
            "name": name,
            "position_x": data["position_x"],
            "position_y": data["position_y"],
            "valence": data["valence"],
            "incumbent": name in incumbent_parties,
        }
        for name, data in INDIA_PARTIES.items()
    ]

    if include_nota:
        party_names.append("NOTA")
        party_list.append(
            {
                "name": "NOTA",
                "position_x": 0.0,
                "position_y": 0.0,
                "valence": 15,
                "incumbent": False,
            }
        )

    n_parties = len(party_names)

    all_seats = dict.fromkeys(party_names, 0)
    all_votes = dict.fromkeys(party_names, 0)
    state_results = {}
    total_voters = 0
    total_voted = 0
    nota_contested_seats = 0
    nota_contested_list = []

    start_time = time.perf_counter()
    global_const_id = 0
    voter_df_sample = None

    for state, n_constituencies in INDIA_STATES.items():
        if verbose:
            print(f"  Simulating {state} ({n_constituencies} seats)...", end=" ", flush=True)

        state_start = time.perf_counter()
        state_weights = STATE_PARTY_WEIGHTS.get(state, DEFAULT_WEIGHTS)

        voter_df = generate_state_voter_frame(
            n_voters_per_constituency,
            n_constituencies,
            state,
            rng,
        )
        n_voters = len(voter_df)
        total_voters += n_voters

        utilities = compute_state_party_utilities(voter_df, party_names, state_weights)

        votes = vote_mnl_fast(utilities, temperature=0.5, rng=rng)

        turnout_prob = voter_df["turnout_prob"].to_numpy()
        will_vote = rng.random(n_voters) < turnout_prob
        voted_count = will_vote.sum()
        total_voted += voted_count

        constituencies = voter_df["constituency"].to_numpy()
        voted_constituencies = constituencies[will_vote]
        voted_choices = votes[will_vote]

        seats_array, vote_counts_array = fptp_count_fast(
            voted_constituencies.astype(np.int64),
            voted_choices.astype(np.int64),
            n_constituencies,
            n_parties,
        )

        state_seats = {party_names[i]: int(seats_array[i]) for i in range(n_parties)}
        state_votes = {party_names[i]: int(vote_counts_array[i]) for i in range(n_parties)}

        if include_nota and "NOTA" in party_names:
            nota_idx = party_names.index("NOTA")
            for c in range(n_constituencies):
                c_mask = voted_constituencies == c
                c_votes = voted_choices[c_mask]
                if len(c_votes) == 0:
                    continue
                vc = np.bincount(c_votes, minlength=n_parties)
                if vc[nota_idx] > 0 and party_names[np.argmax(vc)] != "NOTA":
                    sorted_c = np.sort(vc)[::-1]
                    margin = sorted_c[0] - sorted_c[1]
                    if vc[nota_idx] > margin:
                        nota_contested_seats += 1
                        c_name = (
                            manager.get_name(global_const_id + c)
                            if manager
                            else f"Constituency {c+1}"
                        )
                        nota_contested_list.append(f"{state}: {c_name}")

        for party in party_names:
            all_seats[party] += state_seats[party]
            all_votes[party] += state_votes[party]

        state_results[state] = {
            "seats": state_seats,
            "votes": state_votes,
            "turnout": voted_count / n_voters,
        }

        state_time = time.perf_counter() - state_start
        if verbose:
            top_party = max(state_seats.items(), key=lambda x: x[1])
            print(f"done ({state_time*1000:.0f}ms) - {top_party[0]}: {top_party[1]} seats")

        state_voter_df = pl.DataFrame(
            {
                "ideology_x": voter_df["ideology_x"],
                "ideology_y": voter_df["ideology_y"],
                "vote": [party_names[v] for v in votes],
                "state": state,
            }
        )
        state_sample = state_voter_df.sample(min(100, len(state_voter_df)), seed=seed)
        voter_df_sample = (
            state_sample if voter_df_sample is None else pl.concat([voter_df_sample, state_sample])
        )

        global_const_id += n_constituencies

    total_votes = sum(all_votes.values())
    vote_shares = {p: v / total_votes for p, v in all_votes.items()}

    vote_array = np.array(list(vote_shares.values()))
    seat_array = np.array(list({p: s / 543 for p, s in all_seats.items()}.values()))

    gal_idx = gallagher_index(vote_array, seat_array)
    enp_v = effective_number_of_parties(vote_array)
    enp_s = effective_number_of_parties(seat_array)

    nda_seats = sum(all_seats.get(p, 0) for p in NDA_PARTIES)
    india_seats = sum(all_seats.get(p, 0) for p in INDIA_BLOC_PARTIES)
    others_seats = 543 - nda_seats - india_seats

    elapsed = time.perf_counter() - start_time

    if verbose:
        print(f"\nTotal simulation time: {elapsed:.2f}s")

    party_pos = np.array([[p["position_x"], p["position_y"]] for p in INDIA_PARTIES.values()])

    return IndiaElectionResult(
        seats=all_seats,
        vote_shares=vote_shares,
        state_results=state_results,
        turnout=total_voted / total_voters,
        gallagher_index=gal_idx,
        enp_votes=enp_v,
        enp_seats=enp_s,
        nda_seats=nda_seats,
        india_seats=india_seats,
        others_seats=others_seats,
        nota_contested_seats=nota_contested_seats,
        nota_contested_list=nota_contested_list,
        voter_df=voter_df_sample,
        party_positions=party_pos,
    )
