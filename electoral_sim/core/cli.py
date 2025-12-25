"""
Command-line interface for ElectoralSim

Usage:
    electoral-sim run --voters 100000 --system FPTP
    electoral-sim run --preset india --output results.json
    electoral-sim list-presets
"""

import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        prog="electoral-sim",
        description="Agent-based electoral simulation",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run an election simulation")
    run_parser.add_argument(
        "--voters",
        "-n",
        type=int,
        default=100_000,
        help="Number of voters (default: 100000)",
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
        choices=["FPTP", "PR"],
        default="FPTP",
        help="Electoral system (default: FPTP)",
    )
    run_parser.add_argument(
        "--allocation",
        "-a",
        choices=["dhondt", "sainte_lague"],
        default="dhondt",
        help="PR allocation method (default: dhondt)",
    )
    run_parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        default=0.0,
        help="Electoral threshold 0-1 (default: 0)",
    )
    run_parser.add_argument(
        "--preset",
        "-p",
        choices=["india", "usa", "uk", "germany"],
        help="Use country preset",
    )
    run_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility",
    )
    run_parser.add_argument(
        "--output",
        "-o",
        help="Output file (JSON)",
    )
    run_parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress output",
    )

    # List presets command
    presets_parser = subparsers.add_parser("list-presets", help="List available presets")

    args = parser.parse_args()

    if args.command == "list-presets":
        list_presets()
    elif args.command == "run":
        run_simulation(args)
    else:
        parser.print_help()


def list_presets():
    """List available country presets."""
    from electoral_sim.core.config import PRESETS

    print("Available presets:")
    print("-" * 40)

    presets_info = {
        "india": "543 constituencies, FPTP (Lok Sabha)",
        "usa": "435 districts, FPTP (House)",
        "uk": "650 constituencies, FPTP (Commons)",
        "germany": "299 districts, PR+MMP, 5% threshold",
    }

    for name in PRESETS:
        info = presets_info.get(name, "")
        print(f"  {name:10} - {info}")


def run_simulation(args):
    """Run an election simulation."""
    from electoral_sim import ElectionModel

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
        print(f"System: {model.electoral_system}")
        print("-" * 40)

    # Run election
    results = model.run_election()

    # Display results
    if not args.quiet:
        print("\nResults:")
        print(f"  Turnout: {results['turnout']:.1%}")
        print(f"  Gallagher Index: {results['gallagher']:.2f}")
        print(f"  ENP (votes): {results['enp_votes']:.2f}")
        print(f"  ENP (seats): {results['enp_seats']:.2f}")

        print("\nParty Results:")
        party_names = model.parties.df["name"].to_list()
        for i, name in enumerate(party_names):
            votes = results["vote_counts"][i]
            seats = results["seats"][i]
            share = votes / results["vote_counts"].sum() * 100
            print(f"  {name:15} {votes:>8,} votes ({share:5.1f}%) {seats:>3} seats")

    # Save to file
    if args.output:
        output_data = {
            "system": results["system"],
            "turnout": float(results["turnout"]),
            "gallagher": float(results["gallagher"]),
            "enp_votes": float(results["enp_votes"]),
            "enp_seats": float(results["enp_seats"]),
            "parties": {
                name: {
                    "votes": int(results["vote_counts"][i]),
                    "seats": int(results["seats"][i]),
                }
                for i, name in enumerate(model.parties.df["name"].to_list())
            },
        }

        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)

        if not args.quiet:
            print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
