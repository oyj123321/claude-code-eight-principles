# Claude Code Eight Principles（八荣八耻）

一套 Claude Code 行为约束技能，以"八荣八耻"的形式将编码工作准则固化为 AI 编程助手的自动行为规范。

## 这是什么

在日常编码中，AI 助手常见的问题包括：
- 凭记忆猜测 API 签名，不查实际代码
- 需求不清时自行脑补，不向用户确认
- 重复造轮子，不复用已有实现
- 只写 happy path，忽略边界条件和错误处理
- 不懂装懂，给出 plausible 但错误的答案
- 一口气改几十个文件，出了问题难以定位

这个 skill 将八条核心准则作为**持续生效的行为约束**加载到 Claude Code 中，在每次任务中自动触发。

## 安装

### 方式一：直接 clone

```bash
git clone https://github.com/YOUR_USERNAME/claude-code-eight-principles.git
```

然后链接到 Claude Code 技能目录：

**项目级（仅当前项目生效）：**
```bash
mkdir -p .claude/skills
ln -s /path/to/claude-code-eight-principles .claude/skills/eight-principles
```

**用户级（所有项目生效）：**
```bash
mkdir -p ~/.claude/skills
ln -s /path/to/claude-code-eight-principles ~/.claude/skills/eight-principles
```

### 方式二：OpenSkills

```bash
npx openskills install YOUR_USERNAME/claude-code-eight-principles
```

## 使用

安装后自动生效，无需手动调用。Claude Code 会在编码任务中自动匹配此技能。

也可以手动调用：
```
/eight-principles
```

## 八条准则

| # | 荣 | 耻 | 核心约束 |
|---|-----|-----|----------|
| 1 | 查档求证 | 臆猜接口 | API/参数以实际代码为准，不凭记忆猜测 |
| 2 | 对齐需求 | 模糊开工 | 需求不清时确认，不自脑补 |
| 3 | 请示规则 | 脑补业务 | 业务逻辑向人确认，不自行假设 |
| 4 | 复用存量 | 新增冗余 | 先搜已有实现，不重复造轮子 |
| 5 | 完备测例 | 省略校验 | 边界/错误/空值全量覆盖 |
| 6 | 恪守规范 | 乱改架构 | 遵循项目 conventions，不凭偏好重构 |
| 7 | 坦诚存疑 | 不懂装懂 | 不确定就说，不编造答案 |
| 8 | 分步迭代 | 批量乱改 | 小步可验证，不一口气改多模块 |

## 许可

MIT — 随意使用、修改、分发。
