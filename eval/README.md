# Eval Directory · 评估目录

This directory contains two things:

1. **`skill-eval/`** — A meta skill evaluator. Load it into Claude Code to evaluate ANY skill (not just 八荣八耻).
2. **`tasks/` + `scaffolding/`** — 8 bait tasks and scaffolding projects originally designed for 八荣八耻 eval. These are also usable as custom task sets for skill-eval.

## Quick Start · 快速开始

```bash
# Evaluate a skill (default: standard depth, L1 + L2)
/skill-eval .claude/skills/eight-principles

# Structural only (free, <2s)
/skill-eval .claude/skills/eight-principles --depth quick

# Behavioral × 3 runs (~$4-6)
/skill-eval .claude/skills/eight-principles --depth deep
```

## Architecture

```
eval/
├── skill-eval/              ← Meta skill evaluator (the thing you use)
│   ├── SKILL.md             ← Entry point — load into Claude Code
│   ├── layers/
│   │   ├── static.md        ← L1: structural compliance (skill-kit + anti-patterns)
│   │   └── behavioral.md    ← L2: behavioral delta (API-based A/B)
│   ├── judge/
│   │   ├── prompt.md        ← Blind judge prompt (5-dim rubric)
│   │   └── schema.json      ← Judge output schema
│   ├── task-gen/
│   │   └── protocol.md      ← MUST/MUST NOT → bait task synthesis
│   └── scoring.md           ← 3-dim scoring + letter grade table
│
├── tasks/                   ← 8 bait tasks (by principle, for 八荣八耻)
│   ├── 01-verify-before-assuming.md
│   ├── 02-align-requirements.md
│   ├── ...
│   └── 08-iterate-incrementally.md
│
├── scaffolding/             ← Test environments for tasks 4, 5, 6
│   ├── 04-email-validator/
│   ├── 05-date-parser/
│   └── 06-convention-project/
│
├── evals/                   ← Evaluation reports for specific skills
│   └── eight-principles/
│       └── report.md
│
└── judge/                   ← (DEPRECATED: old manual judge. Use skill-eval/judge/ instead)
    ├── rubric.md
    ├── schema.json
    └── prompt.md
```

## How Skill-Eval Differs From Manual Eval

| | Manual Eval (old) | skill-eval (new) |
|---|---|---|
| Task generation | 8 hand-written tasks for 八荣八耻 | Auto-generated from SKILL.md MUST/MUST NOT |
| Execution | Manual Claude Code sessions | API-based (no meta-contamination) |
| Judging | Manual prompt copy-paste | Automated blind judging |
| Scope | 八荣八耻 only | Any skill |
| Cost | Free (your time) | ~$1-2 per standard eval |

## Relationship to Other Tools

skill-eval is designed to **complement**, not replace:
- **[skill-kit](https://github.com/mjenkinsx9/skill-kit)**: skill-eval's L1 calls `check-skill` as an external dependency. skill-kit covers structural well-formedness; skill-eval adds behavioral delta.
- **[PluginEval](https://github.com/wshobson/agents)**: PluginEval does multi-dim quality scoring with statistical rigor. skill-eval focuses on the one dimension both miss: measured behavioral change with cost analysis.
- **[Bench My Harness](https://www.npmjs.com/package/bench-my-harness)**: BMH does Codex vs Claude Code comparison. skill-eval does skill vs no-skill comparison. Different A/B axis.

## Contributing

To add eval for a new skill:
1. Copy `scoring.md`'s report template
2. Run `/skill-eval path/to/skill --depth standard`
3. Save the report in `evals/<skill-name>/report.md`
