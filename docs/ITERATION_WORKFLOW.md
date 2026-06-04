# Continuous Iteration Workflow

> Autonomous loop: picks next task from TODO.md → executes `docs/WORKFLOW.md`
> → commits → repeats. Discovery phase when TODO.md is empty.

---

## Loop Algorithm

```
START
  │
  ├─ 1. LOAD TODO.md — parse all unchecked `- [ ]` items
  │
  ├─ 2. SELECT NEXT TASK
  │     Priority: P1 > P2 > P3 > P5
  │     Tiebreaker: smallest scope → fewest deps → lowest effort
  │     Skip: GPU-only, external-machine, pure-research
  │     If no unchecked P1-P3 items → enter DISCOVERY PHASE
  │
  ├─ 3. EXECUTE WORKFLOW → follow docs/WORKFLOW.md Phase 1-6
  │
  ├─ 4. VERIFY
  │     pytest tests/ -q --tb=short   → must pass
  │     ruff check .                  → must pass
  │     black --check .               → must pass
  │     If any fail → fix, re-verify, do NOT proceed
  │
  ├─ 5. COMMIT & PUSH
  │     git add -A
  │     git commit -m "<type>: <description>"
  │     git push
  │
  ├─ 6. MARK COMPLETE in TODO.md (`- [ ]` → `- [x]`)
  │
  └─ 7. LOOP → Step 1
```

---

## 1. LOAD TODO.md

Parse `TODO.md` and extract all unchecked items with their priority:

```
- [ ] **P1** Fix Numba multiprocessing crash
- [ ] **P2** Add data provenance docs
- [ ] **P3** Add dashboard screenshots
- [ ] **P5** Redistricting simulation
```

**Skip conditions:**
- `P5` items — only attempt after all P1-P4 are done
- Items requiring GPU hardware (unless GPU is available)
- Items requiring a separate machine
- Pure research items (read a paper, check other sims) — log as blockers

---

## 2. SELECT NEXT TASK

### Priority Order
1. **P1 Bugs** — anything broken
2. **P1 Docs** — misleading README/docs
3. **P2 Architecture** — refactors, consistency
4. **P2 Docs** — missing documentation
5. **P3** — nice-to-haves
6. **P5** — only when nothing else remains

### Tiebreaker (within same priority)
1. Fewest files touched → single-file first
2. No dependencies → self-contained first
3. Quickest → easy wins first
4. Highest impact → coverage gains before cosmetics

---

## 3. EXECUTE WORKFLOW

Follow `docs/WORKFLOW.md` **Phases 1-6** for the selected task:
1. Intake & Research — read all affected files
2. Plan — design API, plan tests, estimate coverage
3. Implement — write code, wire in, format/lint
4. Test — write tests, run `pytest`, verify coverage
5. Document — TODO.md, docstrings, README
6. Verify & Commit — final checks, commit with stats

---

## 4. VERIFY

All three must pass before committing:

```bash
pytest tests/ -q --tb=short
ruff check electoral_sim/ tests/
black --check electoral_sim/ tests/
```

If any fail: fix → re-verify → do NOT proceed until green.

---

## 5. COMMIT & PUSH

### Commit Format
```
<type>: <imperative description>

<bullet points of what changed>

Tests: <N> passed, 0 failed
```

**Types:** `feat:` (feature), `fix:` (bug), `test:` (tests), `docs:` (docs), `refactor:` (restructure), `chore:` (maintenance)

---

## 6. MARK COMPLETE

After push succeeds:
1. Open `TODO.md`
2. Change `- [ ]` → `- [x]` for the completed item
3. Commit: `chore: mark done`
4. Push

---

## 7. LOOP

Return to Step 1.

---

## DISCOVERY PHASE

Triggered when **no unchecked P1-P3 items remain** in TODO.md.

### 7.1 Coverage Scan
```bash
pytest tests/ --cov=electoral_sim --cov-report=term --tb=no -q
```
- Files below **80%** → add TODO
- Skip: GPU code, Numba JIT (untestable without hardware)

### 7.2 Code Smell Scan
```bash
grep -rn "pass  # Placeholder\|TODO\|FIXME\|HACK\|stub" electoral_sim/ --include="*.py"
```
- Add TODO for each genuine unfinished work

### 7.3 Missing Feature Scan
- Review Feature Status table in README
- Beta items that could become Stable → add TODO
- Experimental items that could become Beta → add TODO

### 7.4 Documentation Gap Scan
- Functions/classes without docstrings → add TODO
- Modules missing from README → add TODO

### 7.5 Dependency Audit
- Check `pyproject.toml` vs actual imports
- Missing declared deps → add TODO
- Unused declared deps → add TODO

### 7.6 Test Quality Scan
- Tests with only `assert X is not None` → add TODO
- Parametrize opportunities → add TODO
- Missing edge cases → add TODO

### 7.7 Generate New TODO Items
Compile findings into TODO.md:
- **P1:** Bugs, broken imports, CI failures
- **P2:** Missing docstrings, <80% coverage, data provenance
- **P3:** Screenshots, CI improvements, code quality
- **P5:** New features, countries, ML integration

### 7.8 Restart
Return to Step 1 with fresh TODO items.

---

## Termination

Pause (don't spin endlessly) when:
1. All remaining items are **P5**
2. Coverage **≥90%** (excluding GPU/Numba)
3. **Three consecutive discovery scans** produce zero new items
4. **Human says stop**

---

## Rollback Strategy

If a commit breaks tests:
1. `git revert <bad-commit>` → push revert
2. Uncheck TODO item: `[x]` → `[ ]`
3. Re-plan and re-attempt

---

## Checkpoint Schedule

After every **5 iterations**:
```bash
git tag checkpoint-$(date +%Y%m%d-%H%M)
git push --tags
```
