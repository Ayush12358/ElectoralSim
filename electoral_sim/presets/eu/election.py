"""
European Parliament Election Simulator

Simulates EU Parliament elections with:
- 720 MEPs (post-2024 allocation)
- 27 member states
- Country-specific MEP allocations (degressive proportionality)
- 7 main political groups + non-attached
"""

import time
from dataclasses import dataclass

import numpy as np

# =============================================================================
# EU PARLIAMENT DATA
# =============================================================================

# Member states and their MEP allocations (2024-2029 term)
# Based on degressive proportionality principle
EU_MEMBER_STATES = {
    # Large states
    "Germany": 96,
    "France": 81,
    "Italy": 76,
    "Spain": 61,
    "Poland": 53,
    # Medium states
    "Romania": 33,
    "Netherlands": 31,
    "Belgium": 22,
    "Czech Republic": 21,
    "Greece": 21,
    "Hungary": 21,
    "Portugal": 21,
    "Sweden": 21,
    "Austria": 20,
    "Bulgaria": 17,
    "Denmark": 15,
    "Finland": 15,
    "Slovakia": 15,
    "Ireland": 14,
    "Croatia": 12,
    # Small states
    "Lithuania": 11,
    "Latvia": 9,
    "Slovenia": 9,
    "Estonia": 7,
    "Cyprus": 6,
    "Luxembourg": 6,
    "Malta": 6,
}

# Total MEPs = 720

# EU Parliament Political Groups (as of 2024)
# position_x: economic (left=-1, right=+1)
# position_y: EU integration (pro-EU=-1, eurosceptic=+1)
EU_POLITICAL_GROUPS = {
    "EPP": {
        "name": "European People's Party",
        "position_x": 0.3,
        "position_y": -0.2,
        "valence": 65,
        "color": "#003399",
    },
    "S&D": {
        "name": "Socialists & Democrats",
        "position_x": -0.3,
        "position_y": -0.3,
        "valence": 60,
        "color": "#ED1B24",
    },
    "Renew": {
        "name": "Renew Europe",
        "position_x": 0.1,
        "position_y": -0.4,
        "valence": 55,
        "color": "#FFD700",
    },
    "Greens/EFA": {
        "name": "Greens/European Free Alliance",
        "position_x": -0.4,
        "position_y": -0.5,
        "valence": 50,
        "color": "#00A651",
    },
    "ECR": {
        "name": "European Conservatives and Reformists",
        "position_x": 0.5,
        "position_y": 0.3,
        "valence": 45,
        "color": "#0054A5",
    },
    "ID": {
        "name": "Identity and Democracy",
        "position_x": 0.6,
        "position_y": 0.6,
        "valence": 40,
        "color": "#003366",
    },
    "Left": {
        "name": "The Left (GUE/NGL)",
        "position_x": -0.6,
        "position_y": -0.1,
        "valence": 40,
        "color": "#990000",
    },
    "NI": {
        "name": "Non-Inscrits (Non-attached)",
        "position_x": 0.0,
        "position_y": 0.5,
        "valence": 30,
        "color": "#808080",
    },
}

# Country-specific party strength patterns (simplified)
# Maps countries to their dominant political group leanings
COUNTRY_GROUP_WEIGHTS = {
    # Western Europe - center-right/center-left balance
    "Germany": {
        "EPP": 0.28,
        "S&D": 0.20,
        "Greens/EFA": 0.15,
        "Renew": 0.12,
        "Left": 0.08,
        "ECR": 0.10,
        "ID": 0.05,
        "NI": 0.02,
    },
    "France": {
        "Renew": 0.22,
        "ID": 0.25,
        "EPP": 0.10,
        "S&D": 0.15,
        "Greens/EFA": 0.08,
        "Left": 0.10,
        "ECR": 0.05,
        "NI": 0.05,
    },
    "Italy": {
        "ECR": 0.30,
        "S&D": 0.20,
        "EPP": 0.10,
        "Renew": 0.08,
        "Greens/EFA": 0.05,
        "Left": 0.05,
        "ID": 0.15,
        "NI": 0.07,
    },
    "Spain": {
        "EPP": 0.35,
        "S&D": 0.30,
        "Renew": 0.05,
        "Greens/EFA": 0.05,
        "Left": 0.12,
        "ECR": 0.08,
        "ID": 0.03,
        "NI": 0.02,
    },
    "Poland": {
        "EPP": 0.35,
        "ECR": 0.30,
        "S&D": 0.10,
        "Renew": 0.08,
        "Left": 0.05,
        "Greens/EFA": 0.02,
        "ID": 0.05,
        "NI": 0.05,
    },
    # Default for other countries
    "_default": {
        "EPP": 0.25,
        "S&D": 0.20,
        "Renew": 0.15,
        "Greens/EFA": 0.10,
        "ECR": 0.12,
        "ID": 0.08,
        "Left": 0.05,
        "NI": 0.05,
    },
}


