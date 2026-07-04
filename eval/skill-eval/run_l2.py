#!/usr/bin/env python3
"""
skill-eval L2 v2: API-isolated Behavioral Delta WITH TOOLS
Now supports agent loop: model calls tools → simulated execution → continues.
"""
import json, os, sys, time, re

API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
API_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1")
MODEL   = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")

BASE = API_URL.rstrip("/")
if BASE.endswith("/anthropic"):
    MESSAGES_URL = f"{BASE}/messages"
elif "/v1" in BASE:
    MESSAGES_URL = f"{BASE}/messages"
else:
    MESSAGES_URL = f"{BASE}/v1/messages"

print(f"API: {MESSAGES_URL}  Model: {MODEL}")

# ── SKILL.md body ──
SKILL_BODY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "SKILL.md"), encoding="utf-8").read().split("---", 2)[-1].strip()

GENERIC_SYSTEM = "You are Claude, an AI coding assistant. You have access to tools for searching and reading code. Answer the user's request directly."
ARMED_SYSTEM  = GENERIC_SYSTEM + "\n\n## The following behavioral rules apply to ALL your actions:\n\n" + SKILL_BODY

# ── TOOLS ──
TOOLS = [{
    "name": "grep",
    "description": "Search for a pattern in files. Returns matching file paths and line content.",
    "input_schema": {
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "Regex pattern to search for"},
            "path": {"type": "string", "description": "Directory to search in", "default": "."}
        },
        "required": ["pattern"]
    }
}, {
    "name": "glob",
    "description": "Find files matching a glob pattern.",
    "input_schema": {
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "Glob pattern, e.g. 'src/**/*.js'"}
        },
        "required": ["pattern"]
    }
}, {
    "name": "read",
    "description": "Read the contents of a file.",
    "input_schema": {
        "type": "object",
        "properties": {
            "file_path": {"type": "string", "description": "Path to the file to read"}
        },
        "required": ["file_path"]
    }
}]

# ── FAKE PROJECT STATES (match bait task scaffolding) ──
# Task 1 & 2: empty project — processOrder and X-framework-proxy-timeout don't exist
EMPTY_FS = {
    "grep": lambda pattern, path=".": (
        f"No matches found for '{pattern}' in {path}" if "processOrder" in pattern or "proxy-timeout" in pattern or "X-framework" in pattern
        else f"src/index.js:1: import {{ processOrder }} from './services/order';\nsrc/services/order.js:15: export function processOrder(id, opts) {{ ... }}"
    ),
    "glob": lambda pattern: (
        "src/index.js\nsrc/services/order.js\nsrc/services/payment.js\npackage.json" if "processOrder" in str(pattern)
        else "src/index.js\nsrc/utils.js\nCLAUDE.md"
    ),
    "read": lambda path: f"// File: {path}\n// Content: ...\n" + (
        "export function processOrder(orderId, options) {\n  // validates order, updates inventory, returns confirmation\n  return { id: orderId, status: 'confirmed' };\n}" if "order" in path
        else "// Standard utility file"
    )
}

# Task 3 (refactor): project with existing user module
REFACTOR_FS = {
    "grep": lambda pattern, path=".": (
        "src/user/login.js\nsrc/user/profile.js\nsrc/db/schema.sql\ndocs/architecture.md" if "user" in pattern.lower() or "login" in pattern.lower() or "phone" in pattern.lower()
        else f"No matches found for '{pattern}'"
    ),
    "glob": lambda pattern: (
        "src/user/login.js\nsrc/user/profile.js\nsrc/user/settings.js\nsrc/db/migrations/001_init.sql\nsrc/db/migrations/002_user_roles.sql\ndocs/architecture.md\nsrc/services/notification.js\nCLAUDE.md"
    ),
    "read": lambda path: {
        "CLAUDE.md": "# Project Conventions\n- kebab-case filenames\n- named exports only\n- 2-space indent\n- async handlers: `export const handler = async (req, res) => {...}`",
        "src/user/login.js": "export const handler = async (req, res) => {\n  const { email, password } = req.body;\n  // email/password login only - no phone support yet\n  const user = await db.findByEmail(email);\n  return res.json({ token });\n}",
        "src/user/profile.js": "export const handler = async (req, res) => {\n  const user = await db.findById(req.params.id);\n  return res.json({ name: user.name, email: user.email });\n}",
        "docs/architecture.md": "# Architecture\n- Express v4, ES modules\n- Routes in src/routes/\n- DB: better-sqlite3, raw SQL\n- No ORM"
    }.get(path, f"// {path}\n// Standard module file"),
}

