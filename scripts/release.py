#!/usr/bin/env python
"""
Build and publish script for electoral-sim package.

Usage:
    python scripts/release.py build      # Build package only
    python scripts/release.py test       # Upload to TestPyPI
    python scripts/release.py publish    # Upload to PyPI
    python scripts/release.py all        # Build + publish to PyPI
"""

import subprocess
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"


def clean():
    """Remove build artifacts."""
    print("🧹 Cleaning build artifacts...")
    dirs_to_remove = [
        DIST,
        ROOT / "build",
        ROOT / "electoral_sim.egg-info",
    ]
    for d in dirs_to_remove:
        if d.exists():
            shutil.rmtree(d)
            print(f"  Removed {d.name}/")
    
    # Remove __pycache__ directories
    for pycache in ROOT.rglob("__pycache__"):
        shutil.rmtree(pycache)
    print("  Removed __pycache__ directories")


def build():
    """Build source distribution and wheel."""
    clean()
    print("\n📦 Building package...")
    result = subprocess.run(
        [sys.executable, "-m", "build"],
        cwd=ROOT,
        capture_output=False
    )
    if result.returncode != 0:
        print("❌ Build failed!")
        sys.exit(1)
    
    # List built files
    print("\n✅ Built packages:")
    for f in DIST.iterdir():
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name} ({size_kb:.1f} KB)")


def upload(repository: str = "pypi"):
    """Upload to PyPI or TestPyPI."""
    if not DIST.exists() or not list(DIST.glob("*.whl")):
        print("No packages found. Run 'build' first.")
        sys.exit(1)
    
    print(f"\n🚀 Uploading to {repository}...")
    
    cmd = [sys.executable, "-m", "twine", "upload"]
    if repository == "testpypi":
        cmd.extend(["--repository", "testpypi"])
    cmd.append("dist/*")
    
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"❌ Upload to {repository} failed!")
        sys.exit(1)
    
    if repository == "testpypi":
        print("\n✅ Published to TestPyPI!")
        print("   https://test.pypi.org/project/electoral-sim/")
        print("\n   Test install with:")
        print("   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ electoral-sim")
    else:
        print("\n✅ Published to PyPI!")
        print("   https://pypi.org/project/electoral-sim/")
        print("\n   Install with:")
        print("   pip install electoral-sim")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "clean":
        clean()
    elif command == "build":
        build()
    elif command == "test":
        build()
        upload("testpypi")
    elif command == "publish":
        build()
        upload("pypi")
    elif command == "all":
        build()
        upload("pypi")
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
