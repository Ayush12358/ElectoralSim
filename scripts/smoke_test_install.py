#!/usr/bin/env python3

# Copyright 2025-2026 Ayush Joshi
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
Release-blocking smoke test: build sdist, install in clean venv, run CLI.

Verifies that the installed package works correctly — catches packaging
differences (missing files, broken entry points, import errors) that
in-repo imports can hide.

Usage:
    python scripts/smoke_test_install.py

Exit code 0 = all checks passed. Non-zero = failure (blocks release).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command, print it, and return the result."""
    cmd_str = " ".join(cmd)
    print(f"  $ {cmd_str}")
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode})")
        if result.stderr:
            print(f"  stderr: {result.stderr.strip()}")
    return result


def test_help(venv_python: str) -> bool:
    """Run electoral-sim --help and verify output."""
    result = run([venv_python, "-m", "electoral_sim.core.cli", "--help"])
    if result.returncode != 0:
        print("  FAIL: --help returned non-zero exit code")
        return False
    if "usage:" not in (result.stdout + result.stderr).lower():
        print("  FAIL: --help output missing 'usage:'")
        return False
    print("  PASS")
    return True


def test_list_presets(venv_python: str) -> bool:
    """Run electoral-sim list-presets and verify output."""
    result = run([venv_python, "-m", "electoral_sim.core.cli", "list-presets"])
    if result.returncode != 0:
        print("  FAIL: list-presets returned non-zero exit code")
        return False
    output = result.stdout + result.stderr
    for preset in ["india", "usa", "uk", "germany"]:
        if preset not in output.lower():
            print(f"  FAIL: preset '{preset}' not found in list-presets output")
            return False
    print("  PASS")
    return True


def test_run(venv_python: str) -> bool:
    """Run a tiny election and verify it produces valid results."""
    import json

    output_file = tempfile.mktemp(suffix=".json")
    try:
        result = run(
            [
                venv_python,
                "-m",
                "electoral_sim.core.cli",
                "run",
                "--voters",
                "500",
                "--constituencies",
                "3",
                "--seed",
                "42",
                "--output",
                output_file,
            ]
        )
        if result.returncode != 0:
            print("  FAIL: run returned non-zero exit code")
            return False

        with open(output_file) as f:
            data = json.load(f)
        turnout = data.get("results", {}).get("turnout", -1)
        if turnout < 0 or turnout > 1:
            print(f"  FAIL: invalid or missing turnout: {turnout}")
            return False
        print(f"  PASS (turnout={turnout:.1%})")
        return True
    finally:
        Path(output_file).unlink(missing_ok=True)


def main() -> int:
    print("=" * 60)
    print("ElectoralSim Installed-Package Smoke Test")
    print("=" * 60)

    # Step 1: Build sdist
    print("\n[1/4] Building sdist...")
    result = run([sys.executable, "-m", "build", "--sdist", str(REPO_ROOT)])
    if result.returncode != 0:
        print("FAIL: Could not build sdist. Install 'build' with: pip install build")
        return 1

    # Find the built sdist
    dist_dir = REPO_ROOT / "dist"
    sdists = sorted(dist_dir.glob("electoral_sim-*.tar.gz"), reverse=True)
    if not sdists:
        print("FAIL: No sdist .tar.gz found in dist/")
        return 1
    sdist = sdists[0]
    print(f"  Built: {sdist.name}")

    # Step 2: Create temporary venv
    print("\n[2/4] Creating temporary venv...")
    tmpdir = tempfile.mkdtemp(prefix="electoral-smoke-")
    venv_dir = Path(tmpdir) / "venv"
    result = run([sys.executable, "-m", "venv", str(venv_dir), "--clear"])
    if result.returncode != 0:
        print("FAIL: Could not create venv")
        shutil.rmtree(tmpdir, ignore_errors=True)
        return 1

    venv_python = str(venv_dir / "bin" / "python")
    venv_pip = str(venv_dir / "bin" / "pip")

    # Step 3: Install sdist in venv
    print("\n[3/4] Installing sdist in venv...")
    result = run([venv_pip, "install", str(sdist)])
    if result.returncode != 0:
        print("FAIL: pip install of sdist failed")
        shutil.rmtree(tmpdir, ignore_errors=True)
        return 1
    print(f"  Installed into {venv_dir}")

    # Step 4: Run CLI smoke tests
    print("\n[4/4] Running CLI smoke tests...")

    failures = 0
    print("  electoral-sim --help:")
    if not test_help(venv_python):
        failures += 1

    print("  electoral-sim list-presets:")
    if not test_list_presets(venv_python):
        failures += 1

    print("  electoral-sim run --voters 500 --constituencies 3:")
    if not test_run(venv_python):
        failures += 1

    # Cleanup
    shutil.rmtree(tmpdir, ignore_errors=True)

    print("\n" + "=" * 60)
    if failures == 0:
        print("ALL CHECKS PASSED — package is release-ready.")
        print("=" * 60)
        return 0
    else:
        print(f"{failures} CHECK(S) FAILED — package is NOT release-ready.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
