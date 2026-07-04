# Track C: Format Compliance Evaluation (📐)

**Status**: 📋 DESIGNED — NOT YET IMPLEMENTED

## What This Track Evaluates

Skills whose value is in making Claude's output **consistently structured**, not in changing what it says.

Examples:
- "All commit messages MUST follow conventional commits format"
- "API responses MUST use this JSON schema"
- "Code MUST follow this project's ESLint config"
- "Documentation MUST use this markdown template"

## Why Conversation-Transcript Judging Partially Fails Here

A skill that makes Claude output `{ "status": "ok", "data": [...] }` instead of a free-form response might score *lower* on our Track A "rigor" and "signal-to-noise" rubric — the format scaffolding takes space that could have been "insight." But the format IS the value. Measuring the wrong dimension produces misleading negatives.

## Protocol

### Phase 1: Extract format rules

Parse SKILL.md body → extract every machine-checkable rule:

- JSON/XML/YAML schemas → validate with schema validator
- Naming conventions → regex match
- Code style → run linter (ESLint, ruff, etc.)
- Structural requirements → check heading hierarchy, required sections
- Template adherence → diff against template

### Phase 2: Generate test prompts

Create 5 diverse, realistic prompts that should trigger the format constraints. Each prompt:
- Is natural (a real user would type this)
- Has an obvious "correct answer" the model could give free-form

### Phase 3: Run A/B

```
Bare:  API call (no skill) + prompt → collect raw response
Armed: API call (with skill) + prompt → collect formatted response
```

Run 3 times per prompt (format MUST be consistent across runs).

### Phase 4: Automated compliance check

For each response pair, run automated checks:

| Check | Method | What failure looks like |
|-------|--------|------------------------|
| Schema validity | JSON Schema / XML DTD / regex | Response doesn't parse |
| Section completeness | Check required headings/blocks present | Missing "## References" section |
| Naming convention | Regex match against rules | `userName` instead of `user_name` |
| Linter score | Run ESLint/ruff on code blocks | 5+ lint warnings |
| Template match | Diff against template structure | Response adds unexpected sections |

### Phase 5: Judge the trade-off

For responses where the Armed output follows the format BUT the Bare output has better content:

Judge prompt:
```
Rate this trade-off:

Response A (free-form): {transcript}
Response B (format-constrained): {transcript}

1. Format adherence (0-10): Does B follow the declared format rules?
2. Content quality loss (0-10): How much information/insight was lost in B vs A?
   (0 = no loss, 10 = the format destroyed all value)
3. Net value judgment: "Format wins" / "Content wins" / "Wash"
```

### Phase 6: Report

```
Format Compliance Score: {compliance_rate}%
Content Quality Delta: -{loss}/10
Consistency across runs: {std deviation of compliance rate}
Verdict: Format improves structure at [minimal|moderate|severe] content cost
```

## Implementation Requirements

- Schema validators for JSON/XML/YAML
- Regex rule engine (configurable from skill body)
- Linter runners (ESLint, ruff, etc. — installed on eval machine)
- Format-vs-content judge prompt

## Edge Cases

- **Skill with format rules that can't be auto-checked**: "responses MUST be concise" → not machine-checkable. Fall back to judge-only.
- **Format that IS the content**: JSON API responses where the schema is the whole point. Content quality comparison is meaningless. Report format compliance only.
- **Partial format adherence**: Skill says "preferably use this format." Compliance rate ~70% is acceptable. Don't flag as failure.
