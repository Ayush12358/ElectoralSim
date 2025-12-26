"""
Batch Runner Example - Demonstrates parameter sweeping and parallel execution

This example shows how to use BatchRunner to run multiple simulations
with varying parameters and analyze the results.
"""

from electoral_sim import ElectionModel
from electoral_sim.analysis import BatchRunner, ParameterSweep
import polars as pl


def main():
    print("=" * 60)
    print("ElectoralSim - Batch Runner Demo")
    print("=" * 60)

    # Define parameter sweep
    sweep = ParameterSweep(
        parameters={
            "n_voters": [10_000, 50_000],
            "temperature": [0.3, 0.5, 0.7],
            "economic_growth": [-0.02, 0.0, 0.02],
            "electoral_system": ["FPTP", "PR"],
        },
        fixed_params={"n_constituencies": 10, "seed": 42},
        sweep_type="grid",  # Try all combinations
    )

    print(f"\nParameter Sweep: {len(sweep)} configurations")
    print(f"Parameters varying: {list(sweep.parameters.keys())}")

    # Create batch runner
    runner = BatchRunner(
        model_class=ElectionModel,
        parameter_sweep=sweep,
        n_runs_per_config=5,  # 5 Monte Carlo runs per config
        n_jobs=4,  # Parallel execution with 4 workers
        seed=42,
        verbose=True,
    )

    # Run simulations
    print("\nExecuting batch run...")
    results_df = runner.run()

    # Show sample results
    print("\n" + "=" * 60)
    print("Sample Results (first 5 runs):")
    print("=" * 60)
    print(
        results_df.select(
            [
                "config_idx",
                "run_idx",
                "n_voters",
                "temperature",
                "economic_growth",
                "electoral_system",
                "turnout",
                "gallagher",
            ]
        ).head()
    )

    # Get summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics:")
    print("=" * 60)
    summary = runner.get_summary_stats()
    print(
        summary.select(
            [
                "config_idx",
                "n_voters",
                "temperature",
                "electoral_system",
                "turnout_mean",
                "gallagher_mean",
                "enp_votes_mean",
            ]
        ).head(10)
    )

    # Export results
    runner.export_results("batch_results.csv")
    runner.export_summary("batch_summary.csv")

    print("\n" + "=" * 60)
    print("Results exported to:")
    print("  - batch_results.csv (all runs)")
    print("  - batch_summary.csv (aggregated stats)")
    print("=" * 60)

    # Example analysis: Compare FPTP vs PR
    print("\n" + "=" * 60)
    print("Analysis: FPTP vs PR (average across all configs)")
    print("=" * 60)

    comparison = results_df.group_by("electoral_system").agg(
        [
            pl.col("turnout").mean().alias("avg_turnout"),
            pl.col("gallagher").mean().alias("avg_gallagher"),
            pl.col("enp_votes").mean().alias("avg_enp_votes"),
            pl.col("enp_seats").mean().alias("avg_enp_seats"),
        ]
    )
    print(comparison)


if __name__ == "__main__":
    main()
