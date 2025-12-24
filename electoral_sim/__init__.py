"""
ElectoralSim - India Electoral Simulation
Agent-based electoral simulation using mesa-frames
"""

__version__ = "0.1.0"

# Lazy imports to avoid requiring mesa-frames for basic functionality
def __getattr__(name):
    if name == "ElectionModel":
        from electoral_sim.model import ElectionModel
        return ElectionModel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# These modules don't require mesa-frames
from electoral_sim.systems import allocate_seats, dhondt_allocation, sainte_lague_allocation
from electoral_sim.metrics import gallagher_index, effective_number_of_parties
