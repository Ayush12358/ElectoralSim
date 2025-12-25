# Package Maintenance Guide

Exhaustive checklist for maintaining `electoral-sim` as a professional Python package.

---

## 📁 Repository Structure

### ✅ Complete
- [x] `pyproject.toml` — Modern Python packaging
- [x] `README.md` — Project overview with badges
- [x] `LICENSE` — MIT license
- [x] `CHANGELOG.md` — Version history
- [x] `CONTRIBUTING.md` — Contributor guide
- [x] `.gitignore` — Ignore patterns
- [x] `MANIFEST.in` — Source distribution files
- [x] `requirements.txt` — Dependency reference
- [x] `mkdocs.yml` — Documentation config
- [x] `electoral_sim/py.typed` — PEP 561 type marker
- [x] `CODE_OF_CONDUCT.md` — Community standards
- [x] `SECURITY.md` — Vulnerability reporting
- [x] `.github/FUNDING.yml` — Sponsorship info
- [x] `.editorconfig` — Consistent editor settings

---

## 🔧 GitHub Repository Settings

### General (Settings → General)
- [x] Description and topics (tags)
- [ ] Website URL (your docs link)
- [ ] Social preview image

### Branch Protection (Settings → Branches)
- [ ] Add rule for `main`/`master`:
  - [ ] Require status checks to pass
  - [ ] Require branches to be up to date

### Security (Settings → Security)
- [x] Dependabot enabled
- [ ] Enable secret scanning
- [ ] Enable push protection

### Pages (Settings → Pages)
- [x] Source: GitHub Actions
- [x] Enforce HTTPS

---

## ⚙️ GitHub Actions Workflows

### ✅ Complete (7 Workflows)
| Workflow | File | Trigger |
|----------|------|---------|
| Tests | `tests.yml` | Push/PR |
| Lint | `lint.yml` | Push/PR |
| Docs | `docs.yml` | Push to docs/ |
| Publish | `publish.yml` | Release published |
| Release | `release.yml` | Tag push v* |
| Stale | `stale.yml` | Daily (cron) |
| CodeQL | `codeql.yml` | Push/PR + Weekly |

---

## 📦 PyPI Settings

- [x] Published to PyPI
- [x] Trusted publishing configured
- [ ] Enable 2FA on PyPI account

---

## 🔄 Release Process (Automated)

```bash
python scripts/do_release.py patch  # 0.0.1 → 0.0.2
python scripts/do_release.py minor  # 0.0.1 → 0.1.0
python scripts/do_release.py major  # 0.0.1 → 1.0.0
```

---

## 🧪 Testing

```bash
pytest tests/ -v              # Run all tests
pytest tests/ --cov=electoral_sim  # With coverage
```

---

## 📝 Documentation

- [x] MkDocs with Material theme
- [x] GitHub Pages deployment
- [x] API reference docs
- [x] Installation & Quick start guides

---

## 🔍 Code Quality

- [x] `.pre-commit-config.yaml`
- [x] Black formatter
- [x] Ruff linter

```bash
pip install pre-commit
pre-commit install
```

---

## 📊 README Badges (Complete)

- [x] Tests status
- [x] Lint status
- [x] PyPI version
- [x] Python versions
- [x] Downloads
- [x] License
- [x] Documentation
- [x] Code style: black

---

## 📈 Community

- [x] Bug report template
- [x] Feature request template
- [x] Pull request template
- [x] `CODE_OF_CONDUCT.md`
- [x] `SECURITY.md`

---

## 📅 Maintenance Schedule

### Weekly
- Check Dependabot PRs
- Review open issues

### Monthly
- Merge dependency updates
- Consider patch release

### Quarterly
- Feature planning
- Update roadmap

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Release | `python scripts/do_release.py patch` |
| Test | `pytest tests/ -v` |
| Docs | `mkdocs serve` |
| Format | `black electoral_sim/` |
| Lint | `ruff check electoral_sim/` |
| Build | `python scripts/release.py build` |