@dataclass
class EUElectionResult:
    """Results of EU Parliament election simulation."""

    seats: dict[str, int]  # Group -> seats
    vote_shares: dict[str, float]
    country_results: dict[str, dict]
    turnout: float
    gallagher_index: float
    enp_votes: float
    enp_seats: float
    # Coalition analysis
    pro_eu_seats: int  # EPP + S&D + Renew + Greens
    eurosceptic_seats: int  # ECR + ID + NI
    majority_threshold: int = 361  # 720 / 2 + 1

    def __str__(self):
        lines = ["=" * 60]
        lines.append("EUROPEAN PARLIAMENT ELECTION RESULTS")
        lines.append("=" * 60)
        lines.append(f"\nTurnout: {self.turnout:.1%}")
        lines.append(f"Gallagher Index: {self.gallagher_index:.2f}")
        lines.append(f"ENP (votes): {self.enp_votes:.2f}")
        lines.append(f"ENP (seats): {self.enp_seats:.2f}")
        lines.append(f"\n{'Group':20} {'Seats':>8} {'Vote %':>8}")
        lines.append("-" * 40)

        sorted_groups = sorted(self.seats.items(), key=lambda x: -x[1])
        for group, seats in sorted_groups:
            if seats > 0:
                vote_pct = self.vote_shares.get(group, 0) * 100
                lines.append(f"{group:20} {seats:>8} {vote_pct:>7.1f}%")

        lines.append("\n" + "-" * 40)
        lines.append(f"{'Pro-EU (EPP+S&D+Renew+Greens)':30} {self.pro_eu_seats:>5}")
        lines.append(f"{'Eurosceptic (ECR+ID+NI)':30} {self.eurosceptic_seats:>5}")
        lines.append(f"{'Left':30} {self.seats.get('Left', 0):>5}")
        lines.append("-" * 40)
        lines.append(f"{'TOTAL':30} {sum(self.seats.values()):>5}")
        lines.append(f"\nMajority threshold: {self.majority_threshold}")

        if self.pro_eu_seats >= self.majority_threshold:
            lines.append("🇪🇺 Pro-EU coalition has majority!")
        else:
            lines.append("⚖️ Grand coalition needed for majority")

        return "\n".join(lines)


