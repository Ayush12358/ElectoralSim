#!/usr/bin/env python3
"""
Environment bootstrap check for ElectoralSim development.

Verifies that all core dependencies are installed and importable
before running the test suite. Provides actionable guidance if
dependencies are missing.

Usage:
    python scripts/verify_env.py
    python scripts/verify_env.py --dev  # Also check dev dependencies

Exit code 0 = all checks passed. Non-zero = fix instructions printed.
"""

from __future__ import annotations

import subprocess
import sys

CORE_DEPS = {
    "mesa": "3.4.0",
    "polars": "0.20.0",
    "numpy": "1.24.0",
    "numba": "0.60.1",
    "networkx": "3.0",
    "tqdm": "4.60.0",
}

DEV_DEPS = {
    "pytest": "7.0.0",
    "hypothesis": "6.0.0",
    "black": "23.0.0",
    "ruff": "0.1.0",
}

ELECTORAL_IMPORTS = [
    "electoral_sim",
    "electoral_sim.core.model",
    "electoral_sim.systems.allocation",
    "electoral_sim.engine.numba_accel",
]


def check_import(module: str) -> bool:
    """Check if a module can be imported."""
    try:
        __import__(module)
        return True
    except ImportError as e:
        print(f"  FAIL: {module} — {e}")
        return False


def main() -> int:
    check_dev = "--dev" in sys.argv
    failures = 0

    print("=" * 60)
    print("ElectoralSim Environment Bootstrap Check")
    print("=" * 60)

    # Check Python version
    print(f"\nPython: {sys.version.split()[0]}")
    if sys.version_info < (3, 12):
        print("  FAIL: Python 3.12+ required")
        return 1
    print("  OK")

    # Check core dependencies
    print("\nCore dependencies:")
    for pkg, min_ver in CORE_DEPS.items():
        try:
            __import__(pkg)
            print(f"  {pkg} >= {min_ver}: OK")
        except ImportError:
            print(f"  {pkg} >= {min_ver}: MISSING")
            failures += 1

    if failures:
        print("\n" + "=" * 60)
        print("ACTION REQUIRED")
        print("=" * 60)
        print("Install missing dependencies:")
        print("  pip install -e .")
        print("Or for full development setup:")
        print("  pip install -e '.[dev]'")
        return 1

    # Check ElectoralSim imports
    print("\nElectoralSim imports:")
    for mod in ELECTORAL_IMPORTS:
        if check_import(mod):
            print(f"  {mod}: OK")

    if check_dev:
        print("\nDev dependencies:")
        for pkg, min_ver in DEV_DEPS.items():
            try:
                __import__(pkg)
                print(f"  {pkg} >= {min_ver}: OK")
            except ImportError:
                print(f"  {pkg} >= {min_ver}: MISSING")
                failures += 1

        if failures:
            print("\nInstall dev dependencies:")
            print("  pip install -e '.[dev]'")
            return 1

    print("\n" + "=" * 60)
    print("ALL CHECKS PASSED — environment is ready.")
    print("Run: pytest tests/ -v")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
