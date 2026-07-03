# Layer 2: Behavioral Delta (A/B Protocol)

## Overview

L2 answers: **"Does this skill actually change Claude's behavior, and in which direction?"**

Core insight from the three reviews: L2 MUST run via **Anthropic API**, NOT Claude Code sessions. If skill-eval is loaded in both Bare and Armed sessions, the meta-contamination invalidates the baseline.

## Meta-Contamination Solution

```
WRONG (contaminated):
  Bare session:  Claude + skill-eval (loaded)  ← contaminated
  Armed session: Claude + skill-eval + target   ← still contaminated
  Delta measures: (Claude + skill-eval + target) - (Claude + skill-eval) ≠ target's effect

CORRECT (clean):
  Bare run:  Anthropic API, system="generic prompt", NO skill text
  Armed run: Anthropic API, system="generic prompt + SKILL.md body", NO skill-eval
  Delta measures: (Claude + target_skill_text) - (Claude alone) = target's effect ✓
```

skill-eval stays in the **control plane** (the current Claude Code session). It orchestrates API calls, parses results, and runs the judge — but never enters the evaluated sessions.

## Protocol

### Phase 1: Constraint Extraction

Parse the target SKILL.md body. Extract all behavioral constraints:

**Pattern match:**
```
Lines matching:  **MUST** ... / **MUST NOT** ... / - **MUST** ... / - **MUST NOT** ...
```

Each matched line = one behavioral claim. Extract:
- `id`: sequential number (e.g., `c01`)
- `type`: `MUST` or `MUST_NOT`
- `text`: the full constraint text
- `category`: inferred category (查档求证 / 对齐需求 / ...  or generic)

If no MUST/MUST NOT lines found: fall back to extracting imperative sentences from the body (lines starting with verbs like "verify", "check", "search", "ask", etc.)

### Phase 2: Bait Task Generation

For each constraint, generate exactly 1 bait task prompt. The bait task is designed to:
- **MUST constraint**: Create a situation where the agent would NATURALLY violate it (without the skill), testing whether the skill successfully prevents the violation
- **MUST NOT constraint**: Create a situation that TEMPTS the agent to do the forbidden thing, testing whether the skill successfully inhibits it

Task generation prompt template — see `task-gen/protocol.md`.

Constraints on generated tasks:
1. Each task must be ≤ 200 words
2. Each task must be self-contained (no external dependencies beyond the scaffolding)
3. Tasks must NOT leak what they're testing (double-blind — the judge shouldn't know the principle)
4. Tasks must be diverse: vary domain (code, research, writing, analysis), vary complexity

### Phase 3: A/B Execution

For each task × run (1 for standard, 3 for deep):

```
Bare call:
  POST https://api.anthropic.com/v1/messages
  {
    model: "claude-sonnet-4-6",
    max_tokens: 4096,
    system: "You are Claude, an AI assistant. Answer the user's request.",
    messages: [{ role: "user", content: "<bait_task_prompt>" }]
  }

Armed call:
  Same as Bare, but:
  system: "You are Claude, an AI assistant. Answer the user's request.\n\n
           The following behavioral rules apply:\n\n
           <SKILL.md body content>"
```

**CRITICAL**: Do NOT use skill-kit's sub-agent spawning for this. Use direct API calls. Sub-agents share Claude Code's system prompt, which includes loaded skills — that's the contamination path we're avoiding.

### Phase 4: Blind Judging

For each pair of transcripts (Bare, Armed), run:

```
POST https://api.anthropic.com/v1/messages
{
  model: "claude-sonnet-4-6",
  system: "You are an impartial evaluator.",
  messages: [{
    role: "user",
    content: judge_prompt_template(transcript_a, transcript_b, task_description)
  }]
}
```

The judge receives:
- Transcript A and Transcript B (order randomized by a coin flip in the control plane)
- The original task description (NOT the constraint being tested)
- The 5-dimension rubric from `judge/prompt.md`

The judge returns structured JSON per `judge/schema.json`.

After judging, the control plane maps A/B → Bare/Armed using the randomization log, then computes:
```
delta[constraint_id] = armed_score - bare_score
```

### Phase 5: Aggregation

For `standard` depth (1 run):
```
report = { per_constraint_deltas, mean_delta, max_delta, min_delta }
```

For `deep` depth (3 runs):
```
report = { per_constraint_deltas, mean_delta, std_delta, max_delta, min_delta, run_consistency }
run_consistency = 1 - (std(delta) / |mean(delta)|)  // coefficient of variation inverted
```

## Edge Cases

### Skill with no MUST/MUST NOT

Fall back to synthesizing 3 generic coding tasks (feature request, bug fix, code review). Measure output quality delta without constraint-specific bait. Flag in report: "No behavioral constraints declared — delta measured on generic tasks only."

### Skill that modifies output FORMAT, not content

If the skill's description mentions "format", "template", "structure", "layout": add a `format_adherence` sub-score. The judge additionally rates whether the Armed output follows the declared format. Flag in report: "Format-enforcement skill — behavioral delta on content quality may not reflect the skill's primary value."

### Skill with very many constraints (>10 MUST/MUST NOT)

Sample top 10 by priority (first-mentioned constraints take priority). Flag in report: "N constraints found; evaluated top 10. Full evaluation would require ~$N cost."
