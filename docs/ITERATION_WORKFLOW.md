# Continuous Iteration Workflow

> Autonomous loop that picks the next task from TODO.md, executes
> `docs/WORKFLOW.md` for it, commits, and repeats.

---

## Loop Algorithm

```
START
  │
  ├─ 1. LOAD TODO.md
  │     Parse all unchecked items `- [ ]`
  │
  ├─ 2. SELECT NEXT TASK
  │     Priority: P1 > P2 > P3 > P5
  │     Within same priority: fewest dependencies → easiest → smallest scope
  │     If none unchecked → enter DISCOVERY PHASE
  │
  ├─ 3. EXECUTE WORKFLOW
  │     Follow docs/WORKFLOW.md Phase 1-6 for the selected task
  │
  ├─ 4. VERIFY
  │     pytest tests/ -q --tb=short   → must pass
  │     ruff check .                  → must pass
  │     black --check .               → must pass
  │     If any fail → fix, re-verify, do NOT proceed
  │
  ├─ 5. COMMIT & PUSH
  │     git add -A
  │     git commit -m "<type>: <task description>"
  │     git push
  │
  ├─ 6. MARK COMPLETE
  │     Update TODO.md: `- [ ]` → `- [x]` for completed item
  │     Commit: "chore: check off completed TODO item"
  │
  └─ 7. LOOP → Step 1
```

---

## 1. LOAD TODO.md

Parse `TODO.md` and extract all unchecked items with their priority:

```
- [ ] **P1** Fix Numba multiprocessing crash in BatchRunner
- [ ] **P2** Add data provenance docs for country presets
- [ ] **P3** Add dashboard screenshots to README
- [ ] **P5** Redistricting/Gerrymandering simulation
```

**Skip conditions:**
- Items marked `P5` should only be attempted after all P1-P4 are done
- Items requiring external hardware (CuPy GPU testing) should be **skipped** unless GPU is available
- Items requiring another machine (API testing on separate machine) should be **skipped**
- Items involving research only (read a paper, check other sims) should be **logged as blockers** and skipped

---

## 2. SELECT NEXT TASK

### Priority Order
1. **P1 Bugs** (anything broken)
2. **P1 Docs** (anything misleading in README/docs)
3. **P2 Architecture** (refactors, consistency)
4. **P2 Docs** (missing documentation)
5. **P3 Nice-to-have** (screenshots, CI improvements)
6. **P5 Research** (only when nothing else remains)

### Tiebreaker (within same priority)
1. **Smallest scope** → single-file changes before multi-file
2. **No dependencies** → self-contained before dependent
3. **Lowest effort** → quick wins first
4. **Highest impact** → coverage gains before cosmetic

### Example Selection
```
Input TODO:
  - [ ] P1 Fix Numba multiprocessing crash        ← SELECT (P1, bug)
  - [ ] P1 Add citations for papers               ← skip (research)
  - [ ] P2 Add data provenance docs               ← later
  - [ ] P5 Redistricting simulation               ← skip (P5)

→ Pick: "Fix Numba multiprocessing crash"
```

---

## 3. EXECUTE WORKFLOW

Follow `docs/WORKFLOW.md` **Phase 1 through Phase 6** for the selected task.

Key constraints:
- **Read** all affected files before writing a single line
- **Plan** the implementation before coding
- **Test** with `pytest` after every file change, not just at the end
- **Keep commits small** — one logical change per commit

---

## 4. VERIFY

After completing the workflow, run the full verification suite:

```bash
pytest tests/ -q --tb=short
ruff check electoral_sim/ tests/
black --check electoral_sim/ tests/
```

**Gate:** All three must pass. If any fail:
1. Fix the issue
2. Re-run the failing check
3. Do NOT proceed to commit until green

---

## 5. COMMIT & PUSH

### Commit Format
```
<type>: <imperative description>

<2-3 bullet points of what changed>

Tests: <N> passed, 0 failed
```

**Types:** `feat:` (new feature), `fix:` (bug fix), `test:` (test changes), `docs:` (documentation), `refactor:` (code restructuring), `chore:` (maintenance)

### Push
```bash
git push
```

Wait for CI to complete. If CI fails, fix before continuing.

---

## 6. MARK COMPLETE