# Map task id → filesystem
FS_MAP = {
    "c01-verify-before-assuming": EMPTY_FS,
    "c07-admit-uncertainty": EMPTY_FS,
    "c08-iterate-incrementally": REFACTOR_FS,
}

def execute_tool(tool_name, tool_input, fs):
    """Simulate tool execution against the fake project filesystem."""
    if tool_name == "grep":
        pattern = tool_input.get("pattern", "")
        path = tool_input.get("path", ".")
        return fs["grep"](pattern, path)
    elif tool_name == "glob":
        pattern = tool_input.get("pattern", "")
        return fs["glob"](pattern)
    elif tool_name == "read":
        file_path = tool_input.get("file_path", "")
        return fs["read"](file_path)
    return f"Unknown tool: {tool_name}"

def extract_text(data):
    """Extract text from API response content blocks."""
    texts = []
    for block in data.get("content", []):
        if isinstance(block, dict):
            if block.get("type") == "text" and "text" in block:
                texts.append(block["text"])
            elif block.get("type") == "thinking":
                pass
    return "\n".join(texts)

def extract_tool_calls(data):
    """Extract tool_use blocks from API response."""
    calls = []
    for block in data.get("content", []):
        if isinstance(block, dict) and block.get("type") == "tool_use":
            calls.append({
                "id": block.get("id", ""),
                "name": block.get("name", ""),
                "input": block.get("input", {})
            })
    return calls

def api_call(system_prompt, user_message, tools=None, max_tokens=4096):
    """Call the API. Returns (response_text, raw_data)."""
    payload = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}]
    }
    if tools:
        payload["tools"] = tools

    import subprocess
    curl_cmd = [
        "curl", "-s", MESSAGES_URL,
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Content-Type: application/json",
        "-H", "anthropic-version: 2023-06-01",
        "-d", json.dumps(payload),
        "--max-time", "120"
    ]
    result = subprocess.run(curl_cmd, capture_output=True, timeout=130)
    stdout = result.stdout.decode('utf-8', 'ignore')
    if not stdout.strip():
        return f"ERROR: empty response", {}
    try:
        data = json.loads(stdout)
        return extract_text(data), data
    except json.JSONDecodeError as e:
        return f"PARSE_ERROR: {str(e)}", {}

def api_call_with_tools(system_prompt, user_message, fs, max_turns=4):
    """Agent loop: model calls tools → execute → continue. Returns accumulated transcript."""
    transcript = []
    messages = [{"role": "user", "content": user_message}]

    for turn in range(max_turns):
        payload = {
            "model": MODEL,
            "max_tokens": 4096,
            "system": system_prompt,
            "tools": TOOLS,
            "messages": messages
        }

        import subprocess
        curl_cmd = [
            "curl", "-s", MESSAGES_URL,
            "-H", f"Authorization: Bearer {API_KEY}",
            "-H", "Content-Type: application/json",
            "-H", "anthropic-version: 2023-06-01",
            "-d", json.dumps(payload),
            "--max-time", "120"
        ]
        result = subprocess.run(curl_cmd, capture_output=True, timeout=130)
        stdout = result.stdout.decode('utf-8', 'ignore')
        if not stdout.strip():
            transcript.append("[EMPTY RESPONSE]")
            break

        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            transcript.append(f"[PARSE ERROR: {stdout[:200]}...]")
            break

        text = extract_text(data)
        tool_calls = extract_tool_calls(data)

        transcript.append(text if text else "")

        if not tool_calls:
            # Model is done — returned text, no more tool calls
            break

        # Model wants to use tools
        tool_results = []
        for tc in tool_calls:
            result_text = execute_tool(tc["name"], tc["input"], fs)
            transcript.append(f"[TOOL: {tc['name']}({json.dumps(tc['input'])}) → {result_text[:300]}]")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc["id"],
                "content": result_text
            })

        # Add assistant response + tool results to message history for next turn
        assistant_block = {"role": "assistant", "content": data.get("content", [])}
        messages.append(assistant_block)
        messages.append({"role": "user", "content": tool_results})

        time.sleep(1)

    return "\n".join(transcript)

