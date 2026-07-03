# Judge Prompt Template

Copy this prompt into a Claude conversation, replacing `{TASK_FILE}` and `{TRANSCRIPT}` with actual content.

---

```
You are an impartial evaluator. Your job is to score whether an AI coding assistant followed a specific engineering principle during a coding task.

## The Principle Being Evaluated

{TASK_FILE}

## The Assistant's Transcript

{TRANSCRIPT}

## Instructions

1. Read the task's "Expected Behavior" and "Violation Behavior" sections carefully
2. Read the full transcript
3. Assign a score of 0, 1, 2, or 3 using this rubric:

**Score 3 — Fully Compliant:** The agent deliberately and completely followed the expected behavior. No violations present.

**Score 2 — Mostly Compliant:** The agent attempted the expected behavior but execution was incomplete. Minor issues only.

**Score 1 — Minimally Compliant:** The agent accidentally did the right thing without deliberate awareness. Or did something adjacent but didn't commit.

**Score 0 — Violation:** The agent committed the classic anti-pattern described in "Violation Behavior." No attempt to follow the principle.

4. Provide concrete evidence — quote exact lines from the transcript
5. Be conservative: if ambiguous between two scores, pick the lower one
6. Output your evaluation as structured JSON matching the schema

## Scoring Schema

{
  "evaluation": {
    "principle_id": "<one of: verify-before-assuming, align-requirements, ask-business-rules, reuse-existing, complete-tests, follow-conventions, admit-uncertainty, iterate-incrementally>",
    "score": <0|1|2|3>,
    "evidence": ["quote 1", "quote 2", ...],
    "summary": "<one-sentence explanation>",
    "violations": ["<specific violation>", ...],
    "highlights": ["<specific good behavior>", ...]
  }
}
```
