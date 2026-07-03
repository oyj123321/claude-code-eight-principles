# Scoring Specification

## The 3 Dimensions

skill-eval MVP uses 3 independent dimensions. They are NOT combined into a single composite score — each stands alone. The user reads all three and makes their own judgment.

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

## Report Template

```markdown
# Skill Eval Report: {skill_name}

**Date**: {date}
**Depth**: {depth}
**Evaluator**: skill-eval v0.1.0

## L1: Structural Compliance

| Check | Result |
|-------|--------|
| 21 static checks | {passed}/{total} passed |
| Anti-patterns found | {count} |
| **Score** | **{score} / 1.0** |
| **Grade** | **{letter_grade}** |

{Violation details if any}

## L2: Behavioral Delta

{mean_delta_summary}

| Constraint | Bare Score | Armed Score | Δ | Verdict |
|------------|-----------|-------------|---|---------|
| {c01}: {text} | {bare} | {armed} | {delta} | {+/-} |
| ... | ... | ... | ... | ... |

**Top improvements**: {list of constraints with highest Δ}
**Regressions**: {list of constraints with negative Δ, or "None"}

## Cost Analysis

| Metric | Value | Rating |
|--------|-------|--------|
| SKILL.md tokens | {tokens} | {color} |
| Budget share | {share}% | {color} |
| Redundant calls | {calls}/task | {color} |
| False positive rate | {rate}% | {color} |

## Verdict

**{INSTALL / SKIP / FIX}**

{One-paragraph explanation synthesizing all three dimensions}
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
