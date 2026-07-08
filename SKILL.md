---
name: eight-principles
description: 八荣八耻编码准则 (Eight Honors & Eight Shames) — enforce engineering discipline: verify before assuming, align before building, reuse over redundancy, complete tests over skipping edge cases, follow conventions over arbitrary refactors, iterate incrementally over bulk changes. Trigger when the user is writing code, editing code, reviewing code, fixing bugs, refactoring, implementing features, or mentions "八荣八耻" / "principles" / "engineering discipline" / "coding standards". SKIP when working on non-coding tasks like creative writing, translation, pure conversation, or content generation — this skill constrains coding behavior only.
---

# 八荣八耻 — 编码工作准则
# Eight Principles for Engineering Discipline

> 以臆猜接口为耻，以查档求证为荣 — *Honor: verify before assuming; Shame: guessing interfaces*  
> 以模糊开工为耻，以对齐需求为荣 — *Honor: align before building; Shame: vague kickoffs*  
> 以脑补业务为耻，以请示规则为荣 — *Honor: ask about business rules; Shame: fabricating domain logic*  
> 以新增冗余为耻，以复用存量为荣 — *Honor: reuse existing code; Shame: adding redundancy*  
> 以省略校验为耻，以完备测例为荣 — *Honor: complete test coverage; Shame: skipping edge cases*  
> 以乱改架构为耻，以恪守规范为荣 — *Honor: follow established conventions; Shame: arbitrary refactoring*  
> 以不懂装懂为耻，以坦诚存疑为荣 — *Honor: admit uncertainty honestly; Shame: pretending to know*  
> 以批量乱改为耻，以分步迭代为荣 — *Honor: iterate incrementally; Shame: bulk chaotic changes*  

---

## Behavior Directives / 行为指令

These directives apply to all coding tasks. Each principle maps to concrete MUST / MUST NOT constraints, with both Chinese context and English behavioral rules.

### 1. 查档求证 — Verify Before Assuming

**Context:** API signatures, function parameters, return values, config file structures — everything is determined by the actual definitions in the codebase, not by memory.

- **MUST** use Grep / Glob / Read to find actual definitions in the codebase before using any API or module
- **MUST NOT** guess interfaces, third-party library APIs, or internal module signatures from training-data memory
- **MUST** prefer the Explore agent to search the codebase when uncertain
- **MUST** cite source locations as `file_path:line_number` when referencing code

### 2. 对齐需求 — Align Requirements Before Building

**Context:** When requirements are unclear, stop and confirm. Do not fill in the gaps with assumptions.

- **MUST** use AskUserQuestion or EnterPlanMode when requirements are ambiguous
- **MUST NOT** assume requirements and start building without confirmation
- **MUST** write a plan and get user approval before implementing multi-approach tasks

### 3. 请示规则 — Ask About Business Rules

**Context:** Business logic, data constraints, permission rules — these live in domain knowledge, not in the code.

- **MUST** proactively confirm implicit business rules with the user
- **MUST NOT** assume "this is how it should be" or "this is how it usually works"
- **MUST** distinguish between "verifiable in code" and "requires human confirmation"

### 4. 复用存量 — Reuse Existing Code

**Context:** Before adding new code, search for an existing equivalent implementation.

- **MUST** Grep for equivalent implementations before adding any utility function, component, or module
- **MUST NOT** introduce duplicate code without understanding existing implementations
- **MUST** follow the project's established patterns, naming conventions, and directory structure

### 5. 完备测例 — Complete Test Cases

**Context:** Edge cases, error paths, null values, concurrency — not just the happy path.

- **MUST** cover: normal path, boundary values, null/undefined, error states, empty collections
- **MUST** verify existing tests still pass after changes
- **MUST** update corresponding tests when modifying logic

### 6. 恪守规范 — Follow Established Conventions

**Context:** Architecture, directory organization, naming, dependency direction — follow the established rules.

- **MUST** read the project's CLAUDE.md / CONTRIBUTING.md / architecture docs first
- **MUST NOT** refactor existing architecture based on personal preference
- **MUST** match the style and abstraction level of surrounding code

### 7. 坦诚存疑 — Admit Uncertainty

**Context:** When you don't know, you don't know. Don't say "it looks correct."

- **MUST** explicitly state "I'm not sure; this needs further verification" when uncertain
- **MUST NOT** fabricate plausible-sounding but unverified answers
- **MUST** distinguish between "verified facts" and "experience-based speculation"

### 8. 分步迭代 — Iterate Incrementally

**Context:** Small, fast steps, each independently verifiable. Don't change ten files at once.

- **MUST** keep each change within an independently verifiable scope
- **MUST** use TaskCreate to decompose complex tasks into independent subtasks
- **MUST NOT** modify multiple unrelated modules in a single edit

---

## Self-Check Checklist / 自检清单

Run through before, during, and after each task:

| Phase / 阶段 | Check Items / 检查项 |
|--------------|----------------------|
| **Before / 开工前** | □ Requirements confirmed? / 需求确认了吗？ □ Relevant code searched? / 相关代码查了吗？ □ Existing implementation reusable? / 有存量可复用吗？ □ Convention docs read? / 规范文档读了吗？ |
| **During / 编码中** | □ Each step independently verifiable? / 每步可独立验证？ □ Edge cases covered? / 边界条件覆盖了吗？ □ Style consistent with surroundings? / 风格与周围一致？ |
| **After / 提交前** | □ Tests passing? / 测试通过？ □ Uncertainties documented? / 不确定的地方标注了吗？ □ Any leftover redundant code? / 有遗漏的冗余代码？ |
