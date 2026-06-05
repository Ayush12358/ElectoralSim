# Scripts

Utility and release automation scripts.

## Release Scripts

| Script | Purpose |
|--------|---------|
| `bump_version.py` | Version bump helper (`python scripts/bump_version.py patch\|minor\|major`) |
| `do_release.py` | **One-command release** — calls bump_version, commits, tags, pushes |

For manual build/publish without version bump: use `python -m build && twine upload dist/*`.

## Testing & QA

| Script | Purpose |
|--------|---------|
| `smoke_test_install.py` | Release-blocking smoke test: build sdist in venv, run CLI commands |

## Benchmarks

Performance benchmark scripts have been moved to `benchmarks/`.
