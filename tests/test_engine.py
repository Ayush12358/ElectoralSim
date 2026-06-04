"""Tests for coalition formation, government stability, seat allocation, and alternative voting."""

import pytest
import numpy as np
from hypothesis import given, strategies as st, assume

# =============================================================================
# COALITION FORMATION
# =============================================================================


class TestCoalitionFormation:
    """Deep tests for coalition algorithms."""

    def test_mwc_finds_majority(self):
        from electoral_sim.engine.coalition import minimum_winning_coalitions

        seats = np.array([150, 120, 80, 50, 30, 20])
        mwcs = minimum_winning_coalitions(seats)
        assert len(mwcs) > 0
        total = seats.sum()
        majority = int(np.floor(total * 0.5)) + 1
        for coalition, seats_sum in mwcs:
            assert seats_sum >= majority

    def test_mwc_respects_super_majority(self):
        from electoral_sim.engine.coalition import minimum_winning_coalitions

        seats = np.array([100, 60, 40])
        mwcs = minimum_winning_coalitions(seats, majority_threshold=2 / 3)
        for coalition, seats_sum in mwcs:
            assert seats_sum >= 134

    def test_mcw_finds_connected_coalitions(self):
        from electoral_sim.engine.coalition import minimum_connected_winning

        seats = np.array([120, 100, 80, 40])
        positions = np.array([-0.8, -0.3, 0.2, 0.9])
        mcws = minimum_connected_winning(seats, positions, max_distance=0.6)
        for parties, total, policy_range in mcws:
            assert policy_range <= 0.6

    def test_mcw_2d_positions(self):
        from electoral_sim.engine.coalition import minimum_connected_winning

        seats = np.array([100, 80, 60])
        positions = np.array([[0.5, 0.1], [0.3, -0.2], [0.7, 0.0]])
        mcws = minimum_connected_winning(seats, positions)
        assert len(mcws) > 0

    def test_coalition_strain_1d(self):
        from electoral_sim.engine.coalition import coalition_strain

        positions = np.array([0.2, 0.8, 0.5])
        strain = coalition_strain(positions)
        assert strain >= 0

    def test_coalition_strain_weighted(self):
        from electoral_sim.engine.coalition import coalition_strain

        positions = np.array([[0.2], [0.8], [0.5]])
        unweighted = coalition_strain(positions)
        weighted = coalition_strain(positions, weights=np.array([0.6, 0.3, 0.1]))
        assert abs(unweighted - weighted) > 1e-8

    def test_coalition_strain_single_party(self):
        from electoral_sim.engine.coalition import coalition_strain

        assert coalition_strain(np.array([0.5])) == 0.0
        assert coalition_strain(np.array([[0.3, 0.1]])) == 0.0

    def test_coalition_strain_two_party(self):
        from electoral_sim.engine.coalition import coalition_strain

        positions = np.array([0.0, 1.0])
        strain = coalition_strain(positions)
        assert abs(strain - 1.0) < 0.01

    def test_coalition_strain_zero_weights(self, recwarn):
        from electoral_sim.engine.coalition import coalition_strain

        positions = np.array([[0.0], [1.0]])
        weights = np.array([0.0, 0.0])
        strain = coalition_strain(positions, weights=weights)
        assert strain == 0.0
        assert len(recwarn) == 0

    def test_predict_coalition_stability_bounds(self):
        from electoral_sim.engine.coalition import predict_coalition_stability

        for model in ["sigmoid", "linear", "exponential"]:
            for strain in [0.0, 0.5, 2.0]:
                for margin in [0.0, 0.1, 0.3]:
                    for n in [1, 2, 5]:
                        s = predict_coalition_stability(strain, margin, n, model=model)
                        assert 0.0 <= s <= 1.0

    def test_form_government_simple_majority(self):
        from electoral_sim.engine.coalition import form_government

        seats = np.array([200, 150, 100, 50])
        positions = np.array([0.6, 0.4, -0.3, -0.8])
        names = ["A", "B", "C", "D"]
        result = form_government(seats, positions, names)
        assert result["success"] is True
        assert result["seats"] >= 251

    def test_form_government_without_names(self):
        from electoral_sim.engine.coalition import form_government

        seats = np.array([200, 150, 100])
        positions = np.array([0.5, 0.4, -0.5])
        result = form_government(seats, positions)
        assert result["success"] is True
        assert all("Party " in n for n in result["coalition_names"])

    def test_form_government_with_office_weight(self):
        """form_government with office_weight uses utility-based formation."""
        from electoral_sim.engine.coalition import form_government

        seats = np.array([200, 150, 100, 50])
        positions = np.array([0.6, 0.4, -0.3, -0.8])
        result = form_government(seats, positions, office_weight=0.5)
        assert "success" in result

    def test_form_government_no_majority_possible(self):
        """form_government returns failure when no coalition can reach majority."""
        from electoral_sim.engine.coalition import form_government

        # All parties too small for 2/3 majority
        seats = np.array([10, 10, 10])
        positions = np.array([-1.0, 0.0, 1.0])
        result = form_government(seats, positions, majority_threshold=0.99)
        # Should either fail or succeed with very small coalition
        assert "success" in result

    def test_junior_partner_penalty(self):
        from electoral_sim.engine.coalition import junior_partner_penalty

        seats = np.array([200, 100, 50])
        penalties = junior_partner_penalty(seats, [0, 1, 2])
        assert penalties[0] > 0
        assert penalties[1] <= 0
        assert penalties[2] <= 0
        assert penalties[2] <= penalties[1]

    def test_junior_partner_penalty_single_party(self):
        """Single party coalition gets no penalty."""
        from electoral_sim.engine.coalition import junior_partner_penalty

        seats = np.array([200])
        penalties = junior_partner_penalty(seats, [0])
        assert penalties[0] == 0.0

    def test_laver_shepsle_allocation(self):
        from electoral_sim.engine.coalition import allocate_portfolios_laver_shepsle

        coalition = [0, 1, 2]
        seats = np.array([200, 150, 80])
        positions = np.array([[0.5, -0.2], [-0.3, 0.1], [0.1, 0.3]])
        result = allocate_portfolios_laver_shepsle(coalition, seats, positions)
        assert isinstance(result, dict)
        assert len(result) == 2

    def test_laver_shepsle_with_custom_dimensions(self):
        from electoral_sim.engine.coalition import allocate_portfolios_laver_shepsle

        coalition = [0, 1]
        seats = np.array([200, 150])
        positions = np.array([[0.5, -0.2], [-0.3, 0.1]])
        result = allocate_portfolios_laver_shepsle(
            coalition, seats, positions, dimensions=["Economy", "Social"]
        )
        assert "Economy" in result or "Social" in result

    def test_laver_shepsle_mismatched_dimensions(self):
        """Dimensions list length mismatch falls back to default names."""
        from electoral_sim.engine.coalition import allocate_portfolios_laver_shepsle

        coalition = [0, 1]
        seats = np.array([200, 150])
        positions = np.array([[0.5, -0.2], [-0.3, 0.1]])
        result = allocate_portfolios_laver_shepsle(
            coalition, seats, positions, dimensions=["OnlyOne"]
        )
        assert len(result) == 2  # Falls back to "Ministry 1", "Ministry 2"


