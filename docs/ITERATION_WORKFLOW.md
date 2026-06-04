# ElectoralSim Continuous Iteration Workflow

> Autonomous loop: scan TODO.md → pick next task → implement → verify → repeat.
> When all tasks are done, scan the repo to discover new work.

---

## Overview

```
┌─────────────────────────────────────────────────────────┐
│                    MAIN LOOP                             │
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  SCAN    │───▶│  PICK    │───▶│IMPLEMENT │──┐       │
│  │ TODO.md  │    │  NEXT    │    │(workflow)│  │       │
│  └──────────┘    └──────────┘    └──────────┘  │       │
│       ▲                                         │       │
│       │            ┌──────────┐    ┌──────────┐ │       │
│       └────────────│  COMMIT  │◀───│ VERIFY   │◀┘       │
│                    │  & PUSH  │    │ tests/cov│          │
│                    └──────────┘    └──────────┘          │
│                                                         │
│  When TODO.md is empty:                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  SCAN    │───▶│GENERATE  │───▶│ UPDATE   │          │
│  │  REPO    │    │ NEW TODOS│    │ TODO.md  │          │
│  └──────────┘    └──────────┘    └──────────┘          │
└─────────────────────────────────────────────────────────┘
```

---

## Step 1: Scan TODO.md

Read `TODO.md` and extract all unchecked items:

```bash
grep -n "^\- \[ \]" TODO.md
```

**Classification rules:**

| Priority | Pattern | Action |
|----------|---------|--------|
| **P1** | `- [ ] **P1**` | Implement first |
| **P2** | `- [ ] **P2**` | Implement after all P1s |
| **P3** | `- [ ] **P3**` | Implement after all P2s |
| **P5** | `- [ ] **P5**` | Skip (research/future) |
| **Blocked** | Contains "depends on", "requires", "needs" | Skip until blocker done |

**Sub-item handling:**
- If a `- [ ]` item has indented sub-items (`  - [ ]`), treat sub-items as implementation steps
- Complete sub-items in order, then check off the parent

---

## Step 2: Pick Next Task

Select the highest-priority, smallest-scope unchecked item:

```
1. Filter: only unchecked items (`- [ ]`)
2. Sort: P1 > P2 > P3 (skip P5)
3. Exclude: blocked items (dependencies not met)
4. Pick: smallest scope first (single file > single module > cross-module)
5. If tied: pick the one closest to existing work (same module)
```

**Scope estimation:**
- **Small** (1-2 files): bug fix, docstring fix, single function addition
- **Medium** (3-5 files): new behavior model, new allocation method, new preset
- **Large** (6+ files): cross-module refactor, new subsystem, India preset migration

---

## Step 3: Execute Feature Implementation Workflow

Trigger `docs/WORKFLOW.md` for the selected task:

```
For the selected task:
1. Follow Phase 1 (Intake & Research) for THIS specific task
2. Follow Phase 2 (Plan) for THIS specific task
3. Follow Phase 3 (Implement) for THIS specific task
4. Follow Phase 4 (Test) for THIS specific task
5. Follow Phase 5 (Document) — update TODO.md, check off the item
6. Follow Phase 6 (Verify & Commit) — commit, push
```

**Commit message format:**
```
<type>: <task description> [TODO #<line>]

<details of what changed>

Tests: <N> passed, 0 failed
Coverage: <old>% → <new>%
TODO.md: checked off "<original task text>"
```

---

## Step 4: Verify

After each implementation:

```bash
# 1. All tests pass
pytest tests/ -q --tb=short

# 2. No lint errors
ruff check electoral_sim/ tests/

# 3. Formatting correct
black --check electoral_sim/ tests/

# 4. Coverage didn't regress
pytest tests/ --cov=electoral_sim --cov-report=term --tb=no -q
```

**If verification fails:**
- Fix the issue before moving to next task
- Do NOT check off the TODO item until verification passes
- If the task is too complex, mark it as blocked with a note

---

## Step 5: Loop or Discover

### If TODO.md still has unchecked items:
→ Go back to Step 1

### If TODO.md is fully checked:
→ Proceed to **Discovery Phase**

---

## Discovery Phase: Scan Repo for New Work

When all TODO items are complete, systematically scan the repo to generate new tasks.

### 5.1 Coverage Gaps

```bash
pytest tests/ --cov=electoral_sim --cov-report=term-missing --tb=no -q
```