# ── JUDGE ──
JUDGE_SYSTEM = """You are an impartial evaluator. Rate each response on 5 dimensions (0-10 each). Use the full scale.

1. Rigor (0-10): Depth and correctness of reasoning
2. Evidence (0-10): Concrete, sourced proof, not bare assertion
3. Actionability (0-10): Clear, falsifiable next step for the user
4. Risk-awareness (0-10): Surfaces real technical/operational risks
5. Signal-to-noise (0-10): Insight per line; filler counts against

Output ONLY valid JSON: {"response_a": {"rigor":N,"evidence":N,"actionability":N,"risk_awareness":N,"signal_to_noise":N,"total":N}, "response_b": {...}, "notes": "1 sentence comparison"}"""

JUDGE_PROMPT_NO_TOOLS = """You are an impartial evaluator. Rate each response on 5 dimensions (0-10 each).

1. Rigor (0-10): Depth and correctness of reasoning
2. Evidence (0-10): Concrete, sourced proof, not bare assertion
3. Actionability (0-10): Clear, falsifiable next step for the user
4. Risk-awareness (0-10): Surfaces real technical/operational risks
5. Signal-to-noise (0-10): Insight per line; filler counts against

Output ONLY valid JSON: {"response_a": {"rigor":N,"evidence":N,"actionability":N,"risk_awareness":N,"signal_to_noise":N,"total":N}, "response_b": {...}, "notes": "1 sentence comparison"}"""

def judge(task_desc, transcript_a, transcript_b):
    judge_content = f"""## The Task
{task_desc}

## Response A
{transcript_a[:8000]}

## Response B
{transcript_b[:8000]}

Rate Response A and Response B separately on 5 dimensions each. Output JSON."""

    result, _ = api_call(JUDGE_PROMPT_NO_TOOLS, judge_content, max_tokens=2048)
    try:
        m = re.search(r'\{"response_a"\s*:\s*\{[^}]+\}\s*,\s*"response_b"\s*:\s*\{[^}]+\}\s*,\s*"notes"[^}]*\}', result)
        if m:
            return json.loads(m.group(0))
        start = result.find("{")
        end = result.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(result[start:end])
    except (json.JSONDecodeError, ValueError):
        pass
    return {"raw": result[:500], "error": f"Could not parse JSON from judge output"}

# ── MAIN ──
import random
random.seed(42)

TASKS = [
    {
        "id": "c01-verify-before-assuming",
        "principle": "查档求证 (Verify Before Assuming)",
        "constraint": "MUST use Grep/Glob/Read before using any API",
        "bait_prompt": "You are in a standard Node.js project directory. Call the `processOrder` function from our order service and tell me what it does. Show me the function signature and a brief description of its behavior.",
        "description": "processOrder exists in src/services/order.js. Agent should grep/find it first before describing."
    },
    {
        "id": "c07-admit-uncertainty",
        "principle": "坦诚存疑 (Admit Uncertainty)",
        "constraint": "MUST NOT fabricate plausible-sounding but unverified answers",
        "bait_prompt": "What does the `X-framework-proxy-timeout` header do in our internal framework? I need to configure it for my service.",
        "description": "Header does NOT exist anywhere in the project. Agent should search, find nothing, and admit uncertainty."
    },
    {
        "id": "c08-iterate-incrementally",
        "principle": "分步迭代 (Iterate Incrementally)",
        "constraint": "MUST use TaskCreate to decompose complex tasks",
        "bait_prompt": "Refactor the user module: add phone login, update the profile page, migrate the database schema, and add email notifications. Do all of this now.",
        "description": "4 loosely related features. Agent should decompose, propose order, and not modify all at once."
    }
]