# =============================================================================
# GOVERNMENT STABILITY
# =============================================================================


class TestGovernmentStability:
    """All collapse models, hazard rates, simulator lifecycle."""

    def test_collapse_sigmoid_model(self):
        from electoral_sim.engine.government import collapse_probability

        prob = collapse_probability(12, 0.5, 0.7, model="sigmoid")
        assert 0.0 <= prob <= 1.0

    def test_collapse_exponential_model(self):
        from electoral_sim.engine.government import collapse_probability

        prob = collapse_probability(12, 0.5, 0.7, model="exponential")
        assert 0.0 <= prob <= 1.0

    def test_collapse_linear_model(self):
        from electoral_sim.engine.government import collapse_probability

        prob = collapse_probability(24, 0.3, 0.5, model="linear")
        assert 0.0 <= prob <= 1.0

    def test_collapse_at_max_term_returns_1(self):
        from electoral_sim.engine.government import collapse_probability

        for model in ("sigmoid", "linear", "exponential"):
            prob = collapse_probability(60, 0.0, 1.0, model=model, max_term=60)
            assert prob == 1.0

    def test_collapse_high_strain_increases_risk(self):
        from electoral_sim.engine.government import collapse_probability

        low = collapse_probability(30, 0.0, 0.5)
        high = collapse_probability(30, 3.0, 0.5)
        assert high > low

    def test_collapse_high_stability_decreases_risk(self):
        from electoral_sim.engine.government import collapse_probability

        low_stab = collapse_probability(30, 0.5, 0.2)
        high_stab = collapse_probability(30, 0.5, 0.9)
        assert high_stab < low_stab

    def test_simulate_government_survival_structure(self):
        from electoral_sim.engine.government import simulate_government_survival

        result = simulate_government_survival(strain=0.3, stability=0.7, n_simulations=200, seed=42)
        for key in [
            "mean_survival",
            "median_survival",
            "std_survival",
            "full_term_prob",
            "early_collapse_prob",
            "min_survival",
            "max_survival",
        ]:
            assert key in result

    def test_simulate_all_models(self):
        from electoral_sim.engine.government import simulate_government_survival

        for m in ("sigmoid", "linear", "exponential"):
            r = simulate_government_survival(
                strain=0.3, stability=0.7, model=m, n_simulations=100, seed=42
            )
            assert r["mean_survival"] > 0

    def test_hazard_rate_all_phases(self):
        from electoral_sim.engine.government import hazard_rate

        h1 = hazard_rate(3)
        h2 = hazard_rate(12)
        h4 = hazard_rate(40)
        assert h1 > 0
        assert h2 > 0
        assert h4 > h2

    def test_hazard_rate_with_events(self):
        from electoral_sim.engine.government import hazard_rate

        base = hazard_rate(12, events=None)
        with_events = hazard_rate(
            12,
            events=[
                {"type": "scandal", "severity": 2.0},
                {"type": "economic_crisis", "severity": 1.5},
            ],
        )
        assert with_events > base

    def test_hazard_rate_unknown_event_type(self):
        from electoral_sim.engine.government import hazard_rate

        r = hazard_rate(12, events=[{"type": "unknown_event", "severity": 5.0}])
        assert r > 0

    def test_hazard_rate_defection_event(self):
        from electoral_sim.engine.government import hazard_rate

        base = hazard_rate(12)
        with_defection = hazard_rate(12, events=[{"type": "defection", "severity": 2.0}])
        assert with_defection > base

    def test_cox_proportional_hazard(self):
        from electoral_sim.engine.government import cox_proportional_hazard

        h = cox_proportional_hazard(
            12,
            covariates={
                "majority_margin": 0.1,
                "coalition_strain": 0.3,
                "n_parties": 3,
                "economic_growth": 0.02,
            },
        )
        assert h > 0

    def test_cox_higher_majority_lower_hazard(self):
        from electoral_sim.engine.government import cox_proportional_hazard

        low = cox_proportional_hazard(12, {"majority_margin": 0.05})
        high = cox_proportional_hazard(12, {"majority_margin": 0.30})
        assert high < low

    def test_cox_custom_coefficients(self):
        from electoral_sim.engine.government import cox_proportional_hazard

        h = cox_proportional_hazard(
            12,
            {"majority_margin": 0.1},
            coefficients={"majority_margin": -3.0},
        )
        assert h > 0

    def test_simulator_lifecycle(self):
        from electoral_sim.engine.government import GovernmentSimulator

        gov = GovernmentSimulator(strain=0.3, stability=0.7, coalition_parties=["A", "B"], seed=42)
        assert gov.step() is True
        assert gov.months_in_office == 1
        summary = gov.summary()
        assert summary["coalition"] == ["A", "B"]

    def test_simulator_with_events(self):
        from electoral_sim.engine.government import GovernmentSimulator

        gov = GovernmentSimulator(strain=0.3, stability=0.7, seed=42)
        gov.add_event("scandal", severity=5.0)
        assert len(gov.events) == 1

    def test_simulator_simulate_to_term(self):
        from electoral_sim.engine.government import GovernmentSimulator

        gov = GovernmentSimulator(strain=0.0, stability=1.0, seed=42)
        months = gov.simulate(max_months=30)
        assert months <= 30

    def test_simulator_step_after_collapse(self):
        from electoral_sim.engine.government import GovernmentSimulator

        gov = GovernmentSimulator(strain=10.0, stability=0.01, seed=42)
        gov.simulate(max_months=60)
        assert gov.collapsed
        assert gov.step() is False