After push succeeds:
1. Open `TODO.md`
2. Change `- [ ]` to `- [x]` for the completed item
3. Commit: `chore: mark <task> as complete`
4. Push

---

## 7. LOOP

Return to **Step 1** and repeat.

---

## DISCOVERY PHASE

Triggered when: **no unchecked P1/P2/P3 items remain** in TODO.md.

### 7.1 Coverage Scan
```bash
pytest tests/ --cov=electoral_sim --cov-report=term --tb=no -q
```
- Identify files below **80% coverage**
- For each <80% file, add a TODO: `test: increase coverage of <file> from X% to Y%`
- **Skip:** GPU code, Numba JIT code (untestable without hardware)

### 7.2 Code Smell Scan
Search for patterns that indicate incomplete or placeholder code:
```bash
grep -rn "pass  # Placeholder\|TODO\|FIXME\|HACK\|stub\|not implemented" electoral_sim/ --include="*.py"
```
- For each hit, add a TODO if it represents genuine unfinished work
- Skip docstring examples that mention "placeholder" for context

### 7.3 Missing Feature Scan
Compare listed features against the Feature Status table in README:
- Any `🟡 Beta` items that could be promoted to stable?
- Any `🔶 Experimental` items that could be promoted to beta?
- Add TODOs for items that need more tests or hardening

### 7.4 Documentation Gap Scan
```bash
grep -rn "^def \|^class " electoral_sim/ --include="*.py" | while read line; do
  # Check if function has a docstring
done
```
- Functions without docstrings → TODO: add docstring
- Modules missing from README → TODO: document

### 7.5 Dependency Audit
- Check `pyproject.toml` dependencies against actual imports
- Check if any optional dep has become a hard dep
- Add TODOs for any mismatches

### 7.6 Test Quality Scan
- Any tests that only check `assert X is not None`? → TODO: add meaningful assertions
- Any parametrize opportunities? → TODO: parametrize
- Any missing edge cases? → TODO: add edge case tests

### 7.7 Generate New TODO Items
Compile all findings into TODO.md under the appropriate priority sections:
- **P1:** Bugs, broken imports, CI failures
- **P2:** Missing docstrings, modules below 80% coverage, data provenance
- **P3:** Screenshots, CI improvements, code quality
- **P5:** New features, additional countries, ML integration

### 7.8 Restart Loop
After generating new items, return to **Step 1** and resume the loop.

---

## Termination

The loop never truly ends — it discovers new work. But it should **pause** when:

1. **All remaining items are P5** (research / major features)
2. **Coverage ≥ 90%** across the project (excluding GPU/Numba code)
3. **Three consecutive discovery scans** produce zero new items
4. **Human says stop**

When pausing, commit a summary:
```
chore: iteration pause — all actionable items complete

Remaining: N P5 items (research / major features)
Coverage: 85%
Discovery scans with zero new items: 3
```

---

## Rollback Strategy

If a commit introduces a regression:
1. `git revert <bad-commit>` — create a revert commit
2. Push the revert
3. Mark the TODO item as unchecked again `[ ]`
4. Re-attempt with a corrected approach

If a commit breaks CI:
1. Fix immediately (do not push more work on top)
2. If fix is trivial (<5 min), amend the commit
3. If fix is non-trivial, revert and re-plan

---

## Checkpoint Schedule

After every **5 iterations**, create a lightweight checkpoint:
```bash
git tag checkpoint-$(date +%Y%m%d-%H%M)
git push --tags
```

This enables rolling back to a known-good state if the loop goes wrong.

---

## Quick Reference: Loop in One Terminal

```bash
# Start the loop
while true; do
  # 1. Get next task
  TASK=$(python -c "
import re
with open('TODO.md') as f:
    items = re.findall(r'- \[ \] \*\*P[123]\*\* (.+)', f.read())
    print(items[0] if items else 'NONE')
")

  if [ "$TASK" = "NONE" ]; then
    echo "No P1-P3 items remaining. Entering discovery phase..."
    # Discovery logic here
    break
  fi

  echo "=== Working on: $TASK ==="

  # 2-3. Human/agent does the work (docs/WORKFLOW.md)

  # 4. Verify
  pytest tests/ -q --tb=short || { echo "Tests failed!"; exit 1; }

  # 5. Commit
  git add -A
  git commit -m "feat: $TASK"
  git push

  echo "Done. Next iteration..."
done
```
