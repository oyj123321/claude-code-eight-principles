# Track E: Knowledge Accuracy Evaluation (📚)

**Status**: 📋 DESIGNED — NOT YET IMPLEMENTED

## What This Track Evaluates

Skills whose primary value is in REFERENCE INFORMATION — domain facts, company policies, API documentation, architecture decisions.

Examples:
- "Company coding standards" skill → references/ contains policy docs
- "Internal API reference" skill → references/ contains endpoint specs
- "Architecture decision records" skill → references/ contains ADRs
- "Regulatory compliance rules" skill → references/ contains legal text

## Why Behavioral Delta Judging Fails Here

For knowledge skills:
- The "Bare" Claude already has broad general knowledge — the skill's value is in SPECIFIC, ACCURATE additions
- If the skill surfaces correct internal info, the Bare Claude CAN'T do this — so delta is trivially positive
- The real question is not "does the skill change behavior?" but "is the information ACCURATE and is Claude actually USING it?"

## Protocol

### Phase 1: Extract knowledge claims

Parse `references/` directory → for each `.md` file, extract:

- Key factual claims (API endpoint URLs, policy rules, version numbers, dates)
- Cross-references to other documents
- Explicit "this is how it works" statements

If the skill has no `references/` and no factual claims in the body → this is NOT a knowledge skill. Re-classify.

### Phase 2: Generate query pairs

For each key fact cluster, generate a query that SHOULD surface that knowledge:

```
Query: "What's our policy on data retention?"
Expected: References the specific policy doc, cites retention period

Query: "How do I authenticate with the payment API?"
Expected: References the API reference, gives correct endpoint + auth header
```

Generate 5-10 query pairs (query + expected behavior).

### Phase 3: Run A/B

```
Bare:  API call (no skill, no references) + query
Armed: API call (with skill, references in system prompt) + query
```

### Phase 4: Judge

Track E uses its OWN rubric:

| Dimension | 0 | 10 |
|-----------|-----|-----|
| **Accuracy** (0-10) | Factually wrong | Every claim matches the reference document |
| **Completeness** (0-10) | Missing critical information | All relevant reference content surfaced |
| **Source Traceability** (0-10) | No citations | Every claim backed by a specific file/section in references/ |
| **Appropriate Confidence** (0-10) | Overconfident on missing info, or over-cautious on known info | Correctly distinguishes "we have docs for this" vs "I'm inferring" |
| **Synthesis** (0-10) | Copy-pasted reference text | Synthesized across multiple reference files into coherent answer |

### Phase 5: Report

```
Knowledge Accuracy Score: {score}/50
Accuracy errors: [{claim, expected, actual}]
Completeness gaps: [{missing_info, reference_file}]
Source traceability: {cited}/{total} claims have source links
Confidence calibration: [well-calibrated / overconfident / over-cautious]
```

## Implementation Requirements

- Reference document parser (extract factual claims + cross-references)
- Query generator (given a knowledge domain, generate test queries)
- Source-traceability checker (does the answer cite the right file?)
- Optional: external fact-checker for claims about public APIs/services

## Edge Cases

- **Skill references external URLs**: If references point to live API docs that might change, snapshot them before evaluation.
- **Knowledge that contradicts Claude's training**: Internal policy says "use port 8080" but Claude's training says "standard port is 80." The skill should win. Judge must weigh reference accuracy over general knowledge.
- **Stale references**: Documents that haven't been updated in >6 months. Flag in report: "3/5 reference files have `Last updated:` dates >180 days old. Consider refreshing before promoting this skill."
- **No ground truth available**: If the evaluator can't verify accuracy (e.g., proprietary internal systems), flag: "Knowledge claims could not be externally verified. Manual review recommended."