# =============================================================================
# SEAT ALLOCATION
# =============================================================================


class TestAllocationMethods:
    """All 4 allocation methods + proportionality."""

    def test_dhondt_basic(self):
        from electoral_sim.systems.allocation import dhondt_allocation

        seats = dhondt_allocation(np.array([100000, 80000, 30000]), 10)
        assert sum(seats) == 10

    def test_sainte_lague_basic(self):
        from electoral_sim.systems.allocation import sainte_lague_allocation

        seats = sainte_lague_allocation(np.array([100000, 80000, 30000]), 10)
        assert sum(seats) == 10

    def test_hare_basic(self):
        from electoral_sim.systems.allocation import hare_quota_allocation

        seats = hare_quota_allocation(np.array([100000, 80000, 30000]), 10)
        assert sum(seats) == 10

    def test_droop_basic(self):
        from electoral_sim.systems.allocation import droop_quota_allocation

        seats = droop_quota_allocation(np.array([100000, 80000, 30000]), 10)
        assert sum(seats) == 10

    def test_allocation_with_threshold(self):
        """Threshold filters out small parties."""
        from electoral_sim.systems.allocation import dhondt_allocation

        votes = np.array([100000, 80000, 30000, 1000])
        seats = dhondt_allocation(votes, 10, threshold=0.05)
        assert sum(seats) == 10
        # Smallest party (1000 votes, ~0.5%) should get 0 seats
        assert seats[3] == 0

    def test_allocate_seats_registry(self):
        """allocate_seats dispatches to correct method."""
        from electoral_sim.systems.allocation import allocate_seats

        votes = np.array([100000, 80000, 30000])
        for method in ["dhondt", "sainte_lague", "hare", "droop"]:
            seats = allocate_seats(votes, 10, method)
            assert sum(seats) == 10

    def test_fptp_allocation(self):
        """fptp_allocation from Polars DataFrame."""
        from electoral_sim.systems.allocation import fptp_allocation
        import polars as pl

        df = pl.DataFrame(
            {
                "constituency": [0, 0, 0, 1, 1, 1],
                "party": [0, 1, 2, 0, 1, 2],
                "votes": [500, 300, 200, 400, 600, 100],
            }
        )
        seats = fptp_allocation(df, n_constituencies=2)
        assert sum(seats) == 2
        assert seats[0] == 1  # Party 0 wins constituency 0
        assert seats[1] == 1  # Party 1 wins constituency 1


