# Bisection Guide

Git bisect workflow, binary search debugging techniques, and strategies for narrowing
the source of a bug to a specific change.

---

## Git Bisect Workflow

### When to Use Bisect

Use git bisect when:
- The bug appeared at some point in history (not always present)
- You can identify a known-good commit and a known-bad commit
- You have a way to test each commit (automated or manual)

Do NOT use when:
- The bug is in uncommitted code
- The bug is environment-dependent (same code, different behavior)
- The test takes longer than a few minutes per commit

### Basic Workflow

```bash
# 1. Start bisect session
git bisect start

# 2. Mark the current (broken) commit as bad
git bisect bad

# 3. Mark a known-good commit
git bisect good abc1234

# 4. Git checks out a middle commit. Test it.
# If the bug is present:
git bisect bad

# If the bug is NOT present:
git bisect good

# 5. Repeat step 4 until git identifies the first bad commit
# Output: abc5678 is the first bad commit

# 6. End the bisect session
git bisect reset
```

### Automated Bisect

If you have a script that exits 0 for good and non-zero for bad:

```bash
git bisect start HEAD abc1234
git bisect run python -m pytest tests/test_auth.py::test_login -x
```

Git runs the script for each bisect step automatically. This is the most efficient
approach when a reliable test exists.

### Bisect with a Test Script

```bash
#!/bin/bash
# bisect_test.sh — exits 0 if good, 1 if bad

# Build or install if needed
pip install -e . 2>/dev/null

# Run the specific test
python -c "
from mymodule import process
result = process('test_input')
assert result == 'expected', f'Got {result}'
" 2>/dev/null

# Exit code propagates to git bisect
```

```bash
git bisect start HEAD v1.0.0
git bisect run bash bisect_test.sh
```

### Handling Untestable Commits

Some commits may not compile or may be irrelevant (docs-only changes):

```bash
# Skip the current commit (don't mark good or bad)
git bisect skip

# Skip a range of commits
git bisect skip abc1234..def5678
```

### Viewing Bisect Progress

```bash
# See the remaining commits to test
git bisect visualize

# See bisect log
git bisect log

# Estimate remaining steps
# N commits remaining → log2(N) steps left
```

---

## Binary Search Debugging (Non-Git)

### Comment-Out Bisection

When the bug is within a single function or file, use binary search on code blocks:

1. Comment out the bottom half of the suspect code
2. Run the test
3. If bug persists → bug is in the top half
4. If bug disappears → bug is in the bottom half
5. Repeat on the identified half

This finds the offending line in `O(log N)` steps.

### Input Bisection

When a large input triggers the bug but a small input doesn't:

1. Take the full input that triggers the bug
2. Remove the second half
3. Test with the first half only
4. If bug persists → bug is triggered by something in the first half
5. If bug disappears → the triggering element is in the second half
6. Repeat until you find the minimal triggering input

### Configuration Bisection

When a configuration change causes the bug:

1. Start with the known-bad configuration
2. Change half the settings back to known-good values
3. Test
4. Narrow to the half that contains the breaking change
5. Repeat

---

## Narrowing Techniques

### Delta Debugging

Minimize the failing input systematically:

1. Start with the full failing input
2. Remove one element/section at a time
3. If the bug still reproduces → that element was irrelevant
4. If the bug disappears → that element is relevant to reproduction
5. Continue until no element can be removed without losing the bug

The result is a **minimal reproduction** — the smallest input that triggers the bug.

### Time-Based Narrowing

When you don't know when the bug was introduced:

```bash
# Find when the test last passed using exponential search
# Test HEAD~1, HEAD~2, HEAD~4, HEAD~8, HEAD~16...
git stash  # Save current changes
git checkout HEAD~1 && run_test   # bad
git checkout HEAD~2 && run_test   # bad
git checkout HEAD~4 && run_test   # bad
git checkout HEAD~8 && run_test   # good!
# Bug was introduced between HEAD~8 and HEAD~4
git bisect start HEAD~4 HEAD~8
```

### Feature Flag Bisection

When the bug might be caused by one of several features:

1. Disable all feature flags → baseline
2. Enable half the flags
3. If bug appears → one of the enabled flags causes it
4. If bug doesn't appear → enable the other half
5. Repeat until the offending flag is identified

---

## Common Pitfalls

### Flaky Tests During Bisect

If the test is intermittent, bisect gives wrong results. Mitigation:

```bash
# Run the test N times and fail only if it fails consistently
#!/bin/bash
FAILURES=0
for i in {1..5}; do
  python -m pytest tests/test_flaky.py -x || ((FAILURES++))
done
[ $FAILURES -ge 3 ]  # Exit 0 (bad) if 3+ failures out of 5
```

### Merge Commits

Bisect on merge-heavy histories can be confusing. Use `--first-parent` to
bisect only the merge commits on the main branch:

```bash
git bisect start --first-parent HEAD v1.0.0
```

### Bisect Across Dependency Changes

If the bug is caused by a dependency update, the bisect commit will be the one
that updated the lockfile. Check `requirements.txt` / `pyproject.toml` diffs
in the identified commit.

### Preserving Bisect State

If you need to pause bisect:

```bash
# Save progress
git bisect log > bisect_progress.log

# Later, replay
git bisect replay bisect_progress.log
```
