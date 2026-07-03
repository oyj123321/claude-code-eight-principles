# Layer 1: Structural Compliance

## Overview

L1 answers: **"Is this SKILL.md well-formed and free of structural defects?"**

Two sub-layers:
1. **External**: Run skill-kit `check-skill` (21 deterministic checks) — if skill-kit is not installed, fall back to a manual checklist
2. **Internal**: Scan for 11 anti-patterns derived from PluginEval's static analyzer

## Sub-layer 1A: skill-kit `check-skill` (21 Checks)

Run: `check-skill <path-to-skill-dir>`

Exit code 0 = zero FAILs. WARNs are informational only.

If skill-kit is NOT installed, manually verify these critical checks:

| # | Critical Check | How to verify manually |
|---|---------------|----------------------|
| 1 | Frontmatter parses as YAML | Read SKILL.md lines 1-5 |
| 2 | `name` ≤64 chars, kebab-case, no "anthropic"/"claude" | Inspect frontmatter |
| 5 | `description` present, ≤1024 chars | Count chars in description |
| 10 | No Windows backslash paths | Grep for `C:\` or `\\host` |
| 13 | No leaked secrets (`sk-`, `ghp_`, `AKIA`) | Grep for secret patterns |
| 14 | `tests.md` sidecar with ≥3 scenarios | Check file exists |

## Sub-layer 1B: Anti-pattern Detection (11 Rules)

Scans the SKILL.md body for these structural/design anti-patterns. Each costs 5% penalty (multiplicative, floors at 50%).

| # | Flag | Severity | Trigger | How to Check |
|---|------|----------|---------|--------------|
| 1 | `MISSING_TRIGGER` | 15% | No "Use when"/"Use whenever"/"trigger(s) when" in description | Read description field |
| 2 | `EMPTY_DESCRIPTION` | 10% | Description < 20 chars | Count description chars |
| 3 | `OVER_CONSTRAINED` | 10% | > 15 MUST/ALWAYS/NEVER directives | Grep for `MUST\|ALWAYS\|NEVER` |
| 4 | `BLOATED_SKILL` | 10% | > 500 lines without references/ dir | Count lines in SKILL.md |
| 5 | `SKILL_OVER_CODEX_CAP` | 15% | Body > 8KB without references/ | `wc -c` SKILL.md |
| 6 | `ORPHAN_REFERENCE` | 5% | Dead link in SKILL.md to a file in references/ | For each reference link, check if file exists |
| 7 | `CLAUDE_TOOL_REFS` | 5% | Backticked CamelCase tool names (`` `Read` ``) | Grep for backticked CamelCase |
| 8 | `CLAUDE_TOOL_PROSE` | 5% | Prose like "use the Read tool" (portability issue) | Grep for "use the [A-Z]" pattern |
| 9 | `AGENT_NAME_COLLISION` | 10% | Agent named `default`/`worker`/`explorer` | Check frontmatter `name` field |
| 10 | `BARE_MODEL_ALIAS` | 3% | Bare `opus`/`sonnet`/`haiku` (use `inherit`) | Grep for bare model names |
| 11 | `FIRST_PERSON_DESC` | 5% | Description uses "I can"/"You can" (should be 3rd person) | Grep for `I can\|You can` |

### Penalty Formula

```
structural_score = (passing_checks / 21) × anti_pattern_penalty
anti_pattern_penalty = max(0.5, 1.0 - 0.05 × anti_pattern_count)
```

### Letter Grade Mapping

| Grade | Score Range | Interpretation |
|-------|-------------|----------------|
| A+ | ≥ 97 | Reference quality |
| A  | ≥ 93 | Excellent |
| A- | ≥ 90 | Very good |
| B+ | ≥ 87 | Good |
| B  | ≥ 83 | Solid |
| B- | ≥ 80 | Acceptable |
| C+ | ≥ 77 | Needs improvement |
| C  | ≥ 73 | Several issues |
| C- | ≥ 70 | Marginal |
| D+ | ≥ 67 | Poor |
| D  | ≥ 63 | Very poor |
| D- | ≥ 60 | Barely passing |
| F  | < 60 | Failing |

## L1 Output Format

```json
{
  "layer": "L1",
  "depth": "quick",
  "skill_path": ".claude/skills/eight-principles",
  "structural_score": 0.91,
  "letter_grade": "A-",
  "checks_passed": 21,
  "checks_total": 21,
  "anti_patterns_found": 0,
  "anti_pattern_details": [],
  "verdict": "PASS",
  "recommendation": "Structurally well-formed. Proceed to L2 for behavioral delta measurement."
}
```

## Gate Rule

If structural_score < 0.60 (F): **stop**. Report the violations and recommend fixes. Do NOT proceed to L2 — a fundamentally broken SKILL.md cannot be meaningfully evaluated for behavioral delta.