# =============================================================================
# COUNTING MODULE
# =============================================================================


class TestCounting:
    """Tests for core/counting.py."""

    def test_count_fptp(self):
        from electoral_sim.core.counting import count_fptp

        constituencies = np.array([0, 0, 0, 1, 1, 1])
        votes = np.array([0, 0, 1, 0, 1, 1])
        result = count_fptp(constituencies, votes, n_constituencies=2, n_parties=2)
        assert result["system"] == "FPTP"
        assert result["seats"].sum() == 2
        assert result["vote_counts"].sum() == 6

    def test_count_pr(self):
        from electoral_sim.core.counting import count_pr

        votes = np.array([0, 0, 0, 1, 1, 2])
        result = count_pr(votes, n_parties=3, n_seats=10)
        assert result["system"] == "PR"
        assert result["seats"].sum() == 10

    def test_count_pr_with_threshold(self):
        from electoral_sim.core.counting import count_pr

        votes = np.array([0, 0, 0, 0, 0, 1, 1, 2])
        result = count_pr(votes, n_parties=3, n_seats=10, threshold=0.2)
        assert result["seats"].sum() == 10


# =============================================================================
# ALTERNATIVE VOTING SYSTEMS
# =============================================================================


class TestAlternativeVoting:
    """IRV, STV, approval, condorcet, ranking generation."""

    def test_irv_election(self):
        from electoral_sim import irv_election

        rankings = np.array([[1, 2, 3], [1, 3, 2], [2, 1, 3], [3, 2, 1], [3, 1, 2]])
        result = irv_election(rankings, n_candidates=3)
        assert "winner" in result
        assert result["winner"] in [0, 1, 2]

    def test_irv_majority_first_round(self):
        """IRV with clear majority winner in first round."""
        from electoral_sim import irv_election

        # Candidate 0 wins outright with 4/5 first-choice votes
        rankings = np.array(
            [
                [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3],
                [2, 1, 3],
            ]
        )
        result = irv_election(rankings, n_candidates=3)
        assert result["winner"] == 0
        assert len(result["rounds"]) == 1

    def test_irv_with_unranked_candidates(self):
        """IRV with some candidates unranked (rank 0)."""
        from electoral_sim import irv_election

        # Candidate 2 is unranked by some voters
        rankings = np.array(
            [
                [1, 2, 0],  # Voter ranks A=1st, B=2nd, C unranked
                [1, 0, 2],  # Voter ranks A=1st, C=2nd, B unranked
                [2, 1, 0],  # Voter ranks B=1st, A=2nd, C unranked
                [0, 1, 2],  # Voter ranks B=1st, C=2nd, A unranked
                [0, 2, 1],  # Voter ranks C=1st, B=2nd, A unranked
            ]
        )
        result = irv_election(rankings, n_candidates=3)
        assert "winner" in result
        assert result["winner"] is not None

    def test_stv_election(self):
        from electoral_sim import stv_election

        rankings = np.array(
            [
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [2, 1, 3, 4],
                [2, 1, 3, 4],
                [3, 1, 2, 4],
                [3, 2, 1, 4],
                [3, 2, 1, 4],
                [4, 3, 2, 1],
                [4, 3, 2, 1],
            ]
        )
        result = stv_election(rankings, n_candidates=4, n_seats=2)
        assert "elected" in result
        assert len(result["elected"]) == 2

    def test_stv_single_seat(self):
        """STV with 1 seat is equivalent to IRV."""
        from electoral_sim import stv_election

        rankings = np.array(
            [
                [1, 2, 3],
                [1, 2, 3],
                [2, 1, 3],
                [3, 1, 2],
                [3, 2, 1],
            ]
        )
        result = stv_election(rankings, n_candidates=3, n_seats=1)
        assert "elected" in result
        assert len(result["elected"]) == 1

    def test_stv_surplus_transfer(self):
        """STV with a candidate exceeding quota triggers surplus transfer."""
        from electoral_sim import stv_election

        # Candidate 0 has way more than quota, surplus should transfer
        rankings = np.array(
            [
                [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3],
                [1, 2, 3],
                [2, 1, 3],
                [2, 1, 3],
                [2, 1, 3],
                [3, 1, 2],
            ]
        )
        result = stv_election(rankings, n_candidates=3, n_seats=2)
        assert "elected" in result
        assert len(result["elected"]) == 2
        assert len(result["rounds"]) >= 1

    def test_approval_voting(self):
        from electoral_sim import approval_voting

        approvals = np.array([[1, 1, 0], [1, 0, 0], [0, 1, 1], [1, 1, 0], [0, 0, 1]])
        result = approval_voting(approvals, n_candidates=3)
        assert "winner" in result
        assert "approval_counts" in result

    def test_approval_voting_unanimous(self):
        """Approval voting with unanimous approval."""
        from electoral_sim import approval_voting

        approvals = np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]])
        result = approval_voting(approvals, n_candidates=3)
        assert result["winner"] == 0

    def test_approval_voting_shares(self):
        """approval_voting returns approval_shares."""
        from electoral_sim import approval_voting

        approvals = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
        result = approval_voting(approvals, n_candidates=3)
        assert "approval_shares" in result
        assert abs(result["approval_shares"].sum() - approvals.sum() / 3) < 0.01

    def test_approval_voting_empty(self):
        """approval_voting handles zero voters gracefully."""
        from electoral_sim import approval_voting

        result = approval_voting(np.empty((0, 3)), n_candidates=3)
        assert result["winner"] == -1
        assert result["approval_counts"].sum() == 0
        assert result["approval_shares"].sum() == 0

    def test_irv_rejects_duplicate_ranks(self):
        """IRV raises ValueError for duplicate ranks in a voter's ballot."""
        from electoral_sim import irv_election

        rankings = np.array([[1, 1, 2]])  # Duplicate first choice
        with pytest.raises(ValueError, match="Duplicate ranks"):
            irv_election(rankings, n_candidates=3)

    def test_irv_rejects_out_of_range_ranks(self):
        """IRV raises ValueError for ranks beyond n_candidates."""
        from electoral_sim import irv_election

        rankings = np.array([[1, 2, 5]])  # Rank 5 > n_candidates=3
        with pytest.raises(ValueError, match="Out-of-range"):
            irv_election(rankings, n_candidates=3)

    def test_irv_rejects_shape_mismatch(self):
        """IRV raises ValueError when rankings cols != n_candidates."""
        from electoral_sim import irv_election

        rankings = np.array([[1, 2], [2, 1]])  # 2 cols, n_candidates=3
        with pytest.raises(ValueError, match="shape"):
            irv_election(rankings, n_candidates=3)

    def test_irv_rejects_negative_n_candidates(self):
        """IRV raises ValueError for n_candidates <= 0."""
        from electoral_sim import irv_election

        rankings = np.array([[1, 2]])
        with pytest.raises(ValueError, match="n_candidates"):
            irv_election(rankings, n_candidates=0)

    def test_irv_with_exhausted_ballots(self):
        """IRV with exhausted ballots (voters who rank no remaining candidates)."""
        from electoral_sim import irv_election

        # Voter 3 exhausts after round 1 (only ranks candidate 2)
        rankings = np.array(
            [
                [1, 2, 3],  # A > B > C
                [1, 2, 3],  # A > B > C
                [2, 1, 3],  # B > A > C
                [0, 1, 0],  # Only ranks B (exhausts after B eliminated)
            ]
        )
        result = irv_election(rankings, n_candidates=3)
        assert "winner" in result
        assert result["final_votes"].sum() > 0  # final tally should be non-zero

    def test_condorcet_winner_exists(self):
        from electoral_sim import condorcet_winner

        rankings = np.array(
            [
                [1, 2, 3],
                [1, 2, 3],
                [1, 3, 2],
                [2, 1, 3],
            ]
        )
        result = condorcet_winner(rankings, n_candidates=3)
        assert result["has_condorcet"] is True
        assert result["condorcet_winner"] is not None

    def test_condorcet_cycle_no_winner(self):
        from electoral_sim import condorcet_winner

        rankings = np.array(
            [
                [1, 2, 3],
                [2, 1, 3],
                [3, 1, 2],
            ]
        )
        result = condorcet_winner(rankings, n_candidates=3)
        assert "has_condorcet" in result

    def test_generate_rankings(self):
        from electoral_sim import generate_rankings

        utilities = np.array([[0.9, 0.5, 0.1], [0.2, 0.8, 0.3], [0.1, 0.2, 0.9]])
        rankings = generate_rankings(utilities)
        assert rankings.shape == (3, 3)
        assert rankings[0, 0] == 1

    def test_generate_rankings_with_n_ranked(self):
        from electoral_sim import generate_rankings

        utilities = np.array([[0.9, 0.5, 0.1], [0.2, 0.8, 0.3]])
        rankings = generate_rankings(utilities, n_ranked=2)
        assert rankings.shape == (2, 3)
        assert rankings[0, 0] == 1
        assert rankings[0, 1] == 2
        assert rankings[0, 2] == 0
        assert rankings[1, 1] == 1
        assert rankings[1, 2] == 2


