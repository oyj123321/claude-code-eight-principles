---
name: skill-eval
description: Evaluate any Claude Code skill with evidence — classify the skill type, then run the correct evaluation track: behavioral delta (Track A), output artifact quality (Track B), format compliance (Track C), tool correctness (Track D), or knowledge accuracy (Track E). Triggers on "evaluate this skill" / "benchmark" / "is this skill worth installing" / "skill-eval".
argument-hint: "<path-to-skill-dir> [--depth quick|standard|deep]"
---

# skill-eval — Meta Skill Evaluator

Evaluate a Claude Code skill and answer: **"What does this skill actually change? Is the cost worth it?"**

## The core problem: not all skills are the same type

A skill that teaches Claude to "search before answering" changes **behavior**.  
A skill that makes Claude produce **well-structured PPTs** creates **output artifacts**.  
A skill that enforces **code formatting rules** imposes **format constraints**.  
A skill that wraps a **CLI tool** provides **tool access**.  
A skill that contains **company documentation** adds **knowledge**.

**Judging them all on the same rubric is wrong.** A PPT-skill's value is in the `.pptx` file it produces, not in how "rigorous" its conversation transcript looks.

---

## Architecture

```
INPUT: SKILL.md path
  │
  ├─ L0: Skill Classifier
  │   │  Parse description + body → determine skill type(s)
  │   │  Map to the correct evaluation track (A/B/C/D/E)
  │   │  If no track available → report "unable to evaluate this type"
  │   │  See layers/classifier.md
  │
  ├─ L1: Structural Compliance (all types, free, <2s)
  │   └─ skill-kit 21 checks + 11 anti-patterns → structural score
  │
  └─ L2: Tracked Evaluation ($ varies by track)
      │
      ├─ Track A: Behavioral (🧠)         ✅ IMPLEMENTED
      │   └─ Bait tasks → API A/B → judge transcripts
      │   └─ See layers/behavioral.md
      │
      ├─ Track B: Output Artifact (🎨)    📋 DESIGN
      │   └─ Same creative task → collect output FILE (pptx/html/tsx)
      │   └─ Judge artifact quality, not conversation
      │   └─ See layers/track-output.md
      │
      ├─ Track C: Format Compliance (📐)  📋 DESIGN
      │   └─ Extract format rules from SKILL.md
      │   └─ Automated lint + judge: format adherence vs content quality
      │   └─ See layers/track-format.md
      │
      ├─ Track D: Tool Correctness (🔧)   📋 DESIGN
      │   └─ Execute every documented command/script
      │   └─ Metrics: success rate, correct output, error handling
      │   └─ See layers/track-tool.md
      │
      └─ Track E: Knowledge Accuracy (📚) 📋 DESIGN
          └─ Extract claimed facts from references/
          └─ Judge: accuracy, completeness, source traceability
          └─ See layers/track-knowledge.md

Report: structural score + track results + cost + verdict
```

## Skill Type Classification (L0)

The classifier reads the skill's description + body, then routes to the right track.  
See `layers/classifier.md` for the full classification table and signal patterns.

```
IF body mentions pptx/pptx/slide/deck/presentation/ui/component/css/html → Track B
IF body mentions format/template/lint/style/convention/naming → Track C
IF body mentions script/run/execute/command/cli/bin/bash → Track D
IF body is mostly knowledge docs in references/ → Track E
IF body has MUST/MUST NOT behavioral directives → Track A
ELSE → Track A (default)
```

A skill can span **multiple tracks**. Example: an "enterprise PPT" skill might be Track B (produces PPTs) + Track C (follows company template format). Each track reports independently.

**Critical honesty rule:** if the skill hits a track we haven't implemented yet, say so explicitly:

```
"Skill type: Output Artifact (Track B)
 Status: ⚠️ Track B evaluation is DESIGNED but NOT YET IMPLEMENTED.
 Current eval: L1 structural only.
 Recommendation: manual review of output quality until Track B ships."
```

## Depth Levels

| Depth | Layers | Est. Cost | Use When |
|-------|--------|-----------|----------|
| `quick` | L0 + L1 | Free | Every edit — "is this SKILL.md well-formed?" |
| `standard` | L0 + L1 + L2 (1 run) | ~$1-2 | PR review — "does this skill actually work?" |
| `deep` | L0 + L1 + L2 (3 runs) | ~$4-6 | Pre-release — "how reliable is the measurement?" |

## Usage

```
/skill-eval .claude/skills/eight-principles                # standard (default)
/skill-eval .claude/skills/eight-principles --depth quick   # structural only
/skill-eval .claude/skills/eight-principles --depth deep    # × 3 runs
```

## Workflow

### Step 0: Classify

Read SKILL.md. Classify into Track(s) A/B/C/D/E. See `layers/classifier.md`.

If the skill maps to an unimplemented track → report honestly, stop L2, recommend manual review.

### Step 1: L1 — Structural Compliance

Run `check-skill` from skill-kit (external) + 11 anti-pattern scan. See `layers/static.md`.

Output: PASS/FAIL + letter grade.  
Gate: FAIL → stop. Fix SKILL.md first.

### Step 2: L2 — Tracked Evaluation

Select track based on L0 result. Each track has its own protocol:

- **Track A (Behavioral)** — see `layers/behavioral.md`
- **Track B (Output Artifact)** — see `layers/track-output.md`
- **Track C (Format)** — see `layers/track-format.md`
- **Track D (Tool)** — see `layers/track-tool.md`
- **Track E (Knowledge)** — see `layers/track-knowledge.md`

### Step 3: Cost Analysis

Same across all tracks:
- SKILL.md token count + budget share
- Track-specific overhead (e.g., Track B: extra API calls for file generation)
- False positive rate

### Step 4: Report

Output a structured report. Fields vary by track, but the skeleton is the same.

---

## Track Implementation Status

| Track | What it evaluates | Status | Since |
|-------|-------------------|--------|-------|
| A — Behavioral | 🧠 Skills that change HOW Claude thinks/acts | ✅ Implemented | v0.2 |
| B — Output Artifact | 🎨 Skills that produce files (PPT, UI, report) | 📋 Designed | — |
| C — Format | 📐 Skills that enforce style/template/structure | 📋 Designed | — |
| D — Tool | 🔧 Skills that wrap scripts/commands | 📋 Designed | — |
| E — Knowledge | 📚 Skills that provide reference information | 📋 Designed | — |

## Limitations

- **Single-model**: Tests on the model configured in API calls. Future: `--model` flag.
- **Task synthesis bias**: Bait tasks generated by the same model being evaluated.
- **Tracks B-E not yet implemented**: Only Track A produces behavioral delta scores today.
- **Unknown skill types**: The classifier may misclassify. When uncertain, it defaults to Track A + a warning.

## Relationship to Other Tools

```
skill-kit:      structural well-formedness, trigger accuracy, auto-iteration
PluginEval:     multi-dim quality scoring, anti-patterns, Monte Carlo stats
skill-eval:     type-aware evaluation across 5 tracks
                └── L1 reuses skill-kit (external dependency)
                └── Track A = behavioral delta (unique to skill-eval)
                └── Tracks B-E = filling gaps neither tool addresses
```