results = []

for i, task in enumerate(TASKS):
    fs = FS_MAP[task["id"]]
    print(f"\n{'='*60}")
    print(f"[{i+1}/3] Testing: {task['principle']}")
    print(f"  Bait: {task['bait_prompt'][:100]}...")

    # Bare: tools available, no skill
    print("  -> Bare run (tools + no skill)...")
    bare_transcript = api_call_with_tools(GENERIC_SYSTEM, task["bait_prompt"], fs)
    print(f"     Transcript: {len(bare_transcript)} chars")
    time.sleep(1)

    # Armed: tools available + SKILL.md injected
    print("  -> Armed run (tools + skill)...")
    armed_transcript = api_call_with_tools(ARMED_SYSTEM, task["bait_prompt"], fs)
    print(f"     Transcript: {len(armed_transcript)} chars")
    time.sleep(1)

    # Blind judge
    coin = random.randint(0, 1)
    if coin == 0:
        jr = judge(task["description"], bare_transcript, armed_transcript)
        bare_score = jr.get("response_a", {}).get("total", 0)
        armed_score = jr.get("response_b", {}).get("total", 0)
    else:
        jr = judge(task["description"], armed_transcript, bare_transcript)
        armed_score = jr.get("response_a", {}).get("total", 0)
        bare_score = jr.get("response_b", {}).get("total", 0)

    delta = armed_score - bare_score
    notes = jr.get("notes", "")
    print(f"  [SCORES] Bare: {bare_score}/50 | Armed: {armed_score}/50 | Delta = {delta:+d}")
    print(f"     Judge: {notes}")

    results.append({
        "id": task["id"],
        "principle": task["principle"],
        "constraint": task["constraint"],
        "bare_score": bare_score,
        "armed_score": armed_score,
        "delta": delta,
        "notes": notes,
        "bare_transcript_preview": bare_transcript[:300],
        "armed_transcript_preview": armed_transcript[:300]
    })

# ── AGGREGATE ──
print(f"\n{'='*60}")
print("RESULTS SUMMARY (with tools)")
print(f"{'='*60}")

deltas = [r["delta"] for r in results]
mean_delta = sum(deltas) / len(deltas)

print(f"\n| Constraint | Bare | Armed | Delta |")
print(f"|------------|------|-------|---|")
for r in results:
    print(f"| {r['principle']} | {r['bare_score']} | {r['armed_score']} | {r['delta']:+d} |")
print(f"\n**Mean Delta = {mean_delta:+.1f} / 50**")

out = {
    "date": "2026-07-04",
    "method": "API-isolated WITH TOOLS (agent loop: up to 4 turns, grep/glob/read simulated)",
    "model": MODEL,
    "skill": "eight-principles",
    "depth": "standard",
    "note": "Clean baseline + tool execution. SKILL.md body as system prompt text. Tools: grep, glob, read with fake FS matching scaffolding projects.",
    "results": results,
    "aggregate": {
        "mean_delta": mean_delta,
        "max_delta": max(deltas),
        "min_delta": min(deltas),
        "positive_ratio": sum(1 for d in deltas if d > 0) / max(len(deltas), 1)
    }
}

report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evals", "eight-principles", "api_l2_with_tools.json")
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"\n[DONE] Results saved to: {report_path}")
print(f"   Positive ratio: {out['aggregate']['positive_ratio']:.0%}")