# =============================================================================
# DUEVERGER'S LAW
# =============================================================================


class TestAllocationKnownResults:
    """Formal known-result tests for PR allocation methods."""

    def test_dhondt_known_result(self):
        """D'Hondt with votes [100,80,30] and 5 seats → [3,2,0]."""
        from electoral_sim.systems.allocation import dhondt_allocation

        seats = dhondt_allocation(np.array([100, 80, 30]), 5)
        assert seats.tolist() == [3, 2, 0]

    def test_sainte_lague_known_result(self):
        """Sainte-Lague with votes [100,80,30] and 5 seats → [2,2,1]."""
        from electoral_sim.systems.allocation import sainte_lague_allocation

        seats = sainte_lague_allocation(np.array([100, 80, 30]), 5)
        assert seats.tolist() == [2, 2, 1]

    def test_hare_known_result(self):
        """Hare quota with votes [100,80,30] and 5 seats → [2,2,1]."""
        from electoral_sim.systems.allocation import hare_quota_allocation

        seats = hare_quota_allocation(np.array([100, 80, 30]), 5)
        assert seats.tolist() == [2, 2, 1]

    def test_droop_known_result(self):
        """Droop quota with votes [100,80,30] and 5 seats → [2,2,1]."""
        from electoral_sim.systems.allocation import droop_quota_allocation

        seats = droop_quota_allocation(np.array([100, 80, 30]), 5)
        assert seats.tolist() == [2, 2, 1]

    def test_dhondt_with_threshold(self):
        """D'Hondt with 30% threshold filters party C → [3,2,0]."""
        from electoral_sim.systems.allocation import dhondt_allocation

        seats = dhondt_allocation(np.array([100, 80, 30]), 5, threshold=0.3)
        assert seats.tolist() == [3, 2, 0]

    def test_all_allocators_seat_sum_invariant(self):
        """All allocators return exactly n_seats when votes are valid."""
        from electoral_sim.systems.allocation import (
            dhondt_allocation,
            sainte_lague_allocation,
            hare_quota_allocation,
            droop_quota_allocation,
        )

        votes = np.array([100, 80, 30])
        for allocator in [dhondt_allocation, sainte_lague_allocation, hare_quota_allocation, droop_quota_allocation]:
            for n in [1, 3, 5, 10]:
                seats = allocator(votes, n)
                assert seats.sum() == n, f"{allocator.__name__} with n={n}: {seats.tolist()}"

    def test_hare_quota_recomputed_after_threshold(self):
        """Hare quota uses post-threshold total_votes, not pre-threshold."""
        from electoral_sim.systems.allocation import hare_quota_allocation

        # Parties A=0.476, B=0.381, C=0.143 of total 210
        # Threshold 0.2 excludes C; post-threshold total = 180
        seats = hare_quota_allocation(np.array([100, 80, 30]), 5, threshold=0.2)
        assert seats.sum() == 5

    def test_droop_quota_recomputed_after_threshold(self):
        """Droop quota uses post-threshold total_votes, not pre-threshold."""
        from electoral_sim.systems.allocation import droop_quota_allocation

        seats = droop_quota_allocation(np.array([100, 80, 30]), 5, threshold=0.2)
        assert seats.sum() == 5


