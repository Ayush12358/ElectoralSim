"""
ElectoralSim Stress Test

Tests the system at various scales to find performance limits.
"""

import time
import sys
import gc
import numpy as np

# Ensure we can import from the project
sys.path.insert(0, ".")


def format_time(seconds: float) -> str:
    """Format time nicely."""
    if seconds < 1:
        return f"{seconds*1000:.1f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    else:
        return f"{seconds/60:.1f} min"


def format_memory(bytes_val: int) -> str:
    """Format memory nicely."""
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024**2:
        return f"{bytes_val/1024:.1f} KB"
    elif bytes_val < 1024**3:
        return f"{bytes_val/1024**2:.1f} MB"
    else:
        return f"{bytes_val/1024**3:.2f} GB"


def get_memory_usage():
    """Get current memory usage."""
    try:
        import psutil

        process = psutil.Process()
        return process.memory_info().rss
    except ImportError:
        return 0


def stress_test_elections():
    """Test election performance at various scales."""
    from electoral_sim import ElectionModel

    print("=" * 70)
    print("STRESS TEST: Election Model")
    print("=" * 70)

    scales = [
        (10_000, 10, "Small"),
        (100_000, 50, "Medium"),
        (500_000, 100, "Large"),
        (1_000_000, 200, "Very Large"),
        (2_000_000, 300, "Huge"),
        (5_000_000, 500, "Massive"),
    ]

    results = []

    for n_voters, n_constituencies, label in scales:
        gc.collect()
        mem_before = get_memory_usage()

        try:
            # Model creation
            start = time.perf_counter()
            model = ElectionModel(
                n_voters=n_voters,
                n_constituencies=n_constituencies,
                seed=42,
            )
            create_time = time.perf_counter() - start

            mem_after_create = get_memory_usage()

            # Warm-up run (JIT compilation)
            if n_voters == 10_000:
                model.run_election()

            # Timed election
            start = time.perf_counter()
            result = model.run_election()
            election_time = time.perf_counter() - start

            mem_after = get_memory_usage()
            mem_used = mem_after - mem_before

            results.append(
                {
                    "label": label,
                    "n_voters": n_voters,
                    "n_constituencies": n_constituencies,
                    "create_time": create_time,
                    "election_time": election_time,
                    "memory_mb": mem_used / 1024**2,
                    "turnout": result["turnout"],
                    "gallagher": result["gallagher"],
                    "success": True,
                }
            )

            print(f"\n{label} ({n_voters:,} voters, {n_constituencies} constituencies):")
            print(f"  Create:   {format_time(create_time)}")
            print(f"  Election: {format_time(election_time)}")
            print(f"  Memory:   {format_memory(mem_used)}")
            print(f"  Turnout:  {result['turnout']:.1%}")
            print(f"  Gallagher: {result['gallagher']:.2f}")

            # Clean up
            del model
            gc.collect()

        except Exception as e:
            results.append(
                {
                    "label": label,
                    "n_voters": n_voters,
                    "success": False,
                    "error": str(e),
                }
            )
            print(f"\n{label} ({n_voters:,} voters): FAILED - {e}")
            break

    return results


def stress_test_batch():
    """Test batch election performance."""
    from electoral_sim import ElectionModel

    print("\n" + "=" * 70)
    print("STRESS TEST: Batch Elections (Monte Carlo)")
    print("=" * 70)

    model = ElectionModel(n_voters=500_000, n_constituencies=100, seed=42)

    # Warm up
    model.run_election()

    batch_sizes = [10, 50, 100, 500]

    for n in batch_sizes:
        gc.collect()
        start = time.perf_counter()
        results = model.run_elections_batch(n_elections=n)
        elapsed = time.perf_counter() - start

        stats = model.get_aggregate_stats(results)

        print(f"\n{n} elections (500K voters each):")
        print(f"  Total time: {format_time(elapsed)}")
        print(f"  Per election: {format_time(elapsed/n)}")
        print(f"  Throughput: {n/elapsed:.1f} elections/sec")
        print(f"  Gallagher: {stats['gallagher_mean']:.2f} ± {stats['gallagher_std']:.2f}")


