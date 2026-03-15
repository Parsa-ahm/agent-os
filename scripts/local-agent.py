#!/usr/bin/env python3
"""
agent-os local agent
Uses your Ollama model with tool calling to autonomously execute tasks.
The model reasons through steps and calls tools — you don't chat, it does.

Usage:
  python scripts/local-agent.py "fix the spacing in src/styles/card.css"
  python scripts/local-agent.py "add a .env.example with all the vars from .env"
  python scripts/local-agent.py --model my-coder "rename Button to PrimaryButton everywhere in src/"

Requirements:
  pip install requests  (or: uv add requests)
  Ollama running locally with a model that supports tool calling (qwen2.5-coder recommended)
"""

import sys
import os
import json
import subprocess
import argparse
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
OLLAMA_URL   = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("LOCAL_AGENT_MODEL", "my-coder")
MAX_STEPS    = 20       # hard stop to prevent infinite loops
WORK_DIR     = Path.cwd()

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip install requests  or  uv add requests")
    sys.exit(1)


# ── Tools ─────────────────────────────────────────────────────────────────────

def read_file(path: str) -> str:
    p = _safe_path(path)
    return p.read_text(encoding="utf-8")

def write_file(path: str, content: str) -> str:
    p = _safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"Written: {path}"

def list_dir(path: str = ".") -> str:
    p = _safe_path(path)
    entries = sorted(p.iterdir(), key=lambda e: (e.is_file(), e.name))
    lines = []
    for e in entries:
        prefix = "📁" if e.is_dir() else "📄"
        lines.append(f"{prefix} {e.name}")
    return "\n".join(lines) if lines else "(empty)"

def search_files(pattern: str, path: str = ".") -> str:
    p = _safe_path(path)
    matches = sorted(p.rglob(pattern))
    if not matches:
        return f"No files matching '{pattern}' in {path}"
    return "\n".join(str(m.relative_to(WORK_DIR)) for m in matches[:50])

def run_bash(command: str) -> str:
    """Runs a shell command. Requires user confirmation for non-read-only commands."""
    if not _is_safe_command(command):
        print(f"\n⚠️  The agent wants to run:\n  {command}")
        print("This modifies the system. Allow? [y/N] ", end="", flush=True)
        answer = input().strip().lower()
        if answer != "y":
            return "Command cancelled by user."
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True,
        cwd=WORK_DIR, timeout=30
    )
    out = result.stdout.strip()
    err = result.stderr.strip()
    if result.returncode != 0:
        return f"Exit {result.returncode}\nstdout: {out}\nstderr: {err}"
    return out or "(command completed, no output)"


# ── Tool definitions (OpenAI function calling format) ─────────────────────────

TOOL_DEFS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative file path"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or overwrite a file with given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path":    {"type": "string", "description": "Relative file path"},
                    "content": {"type": "string", "description": "Full file content"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files and folders in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative directory path", "default": "."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Find files matching a glob pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern e.g. '*.css', '**/*.ts'"},
                    "path":    {"type": "string", "description": "Root directory to search from", "default": "."}
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_bash",
            "description": "Run a shell command. For read-only commands only unless essential. User will be asked to confirm commands that modify files or system state.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to execute"}
                },
                "required": ["command"]
            }
        }
    }
]

TOOL_FN_MAP = {
    "read_file":    lambda a: read_file(**a),
    "write_file":   lambda a: write_file(**a),
    "list_dir":     lambda a: list_dir(**a),
    "search_files": lambda a: search_files(**a),
    "run_bash":     lambda a: run_bash(**a),
}


# ── Agent loop ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a local coding agent. You have tools to read files, write files, list directories, search, and run bash commands.

When given a task:
1. Explore the relevant files first to understand the current state.
2. Make the necessary changes using write_file.
3. Verify the result if possible.
4. When the task is complete, respond with a plain summary of what you did (no tool calls).

Rules:
- Work only within the current directory. Do not access paths outside it.
- Read before you write — understand before you change.
- Make targeted edits. Do not rewrite files wholesale unless the task requires it.
- If a task is ambiguous, do your best based on context. Don't ask clarifying questions.
- If a task requires destructive operations (delete, reset, drop), stop and explain why instead of proceeding.
- Be direct in your final summary. What changed, where, why. No fluff.
"""

def run_agent(task: str, model: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": task}
    ]

    print(f"\n🤖 agent-os local agent")
    print(f"   model: {model}")
    print(f"   task:  {task}")
    print(f"   dir:   {WORK_DIR}\n")
    print("─" * 60)

    for step in range(MAX_STEPS):
        response = _call_ollama(model, messages)

        if not response:
            print("✗ No response from Ollama. Is it running?")
            break

        msg = response.get("message", {})
        tool_calls = msg.get("tool_calls", [])

        if not tool_calls:
            # No more tool calls — agent is done
            content = msg.get("content", "").strip()
            print(f"\n✅ Done\n\n{content}")
            break

        # Execute tool calls
        messages.append({"role": "assistant", "content": msg.get("content", ""), "tool_calls": tool_calls})

        for tc in tool_calls:
            fn_name = tc["function"]["name"]
            raw_args = tc["function"].get("arguments", {})
            args = raw_args if isinstance(raw_args, dict) else json.loads(raw_args)

            print(f"  → {fn_name}({_fmt_args(args)})")

            if fn_name not in TOOL_FN_MAP:
                result = f"Unknown tool: {fn_name}"
            else:
                try:
                    result = TOOL_FN_MAP[fn_name](args)
                except PermissionError:
                    result = f"Permission denied: path outside working directory"
                except FileNotFoundError as e:
                    result = f"File not found: {e}"
                except Exception as e:
                    result = f"Error: {e}"

            # Trim long results so we don't blow the context window
            if len(result) > 4000:
                result = result[:4000] + f"\n... (truncated, {len(result)} chars total)"

            messages.append({
                "role": "tool",
                "content": result
            })
    else:
        print(f"\n⚠️  Reached max steps ({MAX_STEPS}). Stopping.")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _call_ollama(model: str, messages: list) -> dict:
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": model, "messages": messages, "tools": TOOL_DEFS, "stream": False},
            timeout=120
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to Ollama at {OLLAMA_URL}. Is it running?")
        return {}
    except requests.exceptions.HTTPError as e:
        print(f"✗ Ollama error: {e}")
        return {}

def _safe_path(path: str) -> Path:
    """Resolve path and ensure it stays within WORK_DIR."""
    p = (WORK_DIR / path).resolve()
    if not str(p).startswith(str(WORK_DIR)):
        raise PermissionError(f"Path '{path}' is outside working directory")
    return p

def _is_safe_command(cmd: str) -> bool:
    """Returns True for read-only commands that don't need confirmation."""
    safe_prefixes = ("cat ", "ls ", "find ", "grep ", "head ", "tail ",
                     "echo ", "pwd", "wc ", "file ", "stat ")
    return any(cmd.strip().startswith(p) for p in safe_prefixes)

def _fmt_args(args: dict) -> str:
    parts = []
    for k, v in args.items():
        v_str = repr(v) if isinstance(v, str) and len(v) < 60 else f"<{len(str(v))} chars>"
        parts.append(f"{k}={v_str}")
    return ", ".join(parts)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="agent-os local agent — give a task, Ollama does it"
    )
    parser.add_argument("task", nargs="+", help="Task to perform")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Ollama model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--url", default=OLLAMA_URL,
                        help=f"Ollama URL (default: {OLLAMA_URL})")
    args = parser.parse_args()

    OLLAMA_URL = args.url
    run_agent(" ".join(args.task), args.model)