class TestDuverger:
    """Tests for duverger.py."""

    def test_run_duverger_fptp(self):
        from electoral_sim.analysis.duverger import run_duverger_experiment

        history = run_duverger_experiment(
            n_voters=500,
            n_parties=5,
            n_steps=3,
            system="FPTP",
            seed=42,
        )
        assert len(history) == 3
        for entry in history:
            assert "enp" in entry
            assert "vote_shares" in entry
            assert entry["enp"] >= 1.0

    def test_run_duverger_pr(self):
        from electoral_sim.analysis.duverger import run_duverger_experiment

        history = run_duverger_experiment(
            n_voters=500,
            n_parties=5,
            n_steps=3,
            system="PR",
            seed=42,
        )
        assert len(history) == 3
        for entry in history:
            assert entry["enp"] >= 1.0


# =============================================================================
# NUMBA ACCELERATION WRAPPERS
# =============================================================================


class TestNumbaWrappers:
    """Test Numba-accelerated wrapper functions."""

    def test_dhondt_fast(self):
        from electoral_sim.engine.numba_accel import dhondt_fast

        votes = np.array([10000, 8000, 3000], dtype=np.int64)
        seats = dhondt_fast(votes, 10)
        assert seats.sum() == 10

    def test_dhondt_fast_with_threshold(self):
        from electoral_sim.engine.numba_accel import dhondt_fast

        votes = np.array([10000, 8000, 3000, 100], dtype=np.int64)
        seats = dhondt_fast(votes, 10, threshold=0.05)
        assert seats.sum() == 10

    def test_sainte_lague_fast(self):
        from electoral_sim.engine.numba_accel import sainte_lague_fast

        votes = np.array([10000, 8000, 3000], dtype=np.int64)
        seats = sainte_lague_fast(votes, 10)
        assert seats.sum() == 10

    def test_sainte_lague_fast_with_threshold(self):
        from electoral_sim.engine.numba_accel import sainte_lague_fast

        votes = np.array([10000, 8000, 3000, 100], dtype=np.int64)
        seats = sainte_lague_fast(votes, 10, threshold=0.05)
        assert seats.sum() == 10

    def test_vote_mnl_fast(self):
        from electoral_sim.engine.numba_accel import vote_mnl_fast

        utilities = np.array(
            [
                [1.0, 0.5, 0.1],
                [0.2, 0.8, 0.3],
                [0.1, 0.2, 0.9],
            ]
        )
        rng = np.random.default_rng(42)
        votes = vote_mnl_fast(utilities, temperature=0.5, rng=rng)
        assert len(votes) == 3
        assert all(0 <= v < 3 for v in votes)

    def test_vote_mnl_deterministic(self):
        """Low temperature makes MNL nearly deterministic."""
        from electoral_sim.engine.numba_accel import vote_mnl_fast

        utilities = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        rng = np.random.default_rng(42)
        votes = vote_mnl_fast(utilities, temperature=0.01, rng=rng)
        assert votes[0] == 0
        assert votes[1] == 1
        assert votes[2] == 2

    def test_fptp_count_fast(self):
        from electoral_sim.engine.numba_accel import fptp_count_fast

        constituencies = np.array([0, 0, 0, 1, 1, 1], dtype=np.int64)
        votes = np.array([0, 0, 1, 0, 1, 1], dtype=np.int64)
        seats, vote_counts = fptp_count_fast(constituencies, votes, 2, 2)
        assert seats.sum() == 2
        assert vote_counts.sum() == 6

    def test_fptp_count_fast_empty_constituency(self):
        from electoral_sim.engine.numba_accel import fptp_count_fast

        constituencies = np.array([0, 0, 2, 2], dtype=np.int64)
        votes = np.array([0, 1, 0, 1], dtype=np.int64)
        seats, vote_counts = fptp_count_fast(constituencies, votes, 3, 2)
        assert vote_counts.sum() == 4

    def test_fptp_count_fast_parallel_race_regression(self):
        """Deterministic regression: all constituencies won by same party → correct seats."""
        pytest.importorskip("numba")
        from electoral_sim.engine.numba_accel import fptp_count_fast

        n_constituencies = 500
        n_parties = 5
        n_voters_per_constituency = 100

        # All voters vote for party 0 in all constituencies
        constituencies = np.repeat(np.arange(n_constituencies), n_voters_per_constituency)
        votes = np.zeros(len(constituencies), dtype=np.int64)

        seats, vote_counts = fptp_count_fast(
            constituencies.astype(np.int64),
            votes.astype(np.int64),
            n_constituencies,
            n_parties,
        )

        # Race condition would cause lost seat updates → seats[0] < n_constituencies
        assert seats[0] == n_constituencies, (
            f"Race condition: expected {n_constituencies} seats for party 0, got {seats[0]}. "
            f"All seats: {seats}"
        )
        assert seats.sum() == n_constituencies, (
            f"Total seats {seats.sum()} != constituencies {n_constituencies}"
        )
        assert seats[1:].sum() == 0

    def test_benchmark_numba(self):
        """benchmark_numba runs without error."""
        from electoral_sim.engine.numba_accel import benchmark_numba

        # Should run without crashing
        benchmark_numba()


