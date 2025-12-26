# Package Maintenance Guide

Complete reference for maintaining `electoral-sim` as a professional Python package.

---

## Repository Structure

### Required Files (Complete)
- `pyproject.toml` - Modern Python packaging configuration
- `README.md` - Project overview with badges and examples
- `LICENSE` - Apache License 2.0 file
- `CHANGELOG.md` - Version history following Keep a Changelog format
- `CONTRIBUTING.md` - Contributor guidelines
- `.gitignore` - Version control ignore patterns
- `MANIFEST.in` - Source distribution file inclusion rules
- `requirements.txt` - Dependency reference for pip
- `mkdocs.yml` - MkDocs documentation configuration
- `electoral_sim/py.typed` - PEP 561 type marker for typed package

### Community Files (Complete)
- `CODE_OF_CONDUCT.md` - Contributor Covenant code of conduct
- `SECURITY.md` - Security vulnerability reporting policy
- `.editorconfig` - Editor configuration for consistent style
- `.github/FUNDING.yml` - GitHub Sponsors configuration
- `.github/PULL_REQUEST_TEMPLATE.md` - PR checklist template
- `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report form
- `.github/ISSUE_TEMPLATE/feature_request.md` - Feature request form

---

## GitHub Repository Settings

### General Settings
Go to Settings > General:
- Set repository description and topics/tags
- Add website URL pointing to documentation
- Upload social preview image (1280x640 recommended)
- Disable unused features (wiki, projects) if not using

### Branch Protection Rules
Go to Settings > Branches > Add rule for `master`:
- Require pull request reviews before merging
- Require status checks to pass before merging
  - Select: `test (3.10)`, `test (3.11)`, `test (3.12)`, `lint`
- Require branches to be up to date before merging
- Optionally require signed commits
- Apply rules to administrators

### Security Settings
Go to Settings > Security:
- Enable Dependabot alerts (automatic)
- Enable Dependabot security updates
- Enable secret scanning
- Enable push protection for secrets

### GitHub Pages
Go to Settings > Pages:
- Source: GitHub Actions
- Enforce HTTPS: Enabled
- Custom domain: Optional

### Environments
Go to Settings > Environments:
- Create `pypi` environment for trusted publishing
- Add reviewers if requiring approval for releases

---

## GitHub Actions Workflows

### Current Workflows (7 Total)

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| Tests | `tests.yml` | Push, PR | Run pytest on Python 3.10, 3.11, 3.12 |
| Lint | `lint.yml` | Push, PR | Check code style with Black and Ruff |
| Docs | `docs.yml` | Push to docs/, manual | Build and deploy MkDocs to GitHub Pages |
| Publish | `publish.yml` | Release published | Upload to PyPI via trusted publishing |
| Release | `release.yml` | Tag push (v*) | Create GitHub release and publish to PyPI |
| Stale | `stale.yml` | Daily cron | Auto-close inactive issues after 60+14 days |
| CodeQL | `codeql.yml` | Push, PR, weekly | Security vulnerability scanning |

### Workflow Maintenance
- Review workflow runs weekly for failures
- Update action versions when Dependabot suggests
- Monitor CodeQL findings in Security tab

---

## PyPI Configuration

### Package Settings
At pypi.org/project/electoral-sim/manage/:
- Verify project description renders correctly
- Check project URLs are correct (docs, repo, changelog)
- Add collaborators/maintainers if needed

### Trusted Publishing Setup
At pypi.org/manage/project/electoral-sim/settings/publishing/:
- Add trusted publisher:
  - Owner: `Ayush12358`
  - Repository: `ElectoralSim`
  - Workflow: `release.yml`
  - Environment: `pypi` (optional)

### Account Security
- Enable 2FA on PyPI account
- Use project-scoped API tokens if not using trusted publishing
- Never commit tokens to repository

---

## Release Process

### Automated Release (Recommended)
```bash
# Bump version, commit, tag, and push in one command
python scripts/do_release.py patch   # 0.0.1 -> 0.0.2
python scripts/do_release.py minor   # 0.0.1 -> 0.1.0
python scripts/do_release.py major   # 0.0.1 -> 1.0.0
```

This script automatically:
1. Updates version in `pyproject.toml` and `__init__.py`
2. Adds new section to `CHANGELOG.md`
3. Commits with message `chore: release vX.Y.Z`
4. Creates git tag `vX.Y.Z`
5. Pushes to GitHub with tags
6. GitHub Actions then publishes to PyPI

### Manual Release Steps
If automation fails, follow these steps:
1. Update version in `pyproject.toml` (line 7)
2. Update version in `electoral_sim/__init__.py` (line 9)
3. Update `CHANGELOG.md` with release notes
4. Stage and commit: `git add -A && git commit -m "chore: release v0.0.2"`
5. Create tag: `git tag v0.0.2`
6. Push with tags: `git push origin master --tags`
7. Verify GitHub Actions completes successfully

### Version Numbering (Semantic Versioning)
- MAJOR (1.0.0): Breaking API changes
- MINOR (0.1.0): New features, backward compatible
- PATCH (0.0.1): Bug fixes, backward compatible

---

## Testing

### Local Testing
```bash
# Run all tests
pytest tests/ -v

