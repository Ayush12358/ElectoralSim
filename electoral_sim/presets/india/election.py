"""
India General Election Simulator

Simulates Lok Sabha elections with:
- 543 constituencies
- Realistic party configurations
- Regional party strongholds
- State-wise vote patterns
"""

import time
from dataclasses import dataclass, field

import numpy as np
import polars as pl

# =============================================================================
# INDIA ELECTION DATA
# =============================================================================

# States and their Lok Sabha seats
INDIA_STATES = {
    # Large states
    "Uttar Pradesh": 80,
    "Maharashtra": 48,
    "West Bengal": 42,
    "Bihar": 40,
    "Tamil Nadu": 39,
    "Madhya Pradesh": 29,
    "Karnataka": 28,
    "Gujarat": 26,
    "Rajasthan": 25,
    "Andhra Pradesh": 25,
    "Odisha": 21,
    "Kerala": 20,
    "Telangana": 17,
    "Jharkhand": 14,
    "Assam": 14,
    "Punjab": 13,
    "Chhattisgarh": 11,
    "Haryana": 10,
    "Delhi": 7,
    # Smaller states and UTs
    "Jammu & Kashmir": 5,
    "Uttarakhand": 5,
    "Himachal Pradesh": 4,
    "Tripura": 2,
    "Meghalaya": 2,
    "Manipur": 2,
    "Nagaland": 1,
    "Goa": 2,
    "Arunachal Pradesh": 2,
    "Mizoram": 1,
    "Sikkim": 1,
    "Puducherry": 1,
    "Chandigarh": 1,
    "Andaman & Nicobar": 1,
    "Dadra & Nagar Haveli": 1,
    "Daman & Diu": 1,
    "Lakshadweep": 1,
    "Ladakh": 1,
}

# Major parties with ideological positions
# position_x: economic (left=-1, right=+1)
# position_y: social (progressive=-1, conservative=+1)
INDIA_PARTIES = {
    # National parties
    "BJP": {"position_x": 0.4, "position_y": 0.6, "valence": 75, "color": "#FF9933"},
    "INC": {"position_x": -0.2, "position_y": -0.1, "valence": 55, "color": "#00BFFF"},
    "AAP": {"position_x": -0.3, "position_y": -0.3, "valence": 50, "color": "#0066FF"},
    # Regional parties
    "TMC": {
        "position_x": -0.1,
        "position_y": 0.1,
        "valence": 50,
        "color": "#20C20E",
    },  # West Bengal
    "DMK": {
        "position_x": -0.4,
        "position_y": -0.4,
        "valence": 55,
        "color": "#FF0000",
    },  # Tamil Nadu
    "AIADMK": {
        "position_x": -0.2,
        "position_y": 0.0,
        "valence": 45,
        "color": "#FF0000",
    },  # Tamil Nadu
    "SP": {"position_x": -0.3, "position_y": 0.2, "valence": 45, "color": "#FF0000"},  # UP alliance
    "BSP": {"position_x": -0.2, "position_y": 0.1, "valence": 40, "color": "#22409A"},  # UP
    "SS-UBT": {
        "position_x": 0.1,
        "position_y": 0.3,
        "valence": 45,
        "color": "#FF6600",
    },  # Maharashtra
    "NCP-SP": {
        "position_x": -0.1,
        "position_y": 0.0,
        "valence": 40,
        "color": "#00008B",
    },  # Maharashtra
    "JD(U)": {
        "position_x": 0.0,
        "position_y": 0.2,
        "valence": 45,
        "color": "#006400",
    },  # Bihar (NDA)
    "TDP": {"position_x": 0.1, "position_y": 0.1, "valence": 50, "color": "#FFFF00"},  # Andhra
    "BJD": {"position_x": 0.0, "position_y": 0.0, "valence": 55, "color": "#006400"},  # Odisha
    "YSR-CP": {"position_x": -0.1, "position_y": 0.1, "valence": 50, "color": "#0000FF"},  # Andhra
    "BRS": {"position_x": 0.0, "position_y": 0.1, "valence": 45, "color": "#FFC0CB"},  # Telangana
    "RJD": {
        "position_x": -0.3,
        "position_y": 0.2,
        "valence": 45,
        "color": "#006400",
    },  # Bihar (INDIA)
    "JMM": {"position_x": -0.2, "position_y": 0.1, "valence": 40, "color": "#008000"},  # Jharkhand
    "SAD": {"position_x": 0.1, "position_y": 0.3, "valence": 35, "color": "#0000FF"},  # Punjab
    "Others": {"position_x": 0.0, "position_y": 0.0, "valence": 25, "color": "#808080"},
}

