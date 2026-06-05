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

    parser.add_argument("--version", action="version", version="%(prog)s 0.2.0")

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
        choices=["FPTP", "PR"],
        default="FPTP",
        help="Electoral system: FPTP (first-past-the-post) or PR (proportional representation) (default: FPTP). IRV/STV not yet wired into model.",
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

    info_parser = subparsers.add_parser(
        "preset-info",
        help="Show metadata for a specific preset",
    )
    info_parser.add_argument("preset", help="Preset name (e.g., india, germany)")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a preset configuration",
    )
    validate_parser.add_argument("--preset", "-p", required=True, help="Preset to validate")
    validate_parser.add_argument("--year", type=int, help="Election year for validation data")

    args = parser.parse_args()

    if args.command == "list-presets":
        from electoral_sim.core._cli_commands import list_presets

        list_presets()
    elif args.command == "preset-info":
        from electoral_sim.core._cli_commands import preset_info

        preset_info(args)
    elif args.command == "validate":
        from electoral_sim.core._cli_commands import validate_preset

        validate_preset(args)
    elif args.command == "run":
        from electoral_sim.core._cli_commands import run_simulation

        run_simulation(args)
    elif args.command == "batch":
        from electoral_sim.core._cli_commands import run_batch

        run_batch(args)
    else:
        parser.print_help()


from electoral_sim.core._cli_commands import list_presets, preset_info, run_batch, run_simulation, validate_preset  # noqa: E402, F401
