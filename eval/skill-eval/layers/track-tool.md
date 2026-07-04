# Track D: Tool Correctness Evaluation (🔧)

**Status**: 📋 DESIGNED — NOT YET IMPLEMENTED

## What This Track Evaluates

Skills that wrap executable code — scripts, CLI tools, API calls.

Examples:
- "Screenshot this URL" → wraps a headless browser
- "Deploy to staging" → wraps deployment scripts
- "Search our internal knowledge base" → wraps an API
- "Migrate the database" → wraps SQL migration tools

## Why Behavioral Delta Judging Fails Here

For tool-wrapper skills:
- The conversation *transcript* is irrelevant — either the tool ran correctly or it didn't
- "Bare" Claude can't run scripts — so the skill always "wins" on actionability, trivially
- Behavioral delta measures the WRONG THING — measuring "did the tool run?" instead of "did the tool produce the correct output?"

## Protocol

### Phase 1: Extract tool inventory

Parse SKILL.md body + `scripts/` directory → enumerate every tool/command the skill documents:

- Read all `.sh`, `.py`, `.js` files in `scripts/`
- Grep body for `npx`, `uv run`, `python`, `curl`, documented CLI commands
- Each tool = one test item

### Phase 2: Generate test inputs

For each tool, generate 3 test cases:

| Case | Input | Expected |
|------|-------|----------|
| Happy path | Valid, normal input | Expected output format |
| Edge case | Valid but unusual input | Should handle gracefully |
| Error | Invalid input | Should fail cleanly with error message |

If the skill's `tests.md` provides test scenarios, use those first.

### Phase 3: Execute (with AND without skill)

```
With skill loaded:
  Claude Code session → user types "/skill-name command args" → capture stdout/stderr/exit code

Without skill (direct):
  Run the underlying script directly → capture stdout/stderr/exit code
```

Compare: does the skill ADD value (better error messages, default handling, validation) or just pass through?

### Phase 4: Score

| Metric | How to measure | Weight |
|--------|---------------|--------|
| **Success rate** | % of happy-path tests that pass | 40% |
| **Edge case handling** | % of edge cases handled without crashing | 25% |
| **Error handling** | % of error cases that fail cleanly (useful message, non-zero exit) | 20% |
| **Value-add over raw tool** | Does the skill add validation/better UX vs running the tool directly? | 15% |

### Phase 5: Report

```
Tool Correctness Score: {score}%
Successful: {passed}/{total} tests
Edge cases handled: {edge_passed}/{edge_total}
Error handling: {error_passed}/{error_total}
Value-add: [minimal / moderate / significant]

Failed tests:
  - happy_path_03: script timeouts after 30s
  - edge_02: passes null to function that doesn't handle it
```

## Open Questions

- **Tool requires credentials**: Some tools need API keys, DB access, etc. How to test in CI?
  → Option A: Skip; flag "requires live environment"
  → Option B: Mock responses
- **Destructive tools**: Some tools deploy, migrate, or delete. How to test safely?
  → Run in sandbox/container; flag in report "tested in isolated environment"
- **Long-running tools**: Model training, large data processing. Timeout threshold?
  → Set a configurable timeout; flag any test that times out
