import json
import sys

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

    except (ValueError, OSError) as e:
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
    except (ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def preset_info(args):
    """Display metadata for a specific preset."""
    from electoral_sim.core.config import PRESETS, PRESET_PROVENANCE

    preset = args.preset.lower()
    if preset not in PRESETS:
        print(f"Error: Unknown preset '{args.preset}'. Run 'electoral-sim list-presets'.", file=sys.stderr)
        sys.exit(1)

    prov = PRESET_PROVENANCE.get(preset, {})
    config = PRESETS[preset](n_voters=100)

    print(f"Preset: {preset}")
    print(f"  Electoral System: {prov.get('electoral_system', 'N/A')}")
    print(f"  Calibration: {prov.get('calibration', 'N/A')}")
    print(f"  Source: {prov.get('source', 'N/A')}")
    print(f"  Parties: {config.n_parties}")
    print(f"  Constituencies: {config.n_constituencies}")


def validate_preset(args):
    """Validate a preset configuration by running a small simulation."""
    from electoral_sim import ElectionModel
    from electoral_sim.core.config import PRESETS

    preset = args.preset.lower()
    if preset not in PRESETS:
        print(f"Error: Unknown preset '{args.preset}'.", file=sys.stderr)
        sys.exit(1)

    try:
        model = ElectionModel.from_preset(preset, n_voters=500)
        result = model.run_election()
        turnout = result["turnout"] if isinstance(result, dict) else result.turnout
        print(f"Preset '{preset}' validated successfully.")
        print(f"  Turnout: {turnout:.1%}")
        print(f"  Gallagher: {result['gallagher']:.2f}" if isinstance(result, dict) else f"  Gallagher: {result.gallagher:.2f}")
    except Exception as e:
        print(f"Validation failed for '{preset}': {e}", file=sys.stderr)
        sys.exit(1)

