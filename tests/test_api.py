"""Test new API"""
from electoral_sim import ElectionModel, Config, PRESETS

print("=== Testing New API ===")

# Test 1: Simple usage
print("\n1. Simple usage:")
model = ElectionModel(n_voters=10000, seed=42)
r = model.run_election()
print(f"   Turnout: {r['turnout']:.1%}")

# Test 2: From preset
print("\n2. From preset:")
model = ElectionModel.from_preset("india", n_voters=20000, seed=42)
print(f"   Constituencies: {model.n_constituencies}")
print(f"   Parties: {len(model.parties)}")

# Test 3: Chainable API
print("\n3. Chainable API:")
r = (
    ElectionModel(n_voters=10000, seed=42)
    .with_system("PR")
    .with_allocation("sainte_lague")
    .run_election()
)
print(f"   System: {r['system']}")
print(f"   Gallagher: {r['gallagher']:.2f}")

# Test 4: Config
print("\n4. Config-based:")
config = Config(n_voters=10000, electoral_system="PR", threshold=0.05, seed=42)
model = ElectionModel.from_config(config)
print(f"   Threshold: {model.threshold}")

print("\n=== All API tests passed! ===")
