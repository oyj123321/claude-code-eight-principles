# Scoring Specification

## Two-Level Scoring

skill-eval scores are organized at two levels:

1. **Cross-track** (applies to ALL skills): `structural` + `cost`
2. **Per-track** (applies only to skills that match that track): track-specific dimensions

Dimensions are NOT combined into a single composite. The user reads all applicable dimensions and makes their own judgment.

---

## Cross-track Dimensions

### Dimension 1: `structural` (L1 → 0–1 scale)

**What it measures**: Is the SKILL.md well-formed? Does it pass static checks and avoid anti-patterns?

**Source**: Layer 1 (`layers/static.md`)

**Formula**:
```
structural = (passing_checks / 21) × anti_pattern_penalty
anti_pattern_penalty = max(0.5, 1.0 - 0.05 × anti_pattern_count)
```

**Interpretation**:
| Range | Meaning |
|-------|---------|
| ≥ 0.90 | Well-formed. No structural concerns. |
| 0.80–0.89 | Minor issues (WARNs present). Fix when convenient. |
| 0.60–0.79 | Significant issues. Fix before promotion. |
| < 0.60 | Critical issues. Do not install. |

### Dimension 2: `behavioral_delta` (L2 → per-constraint Δ list)

**What it measures**: For each behavioral constraint the skill claims, how much does it actually change Claude's output quality?

**Source**: Layer 2 (`layers/behavioral.md`)

**Formula** (per constraint):
```
Δ[c] = armed_judge_score[c] - bare_judge_score[c]
```
where `judge_score[c] = sum of 5 rubric dimensions (0–50)`.

**Aggregation**:
```
mean_delta = mean(Δ across all constraints)
positive_ratio = count(Δ > 0) / total_constraints
strong_positive_ratio = count(Δ > 5) / total_constraints  // >5/50 = clearly positive
```

**Interpretation**:
| mean_delta | Meaning |
|------------|---------|
| > +5 | Strong positive effect — skill clearly improves behavior |
| +1 to +5 | Moderate positive effect — skill nudges in right direction |
| -1 to +1 | No detectable effect — skill doesn't change behavior |
| < -1 | Negative effect — skill degrades behavior (over-constrains?) |

**Per-constraint report**: List top-3 most improved constraints and any constraints with negative Δ (the skill might be hurting there).

### Dimension 3: `cost` (L1+L2 → token budget analysis)

**What it measures**: What does it cost to run this skill?

**Components**:

| Component | Measurement | Source |
|-----------|-------------|--------|
| `skill_tokens` | Token count of SKILL.md body + description | L1 (wc + tokenizer) |
| `description_budget_share` | `skill_description_chars / 15360` (15K budget) | L1 |
| `redundant_calls_per_task` | Average extra tool calls attributable to skill rules | L2 (compare Bare vs Armed tool call counts) |
| `false_positive_rate` | Fraction of L2 tasks where judge score was ≤ 0 but skill's rules still activated | L2 |

**Interpretation**:
| Metric | Green | Yellow | Red |
|--------|-------|--------|-----|
| `skill_tokens` | < 500 | 500–2000 | > 2000 |
| `description_budget_share` | < 3% | 3–8% | > 8% |
| `redundant_calls_per_task` | 0 | 1–2 | > 2 |
| `false_positive_rate` | 0% | < 10% | ≥ 10% |

---

## Per-track Dimensions

Each track has its own scoring dimensions. Only dimensions from the skill's assigned tracks are computed and reported.

### Track A — Behavioral (Track A)

See `layers/behavioral.md` for the full protocol.

| Dimension | Scale | What it measures |
|-----------|-------|------------------|
| `behavioral_delta` | per-constraint Δ list, 0–50 judge scale | With vs without skill: quality change on each behavioral constraint |
| `mean_delta` | -50 to +50 | Average behavioral lift across all constraints |
| `positive_ratio` | 0–100% | Fraction of constraints that improved |

### Track B — Output Artifact (Track B)

See `layers/track-output.md` for the full protocol.

