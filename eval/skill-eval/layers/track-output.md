# Track B: Output Artifact Evaluation (🎨)

**Status**: 📋 DESIGNED — NOT YET IMPLEMENTED

## What This Track Evaluates

Skills whose primary value is in **the files they produce**, not the conversation that produced them.

Examples:
- "Create a 10-slide investor pitch deck from my notes" → value is in the `.pptx`
- "Build a responsive dashboard UI component" → value is in the `.tsx` + `.css`
- "Generate a weekly progress report as HTML" → value is in the `.html`

## Why Conversation-Transcript Judging Fails Here

If you judge a PPT-skill by the conversation transcript:
- A model that says "here's a perfect presentation" (but generates garbage) scores HIGH
- A model that honestly says "I need more information" (and produces nothing) scores LOW
- The 5-dim rubric (rigor/evidence/actionability/risk/signal-to-noise) is measuring the WRONG THING

## Protocol

### Phase 1: Extract output format from skill

Read SKILL.md body → identify:
- What file type does the skill produce? (pptx, html, tsx, pdf, ...)
- What's the typical user prompt? (extract from examples in the body)
- What "good" looks like? (extract quality criteria from the body — if none, use defaults below)

### Phase 2: Create standard creative brief

Generate 3 diverse, realistic creative briefs that would trigger this skill. Each brief:
- Specifies a clear deliverable
- Is ≤200 words
- Does NOT leak evaluation criteria

### Phase 3: Generate both arms

```
Bare:  API call (no skill) + "Create [brief description]"
Armed: API call (with skill) + the full creative brief
```

CRITICAL: Both arms must produce **actual files**. The model must be in a mode/tool configuration that can output the target format (e.g., python-pptx for PowerPoint, file-writing for HTML).

### Phase 4: Collect artifacts

From each arm, collect the **output file**, not the conversation transcript.
Store them for blind comparison.

### Phase 5: Judge artifacts (not transcripts)

Track B uses its OWN 5-dim rubric:

| Dimension | 0 | 10 |
|-----------|-----|-----|
| **Structure** (0-10) | Random order, no hierarchy | Clear information architecture, logical flow, good use of sections/headings |
| **Visual/Format Quality** (0-10) | Plain text dump into file | Appropriate use of layout, spacing, visual hierarchy, color (if applicable) |
| **Completeness** (0-10) | Missing major sections, obvious gaps | All key information present, nothing critical missing |
| **Usability** (0-10) | Receiver can't use this without major rework | Ready to present/ship immediately |
| **Professionalism** (0-10) | Looks amateurish or broken | Matches professional standards for the domain |

Judge prompt:

```
You are evaluating two {file_type} files. You do NOT know which was created
with a skill and which was created without.

## Creative Brief
{the task description}

## File A
{file content or description}

## File B
{file content or description}

Rate each file on: Structure (0-10), Visual Quality (0-10), Completeness (0-10),
Usability (0-10), Professionalism (0-10).

Output JSON: {"file_a": {dimensions...}, "file_b": {dimensions...}}
```

## Implementation Requirements

- File generation tool access (python-pptx, or a VFS that stores generated files)
- Judge that can evaluate structured output (not just conversation text)
- Per-file-format quality defaults (a "good PPT" and a "good HTML page" are different things)

## Open Questions

- How to handle file formats the judge can't interpret (binary .pptx)?
  → Option A: Have the model output an HTML preview alongside the file
  → Option B: Extract text/structure from the file programmatically
- What if the skill's value is partially in the conversation AND partially in the output?
  → Run BOTH Track A and Track B, report both scores
