# Layer 0: Skill Type Classifier

## Overview

Before evaluating a skill, determine WHAT TYPE it is. A PPT-skill's value is in the `.pptx` file, not in conversation transcripts. Classifying wrong means measuring the wrong thing.

## Classification Signals

Read the SKILL.md's `description` field and body. Each signal maps to one or more tracks.

### Track A — Behavioral (🧠)

The skill constrains or redirects HOW Claude thinks/acts during a conversation.

**Primary signals:**
- Body has explicit `MUST`/`MUST NOT`/`ALWAYS`/`NEVER` behavioral directives
- Description uses action verbs: "verify", "search", "ask", "decompose", "check", "confirm"
- Body describes *process* changes: "before writing code, first..."
- Body references Claude Code tools: Grep, Read, AskUserQuestion, EnterPlanMode, TaskCreate

**Examples:** eight-principles, code-review standards, any "before you do X, do Y" skill

### Track B — Output Artifact (🎨)

The skill produces *files* or *visual output* whose quality is independent of conversation quality.

**Primary signals:**
- Description or body mentions output formats: `pptx`/`pptx`/`slide`/`deck`/`presentation`
- Body mentions UI output: `html`/`css`/`component`/`ui`/`button`/`layout`/`page`/`screen`
- Body mentions report/document output: `report`/`document`/`proposal`/`diagram`/`chart`
- Description includes creative verbs: "create", "design", "generate", "build a..."

**Examples:** PPT master, UI component generator, report writer, diagram creator

### Track C — Format Compliance (📐)

The skill enforces output *structure* or *style* rather than content quality.

**Primary signals:**
- Body mentions: `format`/`template`/`lint`/`style`/`convention`/`naming`/`standard`
- Body prescribes specific output shapes: "responses MUST use `<format>` blocks"
- Description emphasizes consistency: "ensures", "enforces", "follows the pattern"
- Skill's value proposition is uniformity, not creativity

**Examples:** code style enforcer, commit message formatter, document template

### Track D — Tool Correctness (🔧)

The skill wraps executable code or shell commands.

**Primary signals:**
- Body mentions: `script`/`run`/`execute`/`command`/`cli`/`bin`/`bash`/`python`
- Skill directory has `scripts/` or `bin/` directory
- Body documents commands users should type: `npx`/`uv run`/`python`/`curl`
- Description says "run", "execute", "invoke", "call"

**Examples:** screenshot tool, deployment script, API wrapper, database migrator

### Track E — Knowledge Accuracy (📚)

The skill's primary value is in REFERENCE INFORMATION, not behavioral instructions.

**Primary signals:**
- Body is >60% reference content (domain facts, API docs, company policies)
- Skill directory has `references/` with substantial content (not just process docs)
- Description mentions "knowledge", "reference", "guide", "documentation", "policy"
- Body's process instructions are minimal; the meat is in what Claude should KNOW

**Examples:** company style guide, API reference, architecture decision records, regulatory rules

## Classification Algorithm

```
For each track A..E, compute a confidence score based on signal hits.

confidence[t] = (signal_hits[t] / max_signals_for_track[t]) * 0.8
              + (0.2 if description explicitly mentions track keywords else 0)

tracks = [t for t in A..E if confidence[t] > 0.3]

If len(tracks) == 0: default to Track A with warning
If len(tracks) > 0:  run each applicable track, report independently

Primary track = track with highest confidence
```

## Multi-track Skills

A skill can span multiple tracks. One track is always PRIMARY:

| Skill | Primary Track | Secondary Track | Why |
|-------|---------------|-----------------|-----|
| Corporate PPT creator | B (Output) | C (Format) | Produces PPT files, but also enforces brand template |
| Code reviewer with lint | A (Behavioral) | C (Format) | Changes review behavior, but also checks style |
| CLI tool with docs | D (Tool) | E (Knowledge) | Wraps a command, but also provides usage docs |

Each track produces its own score. The report shows all of them.

## Edge Cases

### Truly multi-purpose skills
A skill that claims to do EVERYTHING ("generates beautiful PPTs, writes clean code, answers questions, runs your CI pipeline"). The classifier will flag this as an `OVER_SCOPED` anti-pattern (already caught by L1). Confidence across multiple tracks will be moderate-low, and L2 will produce noisy results. The report should flag: "This skill claims too many things. Narrow its scope before meaningful evaluation is possible."

### Skills with NO detectable type
Some skills are just "be more helpful" or "you are an expert at X." These lack behavioral directives, output format specs, tool wrappers, or knowledge content. Default to Track A with a warning: "No specific behavioral constraints detected. Delta measurement may show zero effect."

### Skills where the type is clear but track is unimplemented
If the classifier confidently identifies the skill as Track B, but Track B isn't implemented yet: stop L2, report "Type identified but evaluation track not yet available." Do NOT silently downgrade to Track A — that would produce misleading scores.

## Output Format

```json
{
  "layer": "L0",
  "classification": {
    "primary_track": "A",
    "all_tracks": ["A"],
    "confidence": {
      "A": 0.85,
      "B": 0.10,
      "C": 0.05,
      "D": 0.00,
      "E": 0.00
    },
    "reasoning": "Skill has 25 MUST/MUST NOT behavioral directives; no output format, tool, or knowledge signals detected.",
    "unimplemented_tracks": []
  },
  "warning": null
}
```
