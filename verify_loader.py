from electoral_sim.data.loaders import HistoricalDataLoader
from pathlib import Path

csv_path = Path("electoral_sim/data/india_2024_sample.csv")
loader = HistoricalDataLoader(csv_path)

print(f"Loading data from: {csv_path}")

# 1. Global viability
weights = loader.get_viability_weights()
print("\nGlobal Viability Weights:")
for party, weight in sorted(weights.items(), key=lambda x: -x[1]):
    print(f"  {party:10} {weight:.2%}")

# 2. Incumbents
incumbents = loader.get_incumbents()
print(f"\nIncumbent Parties: {', '.join(incumbents)}")

# 3. Constituency level
const_viability = loader.get_constituency_viability()
print("\nSample Constituency (Amethi):")
if "Amethi" in const_viability:
    for party, share in const_viability["Amethi"].items():
        print(f"  {party:10} {share:.2%}")

# 4. Filter by year
weights_2024 = loader.get_viability_weights(year=2024)
assert len(weights_2024) > 0
print("\nYear filtering works!")