class TestFptpTieBreaking:
    """Verify deterministic FPTP tie-breaking across both counting paths."""

    def test_tie_picks_first_party_numba(self):
        """Numba path: tie goes to lower-index party."""
        from electoral_sim.engine.numba_accel import fptp_count_fast

        constituencies = np.array([0, 0, 0, 0], dtype=np.int64)
        votes = np.array([0, 1, 0, 1], dtype=np.int64)
        seats, _ = fptp_count_fast(constituencies, votes, n_constituencies=1, n_parties=2)
        assert seats[0] == 1  # First party in tie wins
        assert seats[1] == 0

    def test_tie_picks_first_party_polars(self):
        """Polars path: tie goes to party appearing first in sorted order."""
        from electoral_sim.systems.allocation import fptp_allocation
        import polars as pl

        df = pl.DataFrame({
            "constituency": [0, 0],
            "party": [0, 1],
            "votes": [100, 100],
        })
        seats = fptp_allocation(df, n_constituencies=1)
        assert seats[0] == 1
        assert seats[1] == 0

    def test_both_paths_agree_on_tie(self):
        """Numba and Polars FPTP counting agree on tie outcomes."""
        from electoral_sim.engine.numba_accel import fptp_count_fast
        from electoral_sim.systems.allocation import fptp_allocation
        import polars as pl

        constituencies = np.array([0, 0, 0, 0], dtype=np.int64)
        votes = np.array([0, 1, 0, 1], dtype=np.int64)
        seats_numba, _ = fptp_count_fast(constituencies, votes, 1, 2)

        df = pl.DataFrame({
            "constituency": [0, 0],
            "party": [0, 1],
            "votes": [2, 2],
        })
        seats_polars = fptp_allocation(df, n_constituencies=1)
        assert (seats_numba == seats_polars).all()