| Dimension | Scale | What it measures |
|-----------|-------|------------------|
| `artifact_structure` | 0–10 | Information architecture, logical flow |
| `artifact_visual_quality` | 0–10 | Layout, spacing, visual hierarchy |
| `artifact_completeness` | 0–10 | Nothing critical missing |
| `artifact_usability` | 0–10 | Receiver can use immediately |
| `artifact_professionalism` | 0–10 | Matches domain professional standards |

**Status: 📋 Designed, not implemented.**

### Track C — Format Compliance (Track C)

See `layers/track-format.md` for the full protocol.

| Dimension | Scale | What it measures |
|-----------|-------|------------------|
| `format_adherence` | 0–100% | % of responses that pass automated format checks |
| `format_consistency` | std deviation | Variance in adherence across multiple runs |
| `content_quality_loss` | 0–10 | How much information was lost in formatting (0 = none) |

**Status: 📋 Designed, not implemented.**

### Track D — Tool Correctness (Track D)

See `layers/track-tool.md` for the full protocol.

| Dimension | Scale | What it measures |
|-----------|-------|------------------|
| `tool_success_rate` | 0–100% | % of happy-path tests that pass |
| `tool_edge_handling` | 0–100% | % of edge cases handled without crashing |
| `tool_error_handling` | 0–100% | % of error cases that fail cleanly |
| `tool_value_add` | minimal/moderate/significant | Does the skill improve over running the tool directly? |

**Status: 📋 Designed, not implemented.**

### Track E — Knowledge Accuracy (Track E)

See `layers/track-knowledge.md` for the full protocol.

| Dimension | Scale | What it measures |
|-----------|-------|------------------|
| `knowledge_accuracy` | 0–10 | Every claim matches reference document |
| `knowledge_completeness` | 0–10 | All relevant reference content surfaced |
| `knowledge_source_traceability` | 0–10 | Claims backed by specific file/section citations |
| `knowledge_confidence` | 0–10 | Well-calibrated: doesn't over/underclaim |
| `knowledge_synthesis` | 0–10 | Synthesized across files, not copy-pasted |

**Status: 📋 Designed, not implemented.**

---

## Report Template

```markdown
# Skill Eval Report: {skill_name}

**Date**: {date}
**Depth**: {depth}
**Evaluator**: skill-eval v0.3.0

## L0: Skill Classification

| Field | Value |
|-------|-------|
| Primary track | {A/B/C/D/E} |
| All tracks | [{tracks}] |
| Track implementation status | {implemented / designed / unavailable} |

{If track is unimplemented: "⚠️ This skill is classified as Track {X}, which is designed but not yet implemented. Only L1 structural evaluation is available."}

## L1: Structural Compliance

| Check | Result |
|-------|--------|
| 21 static checks | {passed}/{total} passed |
| Anti-patterns found | {count} |
| **Score** | **{score} / 1.0** |
| **Grade** | **{letter_grade}** |

{Violation details if any}

## L2: Track Evaluation — {Track Name}

{Track-specific results section. Format varies by track.}

### Track A (Behavioral) — example:
{mean_delta_summary}

| Constraint | Bare Score | Armed Score | Δ | Verdict |
|------------|-----------|-------------|---|---------|
| {c01}: {text} | {bare} | {armed} | {delta} | {+/-} |

### Track B (Output) — example:
| Dimension | Bare | Armed | Δ |
|-----------|------|-------|---|
| Structure | {b} | {a} | {d} |
...

## Cost Analysis

| Metric | Value | Rating |
|--------|-------|--------|
| SKILL.md tokens | {tokens} | {color} |
| Budget share | {share}% | {color} |
| Track-specific overhead | {overhead} | {color} |

## Verdict

**{INSTALL / SKIP / FIX / CANNOT EVALUATE}**

{One-paragraph explanation}
```

---

## Letter Grade Reference (from PluginEval)

| Grade | Score Range |
|-------|-------------|
| A+ | ≥ 97 |
| A  | ≥ 93 |
| A- | ≥ 90 |
| B+ | ≥ 87 |
| B  | ≥ 83 |
| B- | ≥ 80 |
| C+ | ≥ 77 |
| C  | ≥ 73 |
| C- | ≥ 70 |
| D+ | ≥ 67 |
| D  | ≥ 63 |
| D- | ≥ 60 |
| F  | < 60 |

Applied to `structural` score × 100.
