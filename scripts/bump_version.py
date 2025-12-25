#!/usr/bin/env python
"""
Version bump script for electoral-sim.

Usage:
    python scripts/bump_version.py patch   # 0.0.1 -> 0.0.2
    python scripts/bump_version.py minor   # 0.0.1 -> 0.1.0
    python scripts/bump_version.py major   # 0.0.1 -> 1.0.0
    python scripts/bump_version.py 0.2.0   # Set specific version
"""

import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "electoral_sim" / "__init__.py"
CHANGELOG = ROOT / "CHANGELOG.md"


def get_current_version() -> str:
    """Read current version from pyproject.toml."""
    content = PYPROJECT.read_text()
    match = re.search(r'version = "(.+?)"', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in pyproject.toml")


def bump_version(current: str, bump_type: str) -> str:
    """Calculate new version."""
    if re.match(r"^\d+\.\d+\.\d+$", bump_type):
        return bump_type  # Explicit version
    
    parts = list(map(int, current.split(".")))
    
    if bump_type == "major":
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif bump_type == "minor":
        parts[1] += 1
        parts[2] = 0
    elif bump_type == "patch":
        parts[2] += 1
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")
    
    return ".".join(map(str, parts))


def update_file(path: Path, pattern: str, replacement: str) -> None:
    """Update version in a file."""
    content = path.read_text()
    new_content = re.sub(pattern, replacement, content)
    path.write_text(new_content)
    print(f"  Updated {path.name}")


def update_changelog(new_version: str) -> None:
    """Add new version section to changelog."""
    content = CHANGELOG.read_text()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Add new version header after the title section
    new_section = f"\n## [{new_version}] - {today}\n\n### Changed\n- Version bump\n"
    
    # Insert after the first ## section marker pattern
    if f"## [{new_version}]" not in content:
        # Find the first version section and insert before it
        match = re.search(r"\n## \[", content)
        if match:
            pos = match.start()
            content = content[:pos] + new_section + content[pos:]
            CHANGELOG.write_text(content)
            print(f"  Updated CHANGELOG.md")
        else:
            print("  Warning: Could not update CHANGELOG.md automatically")
    else:
        print(f"  CHANGELOG.md already has version {new_version}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    bump_type = sys.argv[1].lower()
    current = get_current_version()
    new_version = bump_version(current, bump_type)
    
    print(f"\n📦 Bumping version: {current} → {new_version}\n")
    
    # Update pyproject.toml
    update_file(
        PYPROJECT,
        r'version = ".+?"',
        f'version = "{new_version}"'
    )
    
    # Update __init__.py
    update_file(
        INIT,
        r'__version__ = ".+?"',
        f'__version__ = "{new_version}"'
    )
    
    # Update changelog
    update_changelog(new_version)
    
    print(f"\n✅ Version bumped to {new_version}")
    print(f"\nNext steps:")
    print(f"  1. Review and update CHANGELOG.md with actual changes")
    print(f"  2. git add -A && git commit -m 'chore: release v{new_version}'")
    print(f"  3. git tag v{new_version}")
    print(f"  4. git push origin master --tags")
    print(f"  5. Create GitHub Release → auto-publishes to PyPI")


if __name__ == "__main__":
    main()
