"""
Voter Behavior Models

Implements different factors that influence voter utility and choice.
Modular and pluggable.
"""

import numpy as np
from typing import Protocol, runtime_checkable

@runtime_checkable
class BehaviorModel(Protocol):
    """Protocol for voting behavior components."""
    def compute_utility(self, voters, parties, **kwargs) -> np.ndarray:
        ...


class ProximityModel:
    """Standard spatial model: utility decreases with ideological distance."""
    
    def __init__(self, weight: float = 1.0, dimensionality: int = 2):
        self.weight = weight
        self.dimensionality = dimensionality
        
    def compute_utility(self, voter_positions: np.ndarray, party_positions: np.ndarray, **kwargs) -> np.ndarray:
        """
        Args:
            voter_positions: (n_voters, dims)
            party_positions: (n_parties, dims)
        Returns:
            (n_voters, n_parties) utility matrix
        """
        # (n_voters, 1, dims) - (1, n_parties, dims) -> (n_voters, n_parties, dims)
        diff = voter_positions[:, np.newaxis, :] - party_positions[np.newaxis, :, :]
        dist = np.linalg.norm(diff, axis=2)
        return -self.weight * dist


class ValenceModel:
    """Valence model: utility increases with party's non-policy appeal."""
    
    def __init__(self, weight: float = 0.01):
        self.weight = weight
        
    def compute_utility(self, n_voters: int, valence: np.ndarray, **kwargs) -> np.ndarray:
        """
        Args:
            n_voters: Number of voters
            valence: (n_parties,) valence scores
        Returns:
            (n_voters, n_parties) utility matrix
        """
        return np.tile(self.weight * valence, (n_voters, 1))


class RetrospectiveModel:
    """Economic/Retrospective voting: reward/punish incumbents based on 'economic mood'."""
    
    def __init__(self, weight: float = 0.5):
        self.weight = weight
        
    def compute_utility(self, n_voters: int, n_parties: int, incumbent_mask: np.ndarray, economic_growth: float, **kwargs) -> np.ndarray:
        """
        Args:
            incumbent_mask: bool array (n_parties,)
            economic_growth: Current growth rate (can be voter-specific or global)
        """
        utility = np.zeros((n_voters, n_parties))
        # Logic: If growth > 0, bonus to incumbents. If growth < 0, penalty.
        # Here we assume a simple global growth for now
        reward = self.weight * economic_growth
        utility[:, incumbent_mask] = reward
        return utility


class StrategicVotingModel:
    """Strategic voting: voters discount candidates seen as unviable (Duverger's Law)."""
    
    def __init__(self, sensitivity: float = 1.0):
        self.sensitivity = sensitivity
        
    def compute_utility(self, n_voters: int, viability: np.ndarray, **kwargs) -> np.ndarray:
        """
        Args:
            viability: (n_parties,) estimated probability of winning or 'expected vote share'
        """
        # Penalty for low viability
        penalty = self.sensitivity * (np.log(viability + 1e-6))
        return np.tile(penalty, (n_voters, 1))


class BehaviorEngine:
    """Combines multiple behavior models into a single utility matrix."""
    
    def __init__(self):
        self.models = []
        
    def add_model(self, model, weight: float = 1.0):
        self.models.append((model, weight))
        
    def compute_all(self, voter_data: dict, party_data: dict, **kwargs) -> np.ndarray:
        n_voters = voter_data['n_voters']
        n_parties = party_data['n_parties']
        
        total_utility = np.zeros((n_voters, n_parties))
        
        for model, w in self.models:
            if isinstance(model, ProximityModel):
                u = model.compute_utility(voter_data['positions'], party_data['positions'])
            elif isinstance(model, ValenceModel):
                u = model.compute_utility(n_voters, party_data['valence'])
            elif isinstance(model, RetrospectiveModel):
                u = model.compute_utility(n_voters, n_parties, party_data['incumbents'], kwargs.get('growth', 0.0))
            elif isinstance(model, StrategicVotingModel):
                u = model.compute_utility(n_voters, party_data.get('viability', np.ones(n_parties)))
            else:
                # Generic call if it follows protocol
                u = model.compute_utility(voter_data, party_data, **kwargs)
                
            total_utility += w * u
            
        return total_utility