# Run with short tracebacks
pytest tests/ -v --tb=short

# Stop on first failure
pytest tests/ -x

# Run specific test file
pytest tests/test_integration.py -v

# Run with coverage
pytest tests/ --cov=electoral_sim --cov-report=html
```

### CI Testing Matrix
Tests run on:
- Python 3.10, 3.11, 3.12
- Ubuntu (Linux)
- Dependencies installed from pyproject.toml

### Test Maintenance
- Keep test coverage above 80%
- Update tests when adding new features
- Remove tests for deleted features
- Review test output for deprecation warnings

---

## Documentation

### Local Development
```bash
# Install MkDocs
pip install mkdocs mkdocs-material mkdocstrings[python]

# Serve locally with hot reload
mkdocs serve
# Visit http://127.0.0.1:8000

# Build static site
mkdocs build
# Output in ./site/
```

### Documentation Structure
```
docs/
  index.md                 # Landing page
  installation.md          # Setup guide
  quickstart.md            # Getting started tutorial
  api/                     # API reference
    election_model.md
    behavior_models.md
    electoral_systems.md
    metrics.md
    coalition.md
    opinion_dynamics.md
  presets/                 # Country configurations
    india.md
    countries.md
  advanced/                # Advanced topics
    voter_psychology.md
    performance.md
  MAINTENANCE.md           # This file
```

### Documentation Standards
- Use clear, concise language
- Include code examples for all features
- Keep examples runnable and tested
- Update docs when changing public APIs

---

## Code Quality

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install hooks (run once)
pre-commit install

# Run on all files manually
pre-commit run --all-files
```

### Linting and Formatting
```bash
# Format code with Black
black electoral_sim/

# Lint with Ruff
ruff check electoral_sim/

# Auto-fix linting issues
ruff check electoral_sim/ --fix

# Type checking (optional)
mypy electoral_sim/
```

### Code Style Guidelines
- Line length: 100 characters
- Use type hints for public functions
- Write docstrings for public functions and classes
- Follow PEP 8 naming conventions

---

## Dependency Management

### Updating Dependencies
1. Review Dependabot PRs weekly
2. Test locally before merging: `pip install -e . && pytest tests/`
3. Merge if tests pass
4. Consider releasing patch version after security updates

### Adding New Dependencies
1. Add to `pyproject.toml` under `[project.dependencies]`
2. Specify minimum version: `package>=1.0.0`
3. Update `requirements.txt` for reference
4. Test installation: `pip install -e .`

### Security Auditing
```bash
# Install pip-audit
pip install pip-audit

# Check for vulnerabilities
pip-audit

# Fix vulnerabilities by updating packages
pip-audit --fix
```

---

## Issue and PR Management

### Issue Labels
Create these labels in GitHub:
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested
- `wontfix` - This will not be worked on
- `duplicate` - This issue already exists

### PR Review Checklist
- Code follows style guidelines
- Tests added for new features
- Documentation updated
- CHANGELOG updated for user-facing changes
- CI passes

### Response Time Goals
- Issues: Acknowledge within 48 hours
- PRs: Initial review within 1 week
- Security issues: Acknowledge within 24 hours

---

## Maintenance Schedule

### Weekly Tasks
- [ ] Check GitHub Actions for failures
- [ ] Review and merge Dependabot PRs
- [ ] Respond to new issues
- [ ] Review open PRs

### Monthly Tasks
- [ ] Release patch version if bug fixes accumulated
- [ ] Update documentation for any changes
- [ ] Review CodeQL security findings
- [ ] Check PyPI download statistics

### Quarterly Tasks
- [ ] Plan major features for next release
- [ ] Review and update roadmap in TODO.md
- [ ] Clean up stale branches
- [ ] Review and close stale issues
- [ ] Check for deprecated dependencies

### Yearly Tasks
- [ ] Update Python version support (add new, drop EOL)
- [ ] Review license and copyright year
- [ ] Major version release if breaking changes needed
- [ ] Archive old releases

---

## Troubleshooting

### Build Failures
```bash
# Clean build artifacts
python scripts/release.py clean

# Rebuild
python scripts/release.py build
```

### PyPI Upload Failures
- Check trusted publishing is configured correctly
- Verify tag format is `vX.Y.Z`
- Check PyPI for existing version (can't overwrite)

### Documentation Build Failures
- Check mkdocs.yml syntax
- Verify all linked files exist
- Check markdown syntax errors

### Test Failures
- Run tests locally first
- Check for missing dependencies
- Verify test fixtures are present

---

## Quick Reference

| Task | Command |
|------|---------|
| Run tests | `pytest tests/ -v` |
| Format code | `black electoral_sim/` |
| Lint code | `ruff check electoral_sim/` |
| Build docs | `mkdocs serve` |
| Build package | `python scripts/release.py build` |
| Release patch | `python scripts/do_release.py patch` |
| Release minor | `python scripts/do_release.py minor` |
| Release major | `python scripts/do_release.py major` |
| Security audit | `pip-audit` |
| Update hooks | `pre-commit autoupdate` |
