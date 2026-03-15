# Local Agent (Agentic Ollama)

Instead of chatting with your local model, you give it a task and it executes — reading files, writing changes, running commands, and reporting back when done.

No back-and-forth. No copy-pasting. It just does the thing.

---

## What it is

`scripts/local-agent.py` is a ReAct-style agent loop built on Ollama's tool-calling API.
The model gets a task and a set of tools. It reasons through what to do, calls tools, reads results, and continues until the task is complete.

**Tools available:**
| Tool | What it does |
|------|-------------|
| `read_file` | Read any file in the working directory |
| `write_file` | Create or overwrite a file |
| `list_dir` | List files and folders |
| `search_files` | Find files by glob pattern |
| `run_bash` | Run a shell command (requires confirmation for non-read-only) |

**Safety:**
- All file paths are constrained to the working directory — no access outside it
- `run_bash` asks for your confirmation before any command that modifies system state
- Destructive operations (delete, reset) are blocked — the agent explains why instead

---

## Setup

```bash
# Install the requests library (one-time)
pip install requests
# or if using uv:
uv add requests

# Make sure Ollama is running and your model is built
ollama list  # should show your model

# Run a task
python scripts/local-agent.py "fix the spacing in src/styles/card.css"
```

---

## Usage

```bash
# Basic usage
python scripts/local-agent.py "add missing semicolons to src/lib/utils.ts"

# With a specific model
python scripts/local-agent.py --model qwen2.5-coder:7b "rename Button to PrimaryButton in src/"

# Set model via env var (put in your shell profile)
export LOCAL_AGENT_MODEL=my-coder
python scripts/local-agent.py "add .env.example with all vars from the existing .env"

# Point at a different Ollama instance
python scripts/local-agent.py --url http://192.168.1.5:11434 "update the README"
```

---

## What it's good for (the routing table)

These are the tasks where the local agent beats typing: cheap, mechanical, well-scoped.

| Task | Example command |
|------|----------------|
| CSS / styling fixes | `"fix indentation in all .css files in src/styles/"` |
| .env / config edits | `"add REDIS_URL=redis://localhost:6379 to .env.example"` |
| Renaming | `"rename all occurrences of UserCard to MemberCard in src/"` |
| Boilerplate generation | `"create a README.md for the /src/features/auth/ folder"` |
| Import cleanup | `"remove unused imports from src/lib/utils.ts"` |
| Comment generation | `"add JSDoc comments to all exported functions in src/lib/"` |
| File creation | `"create a .gitkeep in every empty directory under src/"` |
| Format fixes | `"ensure all JSON files in config/ are properly formatted"` |

**Don't use it for:**
- Architecture decisions
- Bug investigation requiring reasoning
- Anything touching auth, payments, or user data
- Tasks where you're not sure what the right answer is

If you're unsure — use Claude.

---

## How it works (the loop)

```
You give a task
       │
       ▼
System prompt + task → Ollama
       │
       ▼
Model decides: what tool to call?
       │
       ├── read_file → reads the file → result back to model
       ├── list_dir  → sees the structure → continues reasoning
       ├── write_file → makes the change
       └── run_bash  → executes (with confirmation if needed)
       │
       ▼
Model checks: is the task done?
  YES → prints summary, stops
  NO  → calls next tool
       │
       ▼
Hard stop at 20 steps (configurable via MAX_STEPS in the script)
```

The model is in a loop until it decides the task is complete or hits the step limit.
You see each tool call in real time as it happens.

---

## Output example

```
🤖 agent-os local agent
   model: my-coder
   task:  add .env.example from .env
   dir:   /home/user/my-project

────────────────────────────────────────────────────
  → list_dir(path='.')
  → read_file(path='.env')
  → write_file(path='.env.example', content=<312 chars>)

✅ Done

Created .env.example with 8 variables from .env.
Replaced all values with placeholder strings (DATABASE_URL=your_database_url, etc.).
Your actual .env is unchanged.
```

---

## Extending the agent

To add a new tool:

1. Write the Python function:
```python
def my_tool(arg1: str, arg2: str = "default") -> str:
    # do something
    return "result as string"
```

2. Add it to `TOOL_DEFS` (OpenAI function calling format)

3. Add it to `TOOL_FN_MAP`:
```python
TOOL_FN_MAP = {
    ...
    "my_tool": lambda a: my_tool(**a),
}
```

That's it. The model will use it automatically when relevant.

---

## Configuration

| Setting | Default | Override |
|---------|---------|---------|
| Model | `my-coder` | `--model` flag or `LOCAL_AGENT_MODEL` env var |
| Ollama URL | `http://localhost:11434` | `--url` flag or `OLLAMA_URL` env var |
| Max steps | 20 | Edit `MAX_STEPS` in script |
| Work dir | Current directory | `cd` before running |

---

## Model requirements

Tool calling requires a model that supports it. Confirmed working:
- `qwen2.5-coder:7b` ✅ (recommended)
- `qwen2.5-coder:14b` ✅
- `mistral:7b` ⚠️ (limited tool support, may not follow format)
- `llama3.1` ✅

If your model doesn't support tool calling, Ollama will return an empty tool_calls list
and the agent will print the model's text response instead of executing anything.
Upgrade to qwen2.5-coder if this happens.

---

## Going further

For more powerful local agentic workflows, see `docs/08-ecosystem.md`:
- **Goose** (Block) — full local agent runtime with browser, shell, and plugin system
- **Aider** — architect/editor split with git-native diffs, supports Ollama backends
- **Continue.dev** — in-editor agent with slash commands that execute tasks
