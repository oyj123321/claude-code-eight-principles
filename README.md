# Claude Code Eight Principles · 八荣八耻

<p align="center">
  <strong>🇨🇳 中文</strong> &nbsp;|&nbsp;
  <strong>🇬🇧 English</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6C4DFF?style=flat-square&logo=claude" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" alt="Version 1.0.0">
</p>

---

A Claude Code skill that enforces engineering discipline through eight behavioral principles — inspired by the "Eight Honors & Eight Shames" (八荣八耻) framework. This skill runs as a persistent behavioral constraint across all coding tasks, ensuring Claude follows best practices before writing a single line of code.

一套以"八荣八耻"为框架的 Claude Code 行为约束技能，将编码工作准则固化为 AI 编程助手的自动行为规范，在所有编码任务中持续生效。

---

## Table of Contents · 目录

- [The Eight Principles · 八条准则](#the-eight-principles--八条准则)
- [Why This Exists · 为什么需要它](#why-this-exists--为什么需要它)
- [Installation · 安装](#installation--安装)
- [Usage · 使用](#usage--使用)
- [Repository Structure · 仓库结构](#repository-structure--仓库结构)
- [Contributing · 贡献](#contributing--贡献)
- [License · 许可](#license--许可)

---

## The Eight Principles · 八条准则

| # | Honor · 荣 | Shame · 耻 | Core Constraint · 核心约束 |
|---|------------|------------|---------------------------|
| 1 | 查档求证<br><small>Verify Before Assuming</small> | 臆猜接口<br><small>Guessing Interfaces</small> | API/参数以实际代码为准，不凭记忆猜测<br><small>Base API usage on actual code, not memory</small> |
| 2 | 对齐需求<br><small>Align Before Building</small> | 模糊开工<br><small>Vague Kickoffs</small> | 需求不清时确认，不自行脑补<br><small>Confirm ambiguous requirements, don't fill gaps</small> |
| 3 | 请示规则<br><small>Ask About Business Rules</small> | 脑补业务<br><small>Fabricating Domain Logic</small> | 业务逻辑向人确认，不自行假设<br><small>Confirm business rules with humans, don't assume</small> |
| 4 | 复用存量<br><small>Reuse Existing Code</small> | 新增冗余<br><small>Adding Redundancy</small> | 先搜已有实现，不重复造轮子<br><small>Search before creating, don't reinvent the wheel</small> |
| 5 | 完备测例<br><small>Complete Test Cases</small> | 省略校验<br><small>Skipping Edge Cases</small> | 边界/错误/空值全量覆盖<br><small>Cover boundaries, errors, nulls, not just happy path</small> |
| 6 | 恪守规范<br><small>Follow Conventions</small> | 乱改架构<br><small>Arbitrary Refactoring</small> | 遵循项目 conventions，不凭偏好重构<br><small>Follow project patterns, don't refactor on preference</small> |
| 7 | 坦诚存疑<br><small>Admit Uncertainty</small> | 不懂装懂<br><small>Pretending to Know</small> | 不确定就说，不编造答案<br><small>Say "I'm not sure", don't fabricate answers</small> |
| 8 | 分步迭代<br><small>Iterate Incrementally</small> | 批量乱改<br><small>Bulk Chaotic Changes</small> | 小步可验证，不一口气改多模块<br><small>Small verifiable steps, not mass changes</small> |

---

## Why This Exists · 为什么需要它

**The problem:** In day-to-day coding, AI assistants commonly exhibit problematic behaviors:

| Problem | Example |
|---------|---------|
| Guessing APIs from memory | Using `foo.bar()` without ever reading `foo`'s definition |
| Filling in vague requirements | Assuming "add auth" means JWT when the user meant OAuth |
| Fabricating business logic | Deciding a discount rule is 10% without asking |
| Reinventing the wheel | Writing a date parser when the project already has one |
| Happy-path-only thinking | Forgetting null checks, error handling, empty states |
| Arbitrary refactoring | Renaming all files to match personal preference |
| Hallucinating answers | Giving a confident but entirely wrong explanation |
| Bulk destructive changes | Editing 15 files in one go, breaking 8 of them |

**The fix:** This skill loads the Eight Principles as always-on behavioral constraints, so Claude self-corrects before these patterns emerge.

**AI 助手常见问题：** 凭记忆猜接口、脑补需求、重复造轮子、只写 happy path、不懂装懂、一口气改十几个文件。这个 skill 将八条准则作为持续生效的行为约束加载到 Claude Code 中，让 Claude 在每个任务中自动遵循最佳实践。

---

## Installation · 安装

### Method 1: Git Clone (Recommended)

```bash
# Clone the repository
git clone https://github.com/oyj123321/claude-code-eight-principles.git

# Link into Claude Code skills — project-level (current project only)
mkdir -p .claude/skills
# Linux / macOS
ln -s $(pwd)/claude-code-eight-principles .claude/skills/eight-principles
# Windows (PowerShell, as Administrator)
New-Item -ItemType SymbolicLink -Path .claude/skills/eight-principles -Target (Resolve-Path claude-code-eight-principles)

# Or: user-level (all projects)
# Linux / macOS
ln -s $(pwd)/claude-code-eight-principles ~/.claude/skills/eight-principles
```

### Method 2: OpenSkills

```bash
npx openskills install oyj123321/claude-code-eight-principles
```

### Method 3: Manual Copy

```bash
cp -r claude-code-eight-principles .claude/skills/eight-principles
```

---

## Usage · 使用

**Automatic activation · 自动激活:** The skill activates automatically on coding tasks, code reviews, or when keywords like "engineering discipline", "coding standards", or "八荣八耻" are mentioned.

**Manual invocation · 手动调用:**
```
/eight-principles
```

Once loaded, the eight behavioral directives constrain all subsequent actions in the session. Claude will:
- Search the codebase before using any API
- Ask clarifying questions instead of assuming
- Reuse existing code instead of duplicating
- Cover edge cases in tests
- Follow project conventions
- Admit uncertainty honestly
- Break work into small, verifiable steps

---

## Repository Structure · 仓库结构

```
claude-code-eight-principles/
├── SKILL.md          # Core skill file · 核心技能文件 (Claude Code entry point)
├── README.md         # This document · 本文档 (bilingual human-readable docs)
├── CHANGELOG.md      # Version history · 版本历史
├── LICENSE           # MIT License · MIT 许可
└── .gitignore        # Git ignore rules
```

---

## Contributing · 贡献

This skill is intentionally minimal — eight principles, eight directives. If you have ideas for improvement:

1. Open an issue to discuss before submitting a PR
2. Keep the SKILL.md under 200 lines (Claude Code has description budget limits)
3. Maintain full bilingual parity — every Chinese sentence needs an English equivalent, and vice versa

Contributions are welcome under the MIT license.

---

## License · 许可

MIT — see [LICENSE](./LICENSE) for full text.

随意使用、修改、分发。Use freely, modify, distribute.
