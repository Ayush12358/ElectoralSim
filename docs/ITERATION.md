# Continuous Iteration Workflow

> The meta-workflow that drives all development. This loops continuously:
> pick a task from TODO.md → implement it via WORKFLOW.md → repeat.
> When TODO.md is empty, scan the repo for new work.

---

## Step 0: Start of Session

### 0.1 Read the State
```bash
cat TODO.md
```

### 0.2 Count Open Items
Count all `- [ ]` lines. If zero, jump to **Step 4: Generate New TODOs**.

### 0.3 Pick the Next Task
Scan TODO.md top-to-bottom. Priority order is:
1. **P1 Bugs & Technical Debt** — highest impact, smallest effort
2. **P1 Features** — important, user-facing
3. **P2 Features** — important but not urgent
4. **P3 Nice-to-haves** — polish items
5. **P5 Research / Long-term** — large scope, low urgency

Within the same priority level, pick:
- **Bug fixes over features** (bugs degrade trust more than missing features)
- **Smaller items over larger ones** (build momentum, ship faster)
- **Items that unlock other items** (dependency resolution)

### 0.4 Announce the Choice
State clearly: "Next task: **[priority] Short description** from TODO.md (line N)."

Then pass control to **`docs/WORKFLOW.md`** to implement it.

---

## Step 1: Implement (via WORKFLOW.md)

Follow the full 6-phase workflow:
1. **Intake & Research** — map files, read code, understand context
2. **Plan** — design API, plan tests, estimate coverage
3. **Implement** — write code following conventions
4. **Test** — write tests, run suite, verify coverage
5. **Document** — update docstrings, README, AGENTS.md
6. **Verify & Commit** — full checks, commit with stats, push

---

## Step 2: Mark Complete

### 2.1 Check Off in TODO.md
Change `- [ ]` to `- [x]` for the completed item.

### 2.2 Verify the Mark
```bash
grep "\[x\]" TODO.md | grep "<completed item text>"
```

---

## Step 3: Loop

### 3.1 Check Remaining
```bash
grep -c "\[ \]" TODO.md
```

If count > 0, go back to **Step 0.3** and pick the next task.

If count == 0, proceed to **Step 4**.

---

## Step 4: Generate New TODOs (when TODO.md is empty)

### 4.1 Audit the Codebase
Run these checks across the entire repo:

#### Coverage gaps
```bash
pytest tests/ --cov=electoral_sim --cov-report=term --tb=no -q
```
Look for modules with **<80% coverage**. For each, note the uncovered lines.

#### TODO/FIXME/HACK comments
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX" electoral_sim/ tests/ --include="*.py"
```

#### Untested exception paths
```bash
grep -rn "except " electoral_sim/ --include="*.py" | grep -v "test_"
```
For each `except` block, check if there's a test that hits it.

#### Missing docstrings
```bash
pytest tests/ --cov=electoral_sim --cov-report=term --tb=no -q 2>&1 || true
# Then manually scan any public functions without docstrings
```

#### Feature gaps from README
Compare the README Feature Status table against the actual code. Items marked 🔶 Experimental or 🟡 Beta are candidates for upgrade.

#### Unused or stale files
```bash
# Files not imported anywhere
find electoral_sim/ -name "*.py" ! -name "__init__.py" | while read f; do
    name=$(basename $f .py)
    grep -rq "from.*import.*$name\|import.*$name" electoral_sim/ tests/ || echo "possibly unused: $f"
done
```

#### Missing test files
For each module in `electoral_sim/`, verify a corresponding test file exists in `tests/`.

### 4.2 Categorize Findings

Rate each finding by priority:

| Priority | Criteria | Example |
|----------|----------|---------|
| **P1** | Bug with no workaround, test failure, security issue | Import error, crash on valid input |
| **P2** | Missing test coverage for core module, undocumented feature, known limitation | Module at 30% coverage |
| **P3** | Polish: formatting, docstring improvements, cleanup | Stale TODO comment |
| **P5** | Future research, stretch goals, speculative features | Multi-country simultaneous elections |

### 4.3 Write to TODO.md

Add new items under appropriate sections. Use the format:
```markdown
- [ ] **P1** Short actionable description
    - Sub-item if the task has steps
```

Add a header noting the generation:
```markdown
### Technical Debt — Found 2026-06-04
```

### 4.4 Commit
```bash
git add TODO.md
git commit -m "chore: regenerate TODO.md after clearing all items

Found N items across codebase:
- Coverage gaps: X modules below 80%
- Untested paths: Y exception handlers
- Missing docstrings: Z functions
- ..."
```

### 4.5 Loop Back
After committing, go back to **Step 0.3** and pick the first new task.

---

## Decision Tree (Quick Reference)

```
Start
  │
  ├─ TODO.md has open items?
  │     │
  │     YES ──► Pick next task (P1 > P2 > P3 > P5, bugs > features, smaller > larger)
  │     │        │
  │     │        ▼
  │     │        Follow WORKFLOW.md (6 phases)
  │     │        │
  │     │        ▼
  │     │        Mark [x] in TODO.md
  │     │        │
  │     │        ▼
  │     │        Commit & Push
  │     │        │
  │     │        └──► Loop back to Start
  │     │
  │     NO ──► Audit codebase (coverage, TODOs, excepts, docstrings, imports)
  │              │
  │              ▼
  │              Categorize into P1/P2/P3/P5
  │              │
  │              ▼
  │              Write to TODO.md
  │              │
  │              ▼
  │              Commit
  │              │
  │              └──► Loop back to Start
  │
  └─ Merge/release/PRs outstanding?
        │
        YES ──► Sort them out first (merge, close stale)
        │        │
        │        └──► Loop back to Start
        │
        NO ──► Continue with TODO.md flow
```

---

## Session Tracking

### At Start of Session
```bash
# Check if anything was left uncommitted
git status --short

# Check last commit for context
git log --oneline -5

# Count remaining items
grep -c "\[ \]" TODO.md
```

### At End of Session
```bash
# Ensure clean state
git status --short
# Should show nothing (or just TODO.md if regenerated)

# Count completed this session
git log --oneline --since="2 hours ago" | wc -l
```

---

## Example Session

```
Agent: Starting iteration cycle. 12 items remain in TODO.md.
       Next task: P1 Fix Numba multiprocessing crash (line 32)
       
       [Follows WORKFLOW.md: reads batch_runner.py, plans fix,
        uses multiprocessing.get_context("spawn"), adds OMP_NUM_THREADS=1,
        removes xfail, runs tests: 454 passed, commits]

Agent: Task complete. 11 items remain.
       Next task: P1 Add benchmark scripts (line 45)

       [Follows WORKFLOW.md: reads existing benchmarks, creates
        benchmark_core.py with argparse, warmup, env reporting,
        runs benchmark to verify output, commits]

Agent: Task complete. 10 items remain.
       Next task: P1 Fix "Opinion dynamics (placeholder)" docstring (line 33)
       
       ...
       
Agent: All items complete. 0 items remain.
       Running codebase audit...
       
       Coverage gaps found:
       - core/cli.py: 0% (122 statements)
       - visualization/specialized.py: 0% (54 statements)
       
       Adding to TODO.md as P2 tasks.
       Committed generated TODO.md.
       
       Starting new iteration cycle. 7 items in TODO.md.
       Next task: P2 Add CLI tests (coverage 0% → 84%)
```
