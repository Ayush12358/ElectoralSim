# Scripts

Utility and release automation scripts.

## Release Scripts

| Script | Purpose |
|--------|---------|
| `release.py` | Build and publish to PyPI (`python scripts/release.py test\|publish`) |
| `do_release.py` | One-command release (version bump + build + publish) |
| `bump_version.py` | Version bump helper |
| `release_pypi.bat` | Windows batch: publish to PyPI via `release.py` |
| `release_test.bat` | Windows batch: publish to TestPyPI via `release.py` |

## Testing & QA

| Script | Purpose |
|--------|---------|
| `smoke_test_install.py` | Release-blocking smoke test: build sdist in venv, run CLI commands |

## Benchmarks

Performance benchmark scripts have been moved to `benchmarks/`.