def simulate_eu_election(
    n_voters_per_mep: int = 5000,
    seed: int | None = None,
    verbose: bool = True,
) -> EUElectionResult:
    """
    Simulate European Parliament Election.

    Args:
        n_voters_per_mep: Voters simulated per MEP seat (affects accuracy vs speed)
            - 1000 = quick (~5 seconds)
            - 5000 = normal (~15 seconds)
            - 20000 = detailed (~60 seconds)
        seed: Random seed for reproducibility
        verbose: Print progress

    Returns:
        EUElectionResult with full results
    """
    from electoral_sim.metrics.indices import effective_number_of_parties, gallagher_index

    rng = np.random.default_rng(seed)

    # Prepare group list
    group_names = list(EU_POLITICAL_GROUPS.keys())
    n_groups = len(group_names)

    # Results storage
    all_seats = dict.fromkeys(group_names, 0)
    all_votes = dict.fromkeys(group_names, 0)
    country_results = {}
    total_voters = 0
    total_voted = 0

    start_time = time.perf_counter()

    if verbose:
        print("🇪🇺 Simulating EU Parliament Election (720 MEPs, 27 States)")
        print("=" * 60)

    # Simulate each member state
    for country, n_meps in EU_MEMBER_STATES.items():
        if verbose:
            print(f"  {country} ({n_meps} MEPs)...", end=" ", flush=True)

        country_start = time.perf_counter()

        # Get group weights for this country
        weights = COUNTRY_GROUP_WEIGHTS.get(country, COUNTRY_GROUP_WEIGHTS["_default"])

        # Normalize weights to include all groups
        normalized_weights = {}
        for g in group_names:
            normalized_weights[g] = weights.get(g, 0.05)  # Default 5% for missing
        total_w = sum(normalized_weights.values())
        normalized_weights = {k: v / total_w for k, v in normalized_weights.items()}

        # Create voters
        n_voters = n_voters_per_mep * n_meps
        total_voters += n_voters

        # Generate voter ideologies
        ideology_x = rng.normal(0, 0.3, n_voters)
        ideology_y = rng.normal(0, 0.3, n_voters)

        # Compute utilities for each group
        utilities = np.zeros((n_voters, n_groups))
        for g, group in enumerate(group_names):
            gx = EU_POLITICAL_GROUPS[group]["position_x"]
            gy = EU_POLITICAL_GROUPS[group]["position_y"]
            val = EU_POLITICAL_GROUPS[group]["valence"]

            # Distance-based utility
            dist = np.sqrt((ideology_x - gx) ** 2 + (ideology_y - gy) ** 2)
            utility = -dist * 0.3 + 0.005 * val

            # Country-specific group strength
            weight = normalized_weights.get(group, 0.05)
            utility += weight * 3.0

            utilities[:, g] = utility

        # MNL voting
        temperature = 0.5
        scaled = utilities / temperature
        scaled -= scaled.max(axis=1, keepdims=True)
        exp_utils = np.exp(scaled)
        probs = exp_utils / exp_utils.sum(axis=1, keepdims=True)

        # Sample votes
        cumprobs = np.cumsum(probs, axis=1)
        random_vals = rng.random((n_voters, 1))
        votes = (random_vals > cumprobs).sum(axis=1)

        # Turnout (EU average ~50%, varies by country)
        base_turnout = 0.50 + rng.normal(0, 0.1)  # Country variation
        turnout_prob = np.clip(rng.beta(3, 3, n_voters) * base_turnout * 2, 0.2, 0.9)
        will_vote = rng.random(n_voters) < turnout_prob
        voted_count = will_vote.sum()
        total_voted += voted_count

        # Count votes
        country_votes = dict.fromkeys(group_names, 0)
        valid_votes = votes[will_vote]
        for v in valid_votes:
            country_votes[group_names[v]] += 1

        # Allocate seats using D'Hondt (most common in EU)
        vote_counts = np.array([country_votes[g] for g in group_names])

        # D'Hondt allocation
        seats = np.zeros(n_groups, dtype=int)
        for _ in range(n_meps):
            quotients = vote_counts / (seats + 1)
            winner = np.argmax(quotients)
            seats[winner] += 1

        country_seats = {group_names[i]: int(seats[i]) for i in range(n_groups)}

        # Aggregate
        for group in group_names:
            all_seats[group] += country_seats[group]
            all_votes[group] += country_votes[group]

        country_results[country] = {
            "seats": country_seats,
            "votes": country_votes,
            "turnout": voted_count / n_voters,
        }

        country_time = time.perf_counter() - country_start
        if verbose:
            top_group = max(country_seats.items(), key=lambda x: x[1])
            print(f"done ({country_time*1000:.0f}ms) - {top_group[0]}: {top_group[1]}")

    # Calculate metrics
    total_votes_cast = sum(all_votes.values())
    vote_shares = {g: v / total_votes_cast for g, v in all_votes.items()}
    seat_shares = {g: s / 720 for g, s in all_seats.items()}

    vote_array = np.array(list(vote_shares.values()))
    seat_array = np.array(list(seat_shares.values()))

    gal_idx = gallagher_index(vote_array, seat_array)
    enp_v = effective_number_of_parties(vote_array)
    enp_s = effective_number_of_parties(seat_array)

    # Coalition analysis
    pro_eu_groups = {"EPP", "S&D", "Renew", "Greens/EFA"}
    eurosceptic_groups = {"ECR", "ID", "NI"}

    pro_eu_seats = sum(all_seats.get(g, 0) for g in pro_eu_groups)
    eurosceptic_seats = sum(all_seats.get(g, 0) for g in eurosceptic_groups)

    elapsed = time.perf_counter() - start_time

    if verbose:
        print(f"\nTotal simulation time: {elapsed:.2f}s")

    return EUElectionResult(
        seats=all_seats,
        vote_shares=vote_shares,
        country_results=country_results,
        turnout=total_voted / total_voters,
        gallagher_index=gal_idx,
        enp_votes=enp_v,
        enp_seats=enp_s,
        pro_eu_seats=pro_eu_seats,
        eurosceptic_seats=eurosceptic_seats,
    )


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print()
    result = simulate_eu_election(
        n_voters_per_mep=5000,
        seed=2024,
        verbose=True,
    )
    print()
    print(result)