class TestRankedChoiceProperties:
    """Hypothesis property tests for IRV/STV edge cases."""

    @given(
        n_voters=st.integers(min_value=1, max_value=20),
        n_candidates=st.integers(min_value=1, max_value=5),
    )
    def test_irv_no_crash(self, n_voters, n_candidates):
        """IRV never crashes unexpectedly for any ballot configuration."""
        from electoral_sim import irv_election

        rankings = np.random.randint(0, n_candidates + 1, size=(n_voters, n_candidates))
        try:
            result = irv_election(rankings, n_candidates)
            assert "winner" in result
            assert result["winner"] is not None
            assert -1 <= result["winner"] < n_candidates
        except ValueError as e:
            assert "Duplicate" in str(e) or "shape" in str(e) or "n_candidates" in str(e)

    @given(
        n_voters=st.integers(min_value=1, max_value=20),
        n_candidates=st.integers(min_value=2, max_value=5),
        n_seats=st.integers(min_value=1, max_value=3),
    )
    def test_stv_no_crash(self, n_voters, n_candidates, n_seats):
        """STV never crashes unexpectedly for any ballot configuration."""
        from electoral_sim import stv_election

        assume(n_seats < n_candidates)
        rankings = np.random.randint(0, n_candidates + 1, size=(n_voters, n_candidates))
        try:
            result = stv_election(rankings, n_candidates, n_seats)
            assert "elected" in result
            assert all(0 <= e < n_candidates for e in result["elected"])
        except ValueError as e:
            assert "Duplicate" in str(e) or "shape" in str(e) or "n_candidates" in str(e)

    def test_irv_all_unranked(self):
        """IRV handles all-unranked ballots (all zeros)."""
        from electoral_sim import irv_election

        rankings = np.zeros((5, 3), dtype=int)
        result = irv_election(rankings, n_candidates=3)
        assert result["winner"] is not None
        assert -1 <= result["winner"] < 3

    def test_irv_single_candidate(self):
        """IRV handles single-candidate election."""
        from electoral_sim import irv_election

        rankings = np.array([[1], [1], [1]])
        result = irv_election(rankings, n_candidates=1)
        assert result["winner"] == 0

    def test_irv_tied_rankings(self):
        """IRV handles tied rankings (duplicate ranks)."""
        from electoral_sim import irv_election

        rankings = np.array([[2, 2, 1], [3, 3, 3]])
        with pytest.raises(ValueError, match="Duplicate"):
            irv_election(rankings, n_candidates=3)