# State-wise party strength (probability weights)
STATE_PARTY_WEIGHTS = {
    "Uttar Pradesh": {"BJP": 0.35, "SP": 0.25, "BSP": 0.15, "INC": 0.15, "Others": 0.10},
    "Maharashtra": {"BJP": 0.25, "SS-UBT": 0.15, "NCP-SP": 0.15, "INC": 0.20, "Others": 0.25},
    "West Bengal": {"TMC": 0.45, "BJP": 0.35, "INC": 0.05, "Others": 0.15},
    "Bihar": {"BJP": 0.25, "JD(U)": 0.20, "RJD": 0.25, "INC": 0.10, "Others": 0.20},
    "Tamil Nadu": {"DMK": 0.40, "AIADMK": 0.30, "BJP": 0.10, "INC": 0.10, "Others": 0.10},
    "Gujarat": {"BJP": 0.55, "INC": 0.35, "AAP": 0.05, "Others": 0.05},
    "Rajasthan": {"BJP": 0.45, "INC": 0.45, "Others": 0.10},
    "Madhya Pradesh": {"BJP": 0.50, "INC": 0.40, "Others": 0.10},
    "Karnataka": {"BJP": 0.40, "INC": 0.40, "JD(U)": 0.10, "Others": 0.10},
    "Andhra Pradesh": {"YSR-CP": 0.40, "TDP": 0.35, "BJP": 0.15, "Others": 0.10},
    "Telangana": {"BRS": 0.35, "INC": 0.30, "BJP": 0.25, "Others": 0.10},
    "Odisha": {"BJD": 0.45, "BJP": 0.35, "INC": 0.10, "Others": 0.10},
    "Kerala": {"INC": 0.35, "BJP": 0.20, "Others": 0.45},  # LDF vs UDF
    "Jharkhand": {"BJP": 0.35, "JMM": 0.30, "INC": 0.15, "Others": 0.20},
    "Assam": {"BJP": 0.45, "INC": 0.35, "Others": 0.20},
    "Punjab": {"INC": 0.30, "AAP": 0.30, "SAD": 0.15, "BJP": 0.15, "Others": 0.10},
    "Delhi": {"BJP": 0.40, "AAP": 0.35, "INC": 0.20, "Others": 0.05},
    "Haryana": {"BJP": 0.45, "INC": 0.40, "Others": 0.15},
    "Chhattisgarh": {"BJP": 0.45, "INC": 0.45, "Others": 0.10},
    "Uttarakhand": {"BJP": 0.55, "INC": 0.35, "Others": 0.10},
    "Himachal Pradesh": {"BJP": 0.50, "INC": 0.45, "Others": 0.05},
}

# Default weights for states not specified
DEFAULT_WEIGHTS = {"BJP": 0.40, "INC": 0.35, "Others": 0.25}

# Phase-wise election schedule (2024 pattern)
# 7 phases spanning ~6 weeks
INDIA_ELECTION_PHASES = {
    1: [
        "Assam",
        "Arunachal Pradesh",
        "Meghalaya",
        "Manipur",
        "Mizoram",
        "Nagaland",
        "Tripura",
        "Sikkim",
        "Uttarakhand",
        "Jammu & Kashmir",
        "Rajasthan",
    ],
    2: ["Kerala", "Karnataka", "Madhya Pradesh", "Chhattisgarh", "Maharashtra"],
    3: ["Gujarat", "Bihar", "Jharkhand", "Odisha", "West Bengal"],
    4: ["Andhra Pradesh", "Telangana", "Tamil Nadu", "Puducherry"],
    5: ["Uttar Pradesh", "Punjab", "Haryana", "Delhi", "Chandigarh", "Himachal Pradesh", "Ladakh"],
    6: ["Uttar Pradesh"],  # UP votes across multiple phases (simplified here)
    7: ["Bihar", "Uttar Pradesh", "West Bengal"],  # Remaining constituencies
}


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
    # NOTA close race detection
    nota_contested_seats: int = 0  # Seats where NOTA > victory margin
    nota_contested_list: list[str] = field(default_factory=list)  # List of "State: Constituency #"
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

        # NOTA impact
        if self.nota_contested_seats > 0:
            lines.append(f"\n⚠️ NOTA contested races: {self.nota_contested_seats}")
            lines.append("(NOTA votes exceeded victory margin)")

        return "\n".join(lines)


