"""
ElectionModel - Main simulation model using mesa-frames
Handles India-scale electoral simulation with constituency-based structure
"""

from mesa_frames import AgentSet, Model
import polars as pl
import numpy as np
from typing import Optional


class VoterAgents(AgentSet):
    """
    Voter agents stored as Polars DataFrame for vectorized operations.
    
    Columns:
        - unique_id: Agent identifier
        - constituency: Constituency index (0-542 for Lok Sabha)
        - ideology_x: Left-right position (-1 to 1)
        - ideology_y: Social liberal-conservative (-1 to 1)
        - party_id: Current party identification (0 to n_parties-1)
        - knowledge: Political knowledge (0-100)
        - turnout_prob: Probability of voting (0-1)
    """
    
    def __init__(self, n: int, n_constituencies: int, n_parties: int, model: "ElectionModel"):
        super().__init__(model)
        
        # Initialize voter attributes as DataFrame
        self += pl.DataFrame({
            "constituency": np.random.randint(0, n_constituencies, n),
            "ideology_x": np.random.normal(0, 0.3, n),  # Left-right
            "ideology_y": np.random.normal(0, 0.3, n),  # Social
            "party_id": np.random.randint(0, n_parties, n),
            "knowledge": np.random.uniform(0, 100, n),
            "turnout_prob": np.random.uniform(0.4, 0.9, n),
        })
        
        self.n_parties = n_parties
    
    def compute_utilities(self, party_positions: np.ndarray) -> pl.DataFrame:
        """
        Compute utility for each party using proximity model.
        Returns DataFrame with utility columns for each party.
        
        Args:
            party_positions: Array of shape (n_parties, 2) with ideology positions
        """
        utilities = {}
        
        for p in range(self.n_parties):
            # Euclidean distance in 2D ideology space
            dist = np.sqrt(
                (self.df["ideology_x"].to_numpy() - party_positions[p, 0])**2 +
                (self.df["ideology_y"].to_numpy() - party_positions[p, 1])**2
            )
            # Utility = negative distance (closer = higher utility)
            utilities[f"utility_{p}"] = -dist
        
        return pl.DataFrame(utilities)
    
    def vote_mnl(self, party_positions: np.ndarray, temperature: float = 0.5) -> pl.Series:
        """
        Multinomial logit voting model.
        
        P(vote for j) = exp(U_j / τ) / Σ exp(U_k / τ)
        
        Args:
            party_positions: Array of shape (n_parties, 2)
            temperature: τ parameter (lower = more deterministic)
        
        Returns:
            Series of vote choices (party indices)
        """
        utilities = self.compute_utilities(party_positions)
        utility_matrix = utilities.to_numpy()
        
        # Softmax with temperature
        exp_utils = np.exp(utility_matrix / temperature)
        probs = exp_utils / exp_utils.sum(axis=1, keepdims=True)
        
        # Sample votes based on probabilities
        votes = np.array([
            np.random.choice(self.n_parties, p=p) for p in probs
        ])
        
        return pl.Series("vote", votes)
    
    def decide_turnout(self) -> pl.Series:
        """
        Determine which voters turn out based on turnout probability.
        Returns boolean Series.
        """
        random_vals = np.random.random(len(self.df))
        return pl.Series("will_vote", random_vals < self.df["turnout_prob"].to_numpy())
    
    def step(self):
        """Called each simulation step for opinion dynamics."""
        # Placeholder for opinion dynamics (noisy voter model, etc.)
        pass


class PartyAgents(AgentSet):
    """
    Party/Candidate agents.
    
    Columns:
        - unique_id: Party identifier
        - name: Party name
        - position_x: Left-right ideology
        - position_y: Social ideology
        - valence: Non-policy appeal (0-100)
        - incumbent: Whether currently in power
    """
    
    def __init__(self, parties: list[dict], model: "ElectionModel"):
        super().__init__(model)
        
        self += pl.DataFrame({
            "name": [p["name"] for p in parties],
            "position_x": [p.get("position_x", 0) for p in parties],
            "position_y": [p.get("position_y", 0) for p in parties],
            "valence": [p.get("valence", 50) for p in parties],
            "incumbent": [p.get("incumbent", False) for p in parties],
        })
    
    def get_positions(self) -> np.ndarray:
        """Return party positions as numpy array of shape (n_parties, 2)."""
        return np.column_stack([
            self.df["position_x"].to_numpy(),
            self.df["position_y"].to_numpy()
        ])
    
    def step(self):
        """Called each step for party adaptation."""
        # Placeholder for adaptive party behavior
        pass


