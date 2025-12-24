"""
Voter Agent for Electoral Simulation
Uses mesa-frames AgentSet with Polars DataFrame backend
"""

from mesa_frames import AgentSet, Model
import polars as pl
import numpy as np
from typing import Optional


class VoterAgents(AgentSet):
    """
    Voter agents stored as Polars DataFrame for vectorized operations.
    
    Attributes (DataFrame columns):
        - unique_id: Agent identifier (auto-generated)
        - constituency: Constituency index (0 to n_constituencies-1)
        - ideology_x: Economic left-right (-1 to 1)
        - ideology_y: Social liberal-conservative (-1 to 1)  
        - party_id: Current party identification
        - knowledge: Political knowledge (0-100)
        - turnout_prob: Base probability of voting (0-1)
        - media_susceptibility: Susceptibility to media influence (0-1)
        - is_zealot: Whether agent is a zealot (fixed opinion)
    """
    
    def __init__(
        self, 
        n: int, 
        n_constituencies: int, 
        n_parties: int, 
        model: Model,
        zealot_fraction: float = 0.0,
    ):
        super().__init__(model)
        
        self.n_parties = n_parties
        self.n_constituencies = n_constituencies
        
        # Initialize voter attributes as DataFrame
        self += pl.DataFrame({
            "constituency": np.random.randint(0, n_constituencies, n),
            "ideology_x": np.clip(np.random.normal(0, 0.3, n), -1, 1),
            "ideology_y": np.clip(np.random.normal(0, 0.3, n), -1, 1),
            "party_id": np.random.randint(0, n_parties, n),
            "knowledge": np.random.uniform(20, 100, n),
            "turnout_prob": np.random.beta(5, 2, n),  # Skewed toward higher turnout
            "media_susceptibility": np.random.uniform(0, 1, n),
            "is_zealot": np.random.random(n) < zealot_fraction,
        })
    
    @property
    def n_voters(self) -> int:
        """Total number of voters."""
        return len(self.df)
    
    def get_ideology_matrix(self) -> np.ndarray:
        """Return ideology positions as (n_voters, 2) array."""
        return np.column_stack([
            self.df["ideology_x"].to_numpy(),
            self.df["ideology_y"].to_numpy()
        ])
    
    def compute_distances(self, party_positions: np.ndarray) -> np.ndarray:
        """
        Compute Euclidean distance from each voter to each party.
        
        Args:
            party_positions: Array of shape (n_parties, 2)
            
        Returns:
            Array of shape (n_voters, n_parties)
        """
        voter_pos = self.get_ideology_matrix()  # (n_voters, 2)
        
        # Broadcast subtraction: (n_voters, 1, 2) - (1, n_parties, 2)
        diff = voter_pos[:, np.newaxis, :] - party_positions[np.newaxis, :, :]
        distances = np.linalg.norm(diff, axis=2)  # (n_voters, n_parties)
        
        return distances
    
    def compute_utilities(self, party_positions: np.ndarray) -> np.ndarray:
        """
        Compute utility for each party (negative distance).
        
        Args:
            party_positions: Array of shape (n_parties, 2)
            
        Returns:
            Array of shape (n_voters, n_parties)
        """
        return -self.compute_distances(party_positions)
    
    def vote_proximity(self, party_positions: np.ndarray) -> np.ndarray:
        """
        Deterministic proximity voting: vote for nearest party.
        
        Returns:
            Array of vote choices (party indices)
        """
        distances = self.compute_distances(party_positions)
        return np.argmin(distances, axis=1)
    
    def vote_mnl(
        self, 
        party_positions: np.ndarray, 
        temperature: float = 0.5
    ) -> np.ndarray:
        """
        Multinomial logit (probabilistic) voting.
        
        P(vote for j) = exp(U_j / τ) / Σ exp(U_k / τ)
        
        Args:
            party_positions: Array of shape (n_parties, 2)
            temperature: τ parameter (lower = more deterministic)
            
        Returns:
            Array of vote choices (party indices)
        """
        utilities = self.compute_utilities(party_positions)
        
        # Softmax with temperature
        # Subtract max for numerical stability
        utilities_scaled = utilities / temperature
        utilities_scaled -= utilities_scaled.max(axis=1, keepdims=True)
        exp_utils = np.exp(utilities_scaled)
        probs = exp_utils / exp_utils.sum(axis=1, keepdims=True)
        
        # Vectorized multinomial sampling
        cumprobs = np.cumsum(probs, axis=1)
        random_vals = np.random.random((len(probs), 1))
        votes = (random_vals > cumprobs).sum(axis=1)
        
        return votes
    
    def decide_turnout(self) -> np.ndarray:
        """
        Determine which voters turn out based on turnout probability.
        
        Returns:
            Boolean array of who will vote
        """
        random_vals = np.random.random(self.n_voters)
        return random_vals < self.df["turnout_prob"].to_numpy()
    
    def update_opinions_noisy_voter(
        self, 
        adjacency: np.ndarray,
        mutation_rate: float = 0.01
    ):
        """
        Noisy voter model opinion dynamics.
        
        Each non-zealot voter either:
        - Copies a random neighbor's party_id (with prob 1-mutation_rate)
        - Randomly changes party_id (with prob mutation_rate)
        
        Args:
            adjacency: Sparse adjacency matrix (n_voters x n_voters)
            mutation_rate: Probability of spontaneous opinion change
        """
        current_ids = self.df["party_id"].to_numpy().copy()
        is_zealot = self.df["is_zealot"].to_numpy()
        
        # For each voter, sample a random neighbor
        # This is simplified - in production, use sparse matrix operations
        n = self.n_voters
        
        for i in range(n):
            if is_zealot[i]:
                continue  # Zealots never change
                
            if np.random.random() < mutation_rate:
                # Mutation: random party
                current_ids[i] = np.random.randint(0, self.n_parties)
            else:
                # Copy neighbor (simplified: random other voter)
                neighbor = np.random.randint(0, n)
                current_ids[i] = current_ids[neighbor]
        
        # Update DataFrame
        self.df = self.df.with_columns(pl.Series("party_id", current_ids))
    
    def step(self):
        """Called each simulation step."""
        pass  # Override in subclass or call update methods directly