def simulate_india_election(
    n_voters_per_constituency: int = 10000,
    seed: int | None = None,
    verbose: bool = True,
    include_nota: bool = False,  # NEW: Enable NOTA tracking
    use_real_names: bool = True,  # TECHNICAL: Use real constituency names
    historical_data_path: str | None = None,  # TECHNICAL: Seed with historical data
) -> IndiaElectionResult:
    """
    Simulate India General Election.

    Args:
        n_voters_per_constituency: Voters per constituency
        seed: Random seed
        verbose: Print progress
        include_nota: Include NOTA
        use_real_names: Use real PC names
        historical_data_path: Path to CSV with previous results

    Returns:
        IndiaElectionResult with full results
    """
    from electoral_sim.data.india_pc import get_india_constituencies
    from electoral_sim.data.loaders import HistoricalDataLoader
    from electoral_sim.metrics.indices import effective_number_of_parties, gallagher_index

    manager = get_india_constituencies() if use_real_names else None

    # Load historical seeding if provided
    viability_seeding = None
    pc_viability = {}
    incumbent_parties = set()
    if historical_data_path:
        loader = HistoricalDataLoader(historical_data_path)
        viability_seeding = loader.get_viability_weights()
        pc_viability = loader.get_constituency_viability()
        incumbent_parties = set(loader.get_incumbents())
        if verbose:
            print(f"  Seeded with historical data from {historical_data_path}")

    rng = np.random.default_rng(seed)

    # Prepare party list
    party_names = list(INDIA_PARTIES.keys())
    party_data = [
        {
            "name": name,
            "position_x": data["position_x"],
            "position_y": data["position_y"],
            "valence": data["valence"],
            "incumbent": name in incumbent_parties,
            "viability": viability_seeding.get(name, 0.05) if viability_seeding else None,
        }
        for name, data in INDIA_PARTIES.items()
    ]

    # Add NOTA if enabled
    if include_nota:
        party_names.append("NOTA")
        party_data.append(
            {
                "name": "NOTA",
                "position_x": 0.0,
                "position_y": 0.0,
                "valence": 15,  # Low valence - protest vote
            }
        )

    n_parties = len(party_names)

    # Results storage
    all_seats = dict.fromkeys(party_names, 0)
    all_votes = dict.fromkeys(party_names, 0)
    state_results = {}
    total_voters = 0
    total_voted = 0

    # NOTA close race tracking
    nota_contested_seats = 0
    nota_contested_list = []

    start_time = time.perf_counter()

    global_const_id = 0
    voter_df_sample = None
    # Simulate each state
    for state, n_constituencies in INDIA_STATES.items():
        if verbose:
            print(f"  Simulating {state} ({n_constituencies} seats)...", end=" ", flush=True)

        state_start = time.perf_counter()

        # Get party weights for this state
        state_weights = STATE_PARTY_WEIGHTS.get(state, DEFAULT_WEIGHTS)

        # Create voters with state-specific ideology distribution
        n_voters = n_voters_per_constituency * n_constituencies
        total_voters += n_voters

        # Generate voter ideologies influenced by state patterns
        base_ideology_x = rng.normal(0, 0.3, n_voters)
        base_ideology_y = rng.normal(0, 0.3, n_voters)

        # State-specific shifts
        if state in ["Gujarat", "Rajasthan", "Madhya Pradesh", "Uttar Pradesh"]:
            base_ideology_x += 0.1  # Slightly right-leaning
            base_ideology_y += 0.1  # Slightly conservative
        elif state in ["Kerala", "West Bengal", "Tamil Nadu"]:
            base_ideology_x -= 0.1  # Slightly left-leaning

        # Assign constituency
        constituencies = rng.integers(0, n_constituencies, n_voters)

        # Compute utilities for each party
        utilities = np.zeros((n_voters, n_parties))
        for p, party in enumerate(party_names):
            # Handle NOTA separately (not in INDIA_PARTIES dict)
            if party == "NOTA":
                px, py, val = 0.0, 0.0, 15.0
            else:
                px = INDIA_PARTIES[party]["position_x"]
                py = INDIA_PARTIES[party]["position_y"]
                val = INDIA_PARTIES[party]["valence"]

            # Distance-based utility (smaller weight)
            dist = np.sqrt((base_ideology_x - px) ** 2 + (base_ideology_y - py) ** 2)
            utility = -dist * 0.3 + 0.005 * val

            # State-specific party strength (main factor)
            if party == "NOTA":
                # NOTA is a protest vote - small but universal appeal
                utility -= 1.0  # Lower than active parties
            else:
                # Use PC-level weights if available, else state weights
                # This is a bit complex in vectorized form, so we simplify:
                # If we have historical data for ANY party in this state, use it.
                if party in state_weights:
                    utility += state_weights[party] * 3.0

                # Boost based on national viability if historical seeding used
                if viability_seeding and party in viability_seeding:
                    utility += viability_seeding[party] * 0.5

            utilities[:, p] = utility

        # MNL voting (higher temperature = more randomness/closer races)
        temperature = 0.5  # Makes elections more competitive
        scaled = utilities / temperature
        scaled -= scaled.max(axis=1, keepdims=True)
        exp_utils = np.exp(scaled)
        probs = exp_utils / exp_utils.sum(axis=1, keepdims=True)

        # Sample votes
        cumprobs = np.cumsum(probs, axis=1)
        random_vals = rng.random((n_voters, 1))
        votes = (random_vals > cumprobs).sum(axis=1)

        # Turnout (~67% average)
        turnout_prob = rng.beta(5, 2.5, n_voters) * 0.85
        will_vote = rng.random(n_voters) < turnout_prob
        voted_count = will_vote.sum()
        total_voted += voted_count

        # FPTP counting
        state_seats = dict.fromkeys(party_names, 0)
        state_votes = dict.fromkeys(party_names, 0)

        for c in range(n_constituencies):
            c_mask = (constituencies == c) & will_vote
            c_votes = votes[c_mask]

            if len(c_votes) == 0:
                continue

            # Count votes per party
            vote_counts = np.bincount(c_votes, minlength=n_parties)

            # Total votes
            for p, count in enumerate(vote_counts):
                state_votes[party_names[p]] += count

            # Winner
            winner_idx = np.argmax(vote_counts)
            winner = party_names[winner_idx]

            # NOTA close race detection
            if include_nota and "NOTA" in party_names:
                nota_idx = party_names.index("NOTA")
                nota_votes = vote_counts[nota_idx]

                # Find runner-up (second highest)
                sorted_counts = np.sort(vote_counts)[::-1]
                winner_votes = sorted_counts[0]
                runner_up_votes = sorted_counts[1] if len(sorted_counts) > 1 else 0
                margin = winner_votes - runner_up_votes

                # If NOTA > margin, race is contested
                if nota_votes > margin and winner != "NOTA":
                    nota_contested_seats += 1
                    c_name = (
                        manager.get_name(global_const_id + c) if manager else f"Constituency {c+1}"
                    )
                    nota_contested_list.append(f"{state}: {c_name}")

            # Award seat (NOTA doesn't win seats)
            if winner != "NOTA":
                state_seats[winner] += 1

        # Aggregate
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

        # Sample for visualization
        state_voter_df = pl.DataFrame(
            {
                "ideology_x": base_ideology_x,
                "ideology_y": base_ideology_y,
                "vote": [party_names[v] for v in votes],
                "state": state,
            }
        )
        state_sample = state_voter_df.sample(min(100, len(state_voter_df)), seed=seed)
        if voter_df_sample is None:
            voter_df_sample = state_sample
        else:
            voter_df_sample = pl.concat([voter_df_sample, state_sample])

        global_const_id += n_constituencies

    # Calculate metrics
    total_votes = sum(all_votes.values())
    vote_shares = {p: v / total_votes for p, v in all_votes.items()}
    seat_shares = {p: s / 543 for p, s in all_seats.items()}

    vote_array = np.array(list(vote_shares.values()))
    seat_array = np.array(list(seat_shares.values()))

    gal_idx = gallagher_index(vote_array, seat_array)
    enp_v = effective_number_of_parties(vote_array)
    enp_s = effective_number_of_parties(seat_array)

    # Alliance totals
    nda_parties = {"BJP", "JD(U)", "TDP", "SAD"}  # NDA
    india_parties = {"INC", "AAP", "TMC", "DMK", "SP", "RJD", "SS-UBT", "NCP-SP", "JMM"}  # INDIA

    nda_seats = sum(all_seats.get(p, 0) for p in nda_parties)
    india_seats = sum(all_seats.get(p, 0) for p in india_parties)
    others_seats = 543 - nda_seats - india_seats

    elapsed = time.perf_counter() - start_time

    if verbose:
        print(f"\nTotal simulation time: {elapsed:.2f}s")

    # Collect party positions for mapping
    # We take the positions from the last used config logic
    # (Since INDIA_PARTIES is global, we can use that)
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
        voter_df=voter_df_sample if "voter_df_sample" in locals() else None,
        party_positions=party_pos,
    )


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  INDIA GENERAL ELECTION SIMULATOR")
    print("  Lok Sabha 2024-style simulation")
    print("=" * 60)
    print()

    # Simulate
    print("Running simulation (10K voters per constituency)...\n")
    result = simulate_india_election(
        n_voters_per_constituency=10000,  # ~5.4M total voters
        seed=2024,
        verbose=True,
    )

    print()
    print(result)
