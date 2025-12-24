from electoral_sim.presets.india.election import simulate_india_election

print("Running India simulation with real names and NOTA...")
result = simulate_india_election(
    n_voters_per_constituency=500, # Small for speed
    include_nota=True,
    use_real_names=True,
    verbose=False
)

print("\nSample of NOTA contested seats (should have real names):")
for race in result.nota_contested_list[:10]:
    print(f" - {race}")

# Check if some prominent names exist
all_names = []
# We can't easily get the list back from result other than the nota list 
# but we can check if Varanasi is in the list or something like it.

varanasi_found = any("Varanasi" in r for r in result.nota_contested_list)
lucknow_found = any("Lucknow" in r for r in result.nota_contested_list)

print(f"\nVaranasi found in contested: {varanasi_found}")
print(f"Lucknow found in contested: {lucknow_found}")

# Verify manager works directly
from electoral_sim.data.india_pc import get_india_constituencies
manager = get_india_constituencies()
print(f"\nManager Name Test (ID 0): {manager.get_name(0)}") # Should be Varanasi
print(f"Manager Name Test (ID 542): {manager.get_name(542)}")
