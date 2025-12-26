# Copyright 2025 Ayush Maurya
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Command-line interface for ElectoralSim

Usage:
    electoral-sim run --voters 100000 --system FPTP
    electoral-sim run --preset india --output results.json
    electoral-sim batch --config batch_config.json
    electoral-sim list-presets
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="electoral-sim",
        description="High-performance agent-based electoral simulation toolkit",
        epilog="For more information, visit: https://github.com/Ayush12358/ElectoralSim",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.0.2")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # =========================================================================
    # RUN COMMAND - Single simulation
    # =========================================================================
    run_parser = subparsers.add_parser(
        "run",
        help="Run a single election simulation",
        description="Run an electoral simulation with customizable parameters",
        epilog="""
Examples:
  # Basic simulation
  electoral-sim run --voters 50000 --constituencies 10

  # Use country preset
  electoral-sim run --preset india --voters 100000

  # Proportional representation with threshold
  electoral-sim run --system PR --allocation sainte_lague --threshold 0.05

  # Save results to file
  electoral-sim run --preset germany --output results.json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    run_parser.add_argument(
        "--voters",
        "-n",
        type=int,
        default=100_000,
        help="Number of voters (default: 100,000)",
    )
    run_parser.add_argument(
        "--constituencies",
        "-c",
        type=int,
        default=10,
        help="Number of constituencies (default: 10)",
    )
    run_parser.add_argument(
        "--system",
        "-s",
        choices=["FPTP", "PR", "IRV", "STV"],
        default="FPTP",
        help="Electoral system: FPTP (first-past-the-post), PR (proportional representation), IRV (instant runoff), STV (single transferable vote) (default: FPTP)",
    )
    run_parser.add_argument(
        "--allocation",
        "-a",
        choices=["dhondt", "sainte_lague", "hare", "droop"],
        default="dhondt",
        help="PR allocation method (default: dhondt)",
    )
    run_parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        default=0.0,
        help="Electoral threshold 0-1, e.g., 0.05 for 5%% (default: 0)",
    )
    run_parser.add_argument(
        "--preset",
        "-p",
        choices=[
            "india",
            "usa",
            "uk",
            "germany",
            "france",
            "japan",
            "brazil",
            "australia_house",
            "australia_senate",
            "south_africa",
            "eu",
        ],
        help="Use country/region preset (overrides other parameters)",
    )
    run_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility",
    )
    run_parser.add_argument(
        "--output",
        "-o",
        help="Output file path (JSON format)",
    )
    run_parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress console output",
    )

    # =========================================================================
    # BATCH COMMAND - Multiple simulations with parameter sweeps
    # =========================================================================
    batch_parser = subparsers.add_parser(
        "batch",
        help="Run batch simulations with parameter sweeps",
        description="Execute multiple simulations with varying parameters for sensitivity analysis",
        epilog="""
Examples:
  # Run batch from config file
  electoral-sim batch --config batch_config.json --output results.csv

  # Quick parameter sweep
  electoral-sim batch --voters 10000,50000,100000 --system FPTP,PR --runs 10

Config file format (JSON):
  {
    "parameters": {
      "n_voters": [10000, 50000, 100000],
      "temperature": [0.3, 0.5, 0.7],
      "economic_growth": [-0.02, 0.0, 0.02]
    },
    "fixed_params": {
      "n_constituencies": 10,
      "electoral_system": "FPTP"
    },
    "n_runs_per_config": 5,
    "n_jobs": 4
  }
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    batch_parser.add_argument(
        "--config",
        help="JSON configuration file for batch run",
    )
    batch_parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output file (CSV, Parquet, or JSON)",
    )
    batch_parser.add_argument(
        "--summary",
        help="Optional summary statistics output file",
    )
    batch_parser.add_argument(
        "--jobs",
        "-j",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1)",
    )
    batch_parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress progress output",
    )

    # =========================================================================
    # LIST-PRESETS COMMAND
    # =========================================================================
    presets_parser = subparsers.add_parser(
        "list-presets",
        help="List all available country/region presets",
        description="Display information about built-in electoral system presets",
    )

    args = parser.parse_args()

    if args.command == "list-presets":
        list_presets()
    elif args.command == "run":
        run_simulation(args)
    elif args.command == "batch":
        run_batch(args)
    else:
        parser.print_help()


