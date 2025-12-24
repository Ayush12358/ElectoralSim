"""
Historical Data Loaders

Provides utilities for loading real-world election results to seed
the simulation with viability and incumbency data.
"""

import polars as pl
import numpy as np
from typing import Dict, List, Optional, Any
from pathlib import Path

class HistoricalDataLoader:
    """
    Loads historical election results and converts them to simulation inputs.
    
    Expected CSV schema:
        - constituency: str (name)
        - party: str (party name)
        - votes: int
        - seats: int (optional)
        - year: int (optional)
    """
    
    def __init__(self, data_path: str | Path):
        self.path = Path(data_path)
        if not self.path.exists():
            raise FileNotFoundError(f"Historical data not found at {self.path}")
            
        self.df = pl.read_csv(self.path)
        
    def get_viability_weights(self, year: Optional[int] = None) -> Dict[str, float]:
        """
        Calculate global viability weights (vote shares) per party.
        """
        df = self.df
        if year and "year" in df.columns:
            df = df.filter(pl.col("year") == year)
            
        # Group by party and sum votes
        party_votes = df.group_by("party").agg(pl.col("votes").sum())
        total_votes = party_votes["votes"].sum()
        
        weights = {}
        for row in party_votes.to_dicts():
            weights[row["party"]] = row["votes"] / total_votes
            
        return weights

    def get_incumbents(self, year: Optional[int] = None) -> List[str]:
        """
        Get list of parties that won seats in the historical data.
        """
        df = self.df
        if year and "year" in df.columns:
            df = df.filter(pl.col("year") == year)
            
        if "seats" not in df.columns:
            # Estimate incumbents by top party in each constituency
            incumbents = (
                df.group_by("constituency")
                .agg(pl.col("party").sort_by("votes", descending=True).first())
                ["party"]
                .unique()
                .to_list()
            )
        else:
            incumbents = df.filter(pl.col("seats") > 0)["party"].unique().to_list()
            
        return incumbents

    def get_constituency_viability(self, year: Optional[int] = None) -> Dict[str, Dict[str, float]]:
        """
        Get state/constituency specific party strengths.
        Returns: {constituency_name: {party_name: vote_share}}
        """
        df = self.df
        if year and "year" in df.columns:
            df = df.filter(pl.col("year") == year)
            
        results = {}
        for const_name, group in df.group_by("constituency"):
            total = group["votes"].sum()
            results[const_name] = {
                row["party"]: row["votes"] / total 
                for row in group.to_dicts()
            }
        return results