def stress_test_opinion_dynamics():
    """Test opinion dynamics at scale."""
    from electoral_sim import OpinionDynamics

    print("\n" + "=" * 70)
    print("STRESS TEST: Opinion Dynamics")
    print("=" * 70)

    scales = [
        (10_000, "Small"),
        (50_000, "Medium"),
        (100_000, "Large"),
        (500_000, "Very Large"),
        (1_000_000, "Huge"),
    ]

    for n_agents, label in scales:
        gc.collect()

        try:
            # Network creation
            start = time.perf_counter()
            od = OpinionDynamics(n_agents=n_agents, topology="barabasi_albert", m=3, seed=42)
            create_time = time.perf_counter() - start

            # Initialize opinions
            opinions = od.rng.integers(0, 3, n_agents)

            # Run 50 steps
            start = time.perf_counter()
            for _ in range(50):
                opinions = od.step(opinions, model="noisy_voter", noise_rate=0.01)
            step_time = time.perf_counter() - start

            print(f"\n{label} ({n_agents:,} agents):")
            print(f"  Network creation: {format_time(create_time)}")
            print(f"  50 steps: {format_time(step_time)} ({format_time(step_time/50)}/step)")
            print(f"  Final shares: {od.get_opinion_shares(opinions, 3)}")

            del od
            gc.collect()

        except Exception as e:
            print(f"\n{label} ({n_agents:,} agents): FAILED - {e}")
            break


def stress_test_alternative_voting():
    """Test IRV/STV at scale."""
    from electoral_sim import irv_election, stv_election, generate_rankings

    print("\n" + "=" * 70)
    print("STRESS TEST: Alternative Voting (IRV/STV)")
    print("=" * 70)

    scales = [
        (1_000, 5),
        (10_000, 10),
        (100_000, 15),
        (500_000, 10),
        (1_000_000, 8),
    ]

    for n_voters, n_candidates in scales:
        gc.collect()

        try:
            # Generate rankings
            np.random.seed(42)
            utilities = np.random.randn(n_voters, n_candidates)

            start = time.perf_counter()
            rankings = generate_rankings(utilities)
            rank_time = time.perf_counter() - start

            # IRV
            start = time.perf_counter()
            irv_result = irv_election(rankings, n_candidates)
            irv_time = time.perf_counter() - start

            # STV (3 seats)
            start = time.perf_counter()
            stv_result = stv_election(rankings, n_candidates, n_seats=3)
            stv_time = time.perf_counter() - start

            print(f"\n{n_voters:,} voters, {n_candidates} candidates:")
            print(f"  Ranking gen: {format_time(rank_time)}")
            print(f"  IRV: {format_time(irv_time)} ({len(irv_result['rounds'])} rounds)")
            print(f"  STV: {format_time(stv_time)} (elected: {stv_result['elected']})")

        except Exception as e:
            print(f"\n{n_voters:,} voters: FAILED - {e}")
            break


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " ElectoralSim Stress Test ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Check Numba
    try:
        from electoral_sim.numba_accel import NUMBA_AVAILABLE

        print(f"Numba acceleration: {'✓ ENABLED' if NUMBA_AVAILABLE else '✗ DISABLED'}")
    except Exception:
        print("Numba acceleration: ✗ NOT FOUND")

    # Check memory
    try:
        import psutil

        mem = psutil.virtual_memory()
        print(f"Available memory: {format_memory(mem.available)} / {format_memory(mem.total)}")
    except Exception:
        print("Memory tracking: not available (pip install psutil)")

    print()

    total_start = time.perf_counter()

    # Run tests
    stress_test_elections()
    stress_test_batch()
    stress_test_opinion_dynamics()
    stress_test_alternative_voting()

    total_time = time.perf_counter() - total_start

    print("\n" + "=" * 70)
    print(f"Total stress test time: {format_time(total_time)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
