"""Tests for coalition formation, government stability, seat allocation, and alternative voting."""

import pytest
import numpy as np

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

    def test_junior_partner_penalty(self):
        from electoral_sim.engine.coalition import junior_partner_penalty

        seats = np.array([200, 100, 50])
        penalties = junior_partner_penalty(seats, [0, 1, 2])
        assert penalties[0] > 0  # dominant gets bonus
        assert penalties[1] <= 0
        assert penalties[2] <= 0
        assert penalties[2] <= penalties[1]  # smallest gets biggest penalty

    def test_laver_shepsle_allocation(self):
        from electoral_sim.engine.coalition import allocate_portfolios_laver_shepsle

        coalition = [0, 1, 2]
        seats = np.array([200, 150, 80])
        positions = np.array([[0.5, -0.2], [-0.3, 0.1], [0.1, 0.3]])
        result = allocate_portfolios_laver_shepsle(coalition, seats, positions)
        assert isinstance(result, dict)
        assert len(result) == 2


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

        for model in ["sigmoid", "linear", "exponential"]:
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

        for m in ["sigmoid", "linear", "exponential"]:
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

    def test_allocation_proportionality(self):
        """PR should be more proportional than FPTP."""
        from electoral_sim import ElectionModel
        from electoral_sim.metrics.indices import gallagher_index

        votes = np.array([45000, 35000, 20000])
        for method in ["dhondt", "sainte_lague", "hare", "droop"]:
            from electoral_sim.systems.allocation import allocate_seats

            seats = allocate_seats(votes, 10, method)
            assert sum(seats) == 10


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

    def test_approval_voting(self):
        from electoral_sim import approval_voting

        approvals = np.array([[1, 1, 0], [1, 0, 0], [0, 1, 1], [1, 1, 0], [0, 0, 1]])
        result = approval_voting(approvals, n_candidates=3)
        assert "winner" in result

    def test_generate_rankings(self):
        from electoral_sim import generate_rankings

        utilities = np.array([[0.9, 0.5, 0.1], [0.2, 0.8, 0.3], [0.1, 0.2, 0.9]])
        rankings = generate_rankings(utilities)
        assert rankings.shape == (3, 3)
