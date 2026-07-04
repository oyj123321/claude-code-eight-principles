# Eval Directory · 评估目录

八荣八耻 skill 的评估资源。

## 目录结构

```
eval/
├── tasks/                   ← 8 个按八条原则设计的诱饵任务
│   ├── 01-verify-before-assuming.md
│   ├── 02-align-requirements.md
│   ├── 03-ask-business-rules.md
│   ├── 04-reuse-existing.md
│   ├── 05-complete-tests.md
│   ├── 06-follow-conventions.md
│   ├── 07-admit-uncertainty.md
│   └── 08-iterate-incrementally.md
│
├── scaffolding/             ← 任务 4、5、6 的测试环境
│   ├── 04-email-validator/
│   ├── 05-date-parser/
│   └── 06-convention-project/
│
└── evals/
    └── eight-principles/
        ├── report.md                 ← 完整评估报告
        ├── api_l2_results.json       ← v0.1 原始数据（无工具）
        └── api_l2_with_tools.json    ← v0.2 原始数据（有工具，19 API calls）
```

## 如何运行评估

此仓库的评估使用独立工具 **[skill-eval](https://github.com/oyj123321/skill-eval)**：

```bash
git clone https://github.com/oyj123321/skill-eval.git
cd skill-eval
python run_l2.py --skill-path ../claude-code-eight-principles --tasks c01,c08 --depth standard
```

## 评估结果摘要

| 约束 | Bare | Armed | Δ | 数据 |
|------|------|-------|-----|------|
| 查档求证 | 9/50 | 43/50 | **+34** | `api_l2_with_tools.json` |
| 分步迭代 | 5/50 | 46/50 | **+41** | `api_l2_with_tools.json` |

完整分析见 [`evals/eight-principles/report.md`](evals/eight-principles/report.md)。
