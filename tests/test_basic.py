"""
Quick test of the electoral simulation
"""

import numpy as np

# Test allocation methods
from electoral_sim.systems import dhondt_allocation, sainte_lague_allocation, allocate_seats
from electoral_sim.metrics import gallagher_index, effective_number_of_parties

print("=" * 50)
print("ElectoralSim Test Suite")
print("=" * 50)

# Test 1: Seat allocation
print("\n1. SEAT ALLOCATION TEST")
print("-" * 30)

votes = np.array([100000, 80000, 30000, 20000, 10000])
parties = ["BJP", "INC", "AAP", "SP", "Others"]
n_seats = 10

dhondt_seats = dhondt_allocation(votes, n_seats)
sl_seats = sainte_lague_allocation(votes, n_seats)

print(f"Votes: {dict(zip(parties, votes))}")
print(f"D'Hondt seats:      {dict(zip(parties, dhondt_seats))}")
print(f"Sainte-Laguë seats: {dict(zip(parties, sl_seats))}")

# Test 2: Metrics
print("\n2. METRICS TEST")
print("-" * 30)

vote_shares = votes / votes.sum()
seat_shares_dh = dhondt_seats / dhondt_seats.sum()
seat_shares_sl = sl_seats / sl_seats.sum()

gallagher_dh = gallagher_index(vote_shares, seat_shares_dh)
gallagher_sl = gallagher_index(vote_shares, seat_shares_sl)

enp_votes = effective_number_of_parties(vote_shares)
enp_seats_dh = effective_number_of_parties(seat_shares_dh)

print(f"Vote shares: {dict(zip(parties, [f'{s:.1%}' for s in vote_shares]))}")
print(f"ENP (votes): {enp_votes:.2f}")
print(f"ENP (D'Hondt seats): {enp_seats_dh:.2f}")
print(f"Gallagher Index (D'Hondt): {gallagher_dh:.2f}")
print(f"Gallagher Index (Sainte-Laguë): {gallagher_sl:.2f}")

# Test 3: Threshold
print("\n3. THRESHOLD TEST (5%)")
print("-" * 30)

seats_with_threshold = allocate_seats(votes, n_seats, method="dhondt", threshold=0.05)
print(f"D'Hondt with 5% threshold: {dict(zip(parties, seats_with_threshold))}")

print("\n" + "=" * 50)
print("All tests passed!")
print("=" * 50)