def list_presets():
    """List all available country presets with details."""
    from electoral_sim.core.config import PRESETS

    print("=" * 70)
    print("Available Electoral System Presets")
    print("=" * 70)

    presets_info = {
        "india": "543 constituencies, FPTP, 17 parties (Lok Sabha)",
        "usa": "435 districts, FPTP, 2 parties (House of Representatives)",
        "uk": "650 constituencies, FPTP, 5+ parties (House of Commons)",
        "germany": "299 districts, MMP (PR), 5% threshold, 6 parties (Bundestag)",
        "france": "577 constituencies, Two-round system, 5 parties (National Assembly)",
        "japan": "289 constituencies, Mixed system, 2% threshold (House of Representatives)",
        "brazil": "513 seats, Open-list PR, 8 parties (Chamber of Deputies)",
        "australia_house": "151 electorates, IRV (preferential voting), 5 parties",
        "australia_senate": "76 seats, STV (proportional), 5 parties",
        "south_africa": "400 seats, Closed-list PR, 1.5% threshold, 8 parties",
        "eu": "720 MEPs, 27 member states, D'Hondt allocation (EU Parliament)",
    }

    for name in sorted(PRESETS.keys()):
        info = presets_info.get(name, "Electoral system preset")
        print(f"\n  {name}")
        print(f"  {'-' * len(name)}")
        print(f"  {info}")

    print("\n" + "=" * 70)
    print(f"Total: {len(PRESETS)} presets available")
    print("=" * 70)


def run_simulation(args):
    """Run a single election simulation."""
    from electoral_sim import ElectionModel

    try:
        # Create model
        if args.preset:
            model = ElectionModel.from_preset(
                args.preset,
                n_voters=args.voters,
                seed=args.seed,
            )
            if not args.quiet:
                print(f"Using preset: {args.preset}")
        else:
            model = ElectionModel(
                n_voters=args.voters,
                n_constituencies=args.constituencies,
                electoral_system=args.system,
                allocation_method=args.allocation,
                threshold=args.threshold,
                seed=args.seed,
            )

        if not args.quiet:
            print(f"Voters: {len(model.voters):,}")
            print(f"Parties: {len(model.parties)}")
            print(f"Constituencies: {model.n_constituencies}")
            print(f"System: {model.electoral_system}")
            print("-" * 60)

        # Run election
        results = model.run_election()

        # Display results
        if not args.quiet:
            print("\nElection Results:")
            print("-" * 60)
            print(f"  Turnout:         {results['turnout']:.1%}")
            print(f"  Gallagher Index: {results['gallagher']:.2f}")
            print(f"  ENP (votes):     {results['enp_votes']:.2f}")
            print(f"  ENP (seats):     {results['enp_seats']:.2f}")

            print("\nParty Results:")
            print("-" * 60)
            print(f"{'Party':<20} {'Votes':>12} {'Share':>8} {'Seats':>8}")
            print("-" * 60)

            party_names = model.parties.df["name"].to_list()
            for i, name in enumerate(party_names):
                votes = results["vote_counts"][i]
                seats = results["seats"][i]
                share = votes / results["vote_counts"].sum() * 100
                print(f"{name:<20} {votes:>12,} {share:>7.1f}% {seats:>8}")

        # Save to file
        if args.output:
            output_data = {
                "metadata": {
                    "system": results["system"],
                    "voters": len(model.voters),
                    "constituencies": model.n_constituencies,
                },
                "results": {
                    "turnout": float(results["turnout"]),
                    "gallagher": float(results["gallagher"]),
                    "enp_votes": float(results["enp_votes"]),
                    "enp_seats": float(results["enp_seats"]),
                },
                "parties": {
                    name: {
                        "votes": int(results["vote_counts"][i]),
                        "seats": int(results["seats"][i]),
                        "vote_share": float(
                            results["vote_counts"][i] / results["vote_counts"].sum()
                        ),
                    }
                    for i, name in enumerate(model.parties.df["name"].to_list())
                },
            }

            with open(args.output, "w") as f:
                json.dump(output_data, f, indent=2)

            if not args.quiet:
                print(f"\nResults saved to: {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def run_batch(args):
    """Run batch simulations with parameter sweeps."""
    from electoral_sim import ElectionModel
    from electoral_sim.analysis import BatchRunner, ParameterSweep

    try:
        if not args.config:
            print("Error: --config is required for batch command", file=sys.stderr)
            sys.exit(1)

        # Load configuration
        with open(args.config) as f:
            config = json.load(f)

        # Create parameter sweep
        sweep = ParameterSweep(
            parameters=config.get("parameters", {}),
            fixed_params=config.get("fixed_params", {}),
            sweep_type=config.get("sweep_type", "grid"),
            n_samples=config.get("n_samples", 100),
        )

        # Create batch runner
        runner = BatchRunner(
            model_class=ElectionModel,
            parameter_sweep=sweep,
            n_runs_per_config=config.get("n_runs_per_config", 1),
            n_jobs=args.jobs,
            election_kwargs=config.get("election_kwargs", {}),
            seed=config.get("seed"),
            verbose=not args.quiet,
        )

        # Run batch
        results_df = runner.run()

        # Export results
        runner.export_results(args.output)

        # Export summary if requested
        if args.summary:
            runner.export_summary(args.summary)

        if not args.quiet:
            print(f"\n{'=' * 60}")
            print("Batch run complete!")
            print(f"  Configurations: {len(sweep)}")
            print(f"  Total runs: {len(results_df)}")
            print(f"  Results: {args.output}")
            if args.summary:
                print(f"  Summary: {args.summary}")
            print(f"{'=' * 60}")

    except FileNotFoundError:
        print(f"Error: Config file not found: {args.config}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