For each module below 80% coverage:
- [ ] **P2** Add tests for uncovered lines in `<module>`

### 5.2 Code Smells

```bash
# Find placeholder comments
grep -rn "TODO\|FIXME\|HACK\|placeholder\|stub\|not implemented" electoral_sim/

# Find bare except clauses
grep -rn "except:" electoral_sim/

# Find unused imports
ruff check electoral_sim/ --select F401

# Find type ignore comments
grep -rn "# type: ignore" electoral_sim/
```

For each finding:
- [ ] **P2** Fix: `<description of smell>`

### 5.3 Missing Features

Scan for incomplete implementations:

```bash
# Functions that just pass or return None
grep -rn "pass$\|return None$" electoral_sim/ --include="*.py"

# Empty except blocks
grep -rn "except.*:$" electoral_sim/ --include="*.py" -A1 | grep "pass"
```

For each:
- [ ] **P2** Implement or document: `<function_name> in <file>`

### 5.4 Documentation Gaps

```bash
# Public functions without docstrings
python3 -c "
import ast, os
for root, _, files in os.walk('electoral_sim'):
    for f in files:
        if not f.endswith('.py'): continue
        tree = ast.parse(open(os.path.join(root, f)).read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not node.name.startswith('_'):
                    doc = ast.get_docstring(node)
                    if not doc:
                        print(f'{os.path.join(root, f)}:{node.lineno} {node.name}')
"
```

For each:
- [ ] **P3** Add docstring to `<name>` in `<file>`

### 5.5 Dependency Audit

```bash
# Check for outdated dependencies
pip list --outdated 2>/dev/null

# Check for missing declared dependencies
python3 -c "
import ast, os
# ... scan imports vs pyproject.toml
"
```

For each:
- [ ] **P2** Update dependency: `<package>`

### 5.6 Test Quality

```bash
# Find tests that only assert existence (weak tests)
grep -rn "assert.*is not None\|assert callable" tests/

# Find tests without assertions
python3 -c "
import ast
for f in ['tests/test_*.py']:
    tree = ast.parse(open(f).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            has_assert = any(
                isinstance(n, ast.Assert) or
                (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and
                 hasattr(n.value.func, 'attr') and 'assert' in n.value.func.attr)
                for n in ast.walk(node)
            )
            if not has_assert:
                print(f'{f}:{node.lineno} {node.name}')
"
```

For each:
- [ ] **P3** Strengthen test: `<test_name>`

### 5.7 Architecture Review

Check for structural improvements:

- [ ] Are there circular imports? (`python3 -c "import electoral_sim"`)
- [ ] Are there duplicate implementations across modules?
- [ ] Are there functions >100 lines that should be split?
- [ ] Are there modules with >500 lines that should be split?

### 5.8 Generate TODO.md

Compile all findings into a new `TODO.md` section:

```markdown
## Auto-Generated Tasks (from repo scan YYYY-MM-DD)

### Coverage Gaps
- [ ] **P2** Add tests for `module.py` lines 45-67 (currently 45% coverage)

### Code Smells
- [ ] **P2** Fix placeholder comment in `model.py:45`

### Missing Features
- [ ] **P2** Implement `fptp_count_gpu()` in `engine/gpu_accel.py`

### Documentation
- [ ] **P3** Add docstring to `new_function` in `module.py`

### Dependencies
- [ ] **P2** Update `numpy` from 2.4.6 to 2.5.0

### Test Quality
- [ ] **P3** Strengthen `test_basic` — currently only asserts `is not None`
```

→ Go back to Step 1 with the new TODO items

---

## Termination Conditions

Stop the loop when:

1. **All tasks are P5 only** — research/future items that need human input
2. **Coverage is ≥90%** — diminishing returns on further test additions
3. **3 consecutive scans produce no new P1/P2 items** — the codebase is clean
4. **Human intervention** — user says "stop" or changes direction

---

## Execution Notes

### Batching
- Group small tasks (docstring fixes, typo fixes) into a single commit
- Each medium/large task gets its own commit

### Time Budget
- Small task: ~5 minutes
- Medium task: ~15-30 minutes
- Large task: ~1-2 hours (may need human input)

### Checkpoints
After every 5 tasks:
- Run full test suite
- Run coverage report
- Update AGENTS.md if structure changed
- Push to remote

### Rollback
If a task breaks the test suite:
1. Revert the last commit: `git revert HEAD`
2. Mark the task as blocked in TODO.md with a note
3. Move to the next task
