#!/usr/bin/env python
"""
One-command release script.

Usage:
    python scripts/do_release.py patch   # 0.0.1 -> 0.0.2, commit, tag, push
    python scripts/do_release.py minor   # 0.0.1 -> 0.1.0, commit, tag, push
    python scripts/do_release.py major   # 0.0.1 -> 1.0.0, commit, tag, push
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def run(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    print(f"  $ {cmd}")
    return subprocess.run(cmd, shell=True, cwd=ROOT, check=check)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    bump_type = sys.argv[1].lower()

    # 1. Bump version
    print("\n[1] Bump version")
    run(f"python scripts/bump_version.py {bump_type}")

    # Get new version
    import re
    pyproject = (ROOT / "pyproject.toml").read_text()
    match = re.search(r'version = "(.+?)"', pyproject)
    new_version = match.group(1) if match else "unknown"

    # 2. Stage all changes
    print("\n[2] Stage changes")
    run("git add -A")

    # 3. Commit
    print("\n[3] Commit")
    run(f'git commit -m "chore: release v{new_version}"')

    # 4. Tag
    print("\n[4] Create tag")
    run(f"git tag v{new_version}")

    # 5. Push
    print("\n[5] Push to GitHub")
    run("git push origin master --tags")

    print(f"\n[OK] Released v{new_version}!")
    print(f"\nGitHub Actions will now:")
    print(f"   - Create GitHub Release with auto-generated notes")
    print(f"   - Publish to PyPI automatically")
    print(f"\nCheck: https://pypi.org/project/electoral-sim/{new_version}/")


if __name__ == "__main__":
    main()
