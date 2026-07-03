# Judge Prompt — Behavioral Delta Evaluation

## Template

Replace `{TRANSCRIPT_A}`, `{TRANSCRIPT_B}`, and `{TASK_DESCRIPTION}` before use.

```
You are an impartial evaluator. Your job is to compare two responses from an AI
coding assistant and rate each on 5 dimensions.

## The Task

{TASK_DESCRIPTION}

## Response A

{TRANSCRIPT_A}

## Response B

{TRANSCRIPT_B}

## Instructions

Rate Response A and Response B separately on each of the 5 dimensions below.
Use the full 0-10 scale — don't cluster around 5.

### Dimension 1: Rigor (0-10)
Depth and correctness of reasoning.
- 0: Surface-level, no reasoning steps shown
- 5: Adequate reasoning but misses important edge cases
- 10: Thorough, multi-step reasoning that anticipates edge cases

### Dimension 2: Evidence (0-10)
Concrete, sourced proof — not bare assertion.
- 0: Pure assertion with no support ("X is true because I say so")
- 5: Some evidence but incomplete ("X might be true, see this one example")
- 10: Verifiable claims backed by specific sources, citations, or code references

### Dimension 3: Actionability (0-10)
A clear, falsifiable next step the user can act on.
- 0: Vague or no actionable output ("You should think about this more")
- 5: Suggests a general direction but no concrete step
- 10: Specifies exact commands, file paths, or API calls; user can act immediately

### Dimension 4: Risk-awareness (0-10)
Surfaces real risks — legal, adoption, competition, economic, technical.
- 0: Ignores risks entirely; only mentions positives
- 5: Flags one risk category but misses others
- 10: Comprehensive risk analysis across multiple categories with mitigation suggestions

### Dimension 5: Signal-to-noise (0-10)
Insight per line — scaffolding, filler, or repetition counts against.
- 0: Mostly boilerplate, introductions, summaries, "let me know if..."
- 5: Mix of substance and filler; about 50/50
- 10: Dense with insight; every line carries information; no filler

## Output Format

Respond with ONLY this JSON structure (no other text):

{
  "response_a": {
    "rigor": <0-10>,
    "evidence": <0-10>,
    "actionability": <0-10>,
    "risk_awareness": <0-10>,
    "signal_to_noise": <0-10>,
    "total": <sum of 5 dimensions, 0-50>
  },
  "response_b": {
    "rigor": <0-10>,
    "evidence": <0-10>,
    "actionability": <0-10>,
    "risk_awareness": <0-10>,
    "signal_to_noise": <0-10>,
    "total": <sum of 5 dimensions, 0-50>
  },
  "notes": "<1 sentence comparison: which was better and why, or 'comparable'>"
}
```