class ElectionModel(Model):
    """
    Main election simulation model.
    
    Supports:
        - Multiple constituencies (default: 543 for Lok Sabha)
        - Configurable electoral systems (FPTP, PR)
        - Opinion dynamics on social networks
    """
    
    def __init__(
        self,
        n_voters: int = 100_000,
        n_constituencies: int = 10,
        parties: Optional[list[dict]] = None,
        electoral_system: str = "FPTP",
        temperature: float = 0.5,
    ):
        super().__init__()
        
        # Default parties if not provided
        if parties is None:
            parties = [
                {"name": "Party A", "position_x": -0.3, "position_y": 0.1},
                {"name": "Party B", "position_x": 0.3, "position_y": -0.1},
                {"name": "Party C", "position_x": 0.0, "position_y": 0.3},
            ]
        
        self.n_constituencies = n_constituencies
        self.n_parties = len(parties)
        self.electoral_system = electoral_system
        self.temperature = temperature
        
        # Create agent sets
        self.voters = VoterAgents(n_voters, n_constituencies, self.n_parties, self)
        self.parties = PartyAgents(parties, self)
        
        self.sets += self.voters
        self.sets += self.parties
        
        # Results storage
        self.election_results = []
    
    def run_election(self) -> dict:
        """
        Run a single election and return results.
        
        Returns:
            Dictionary with vote counts, seat allocation, and metrics
        """
        # Get party positions
        party_positions = self.parties.get_positions()
        
        # Determine turnout
        will_vote = self.voters.decide_turnout()
        
        # Cast votes
        votes = self.voters.vote_mnl(party_positions, self.temperature)
        
        # Add to voter DataFrame temporarily
        voter_df = self.voters.df.with_columns([
            will_vote.alias("will_vote"),
            votes.alias("vote")
        ])
        
        # Filter to only those who voted
        voted_df = voter_df.filter(pl.col("will_vote"))
        
        # Count votes by constituency and party
        if self.electoral_system == "FPTP":
            results = self._count_fptp(voted_df)
        else:
            results = self._count_pr(voted_df)
        
        self.election_results.append(results)
        return results
    
    def _count_fptp(self, voted_df: pl.DataFrame) -> dict:
        """First Past The Post: winner takes all in each constituency."""
        # Count votes per constituency per party
        vote_counts = voted_df.group_by(["constituency", "vote"]).len()
        
        # Find winner in each constituency
        winners = (
            vote_counts
            .sort("len", descending=True)
            .group_by("constituency")
            .first()
        )
        
        # Count seats per party
        seat_counts = winners.group_by("vote").len().rename({"len": "seats"})
        
        # Total votes per party
        total_votes = voted_df.group_by("vote").len().rename({"len": "votes"})
        
        return {
            "system": "FPTP",
            "seat_counts": seat_counts.to_dict(),
            "vote_counts": total_votes.to_dict(),
            "turnout": len(voted_df) / len(self.voters.df),
            "n_constituencies": self.n_constituencies,
        }
    
    def _count_pr(self, voted_df: pl.DataFrame) -> dict:
        """Proportional Representation with D'Hondt allocation."""
        # Total votes per party
        vote_counts = voted_df.group_by("vote").len()
        votes = vote_counts["len"].to_numpy()
        party_ids = vote_counts["vote"].to_numpy()
        
        # D'Hondt allocation
        seats = self._dhondt(votes, self.n_constituencies)
        
        seat_df = pl.DataFrame({
            "vote": party_ids,
            "seats": seats
        })
        
        return {
            "system": "PR",
            "seat_counts": seat_df.to_dict(),
            "vote_counts": vote_counts.to_dict(),
            "turnout": len(voted_df) / len(self.voters.df),
            "n_constituencies": self.n_constituencies,
        }
    
    def _dhondt(self, votes: np.ndarray, n_seats: int) -> np.ndarray:
        """D'Hondt seat allocation method."""
        n_parties = len(votes)
        seats = np.zeros(n_parties, dtype=int)
        
        for _ in range(n_seats):
            # Quotients: votes / (seats + 1)
            quotients = votes / (seats + 1)
            winner = np.argmax(quotients)
            seats[winner] += 1
        
        return seats
    
    def step(self):
        """Run one simulation step (for opinion dynamics)."""
        self.sets.do("step")
    
    def run(self, n_steps: int = 100, election_interval: int = 10):
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


# Quick test
if __name__ == "__main__":
    print("Creating model with 100K voters...")
    model = ElectionModel(n_voters=100_000, n_constituencies=10)
    
    print("Running election...")
    results = model.run_election()
    
    print(f"\nResults ({results['system']}):")
    print(f"Turnout: {results['turnout']:.1%}")
    print(f"Seats: {results['seat_counts']}")
    print(f"Votes: {results['vote_counts']}")
