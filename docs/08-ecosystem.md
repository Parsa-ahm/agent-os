# Ecosystem: Complementary Tools

agent-os is intentionally minimal — a workflow and a set of conventions, not a platform.
These tools either extend what agent-os does or took the same problems in different directions.
Worth knowing before you build something that already exists.

---

## Category 1: IDE & Editor Integration

### Continue.dev
**What:** Open-source IDE extension (VS Code + JetBrains) connecting any LLM to your editor — Claude, GPT-4, local Ollama. Context-aware chat, autocomplete, slash commands.
**Key pattern:** `config.json` model routing — define multiple providers by role (chat, autocomplete, embeddings). Closest existing implementation to agent-os task routing. Also its `@file`, `@repo`, `@docs` context providers.
**How to use with agent-os:** Install Continue.dev, point `autocomplete` at your Ollama model, `chat` at Claude. Add brain files as `@file` context providers.
**URL:** https://github.com/continuedev/continue

### Cline (formerly Claude Dev)
**What:** VS Code extension giving Claude autonomous file editing, terminal access, and browser control inside the editor. Per-project `.clinerules` files, tool approval flows.
**Key pattern:** `.clinerules` is identical in intent to `CLAUDE.md` — project-level AI instructions. Also the "auto-approve vs ask every time" tool permission model.
**How to use with agent-os:** agent-os ships a `.clinerules` file. If you use Cline, copy it to your project root.
**URL:** https://github.com/cline/cline

### Aider
**What:** CLI AI pair programmer working directly with your git repo. Sends diffs, not whole files. Supports multiple backends including local Ollama.
**Key pattern:** Architect/editor split mode — one model plans the change, a cheaper model applies it. Every change is a git commit.
**How to use with agent-os:** `--architect-model claude` + `--editor-model ollama/my-coder` maps directly to our routing table.
**URL:** https://github.com/paul-gauthier/aider

---

## Category 2: Local Agent Runtimes

### Goose (by Block/Square)
**What:** Local AI developer agent. Runs on your machine, uses local or remote models, plugin system for tools (shell, browser, code editor), session memory.
**Key pattern:** "Toolkit" plugin system — each toolkit is a set of tools per-session. Clean separation between agent runtime and capabilities.
**How to use with agent-os:** Goose + your Ollama model is a strong local agent lane. Add it to the routing table for offline autonomous tasks.
**URL:** https://github.com/block/goose

### Fabric (by Daniel Miessler)
**What:** Library of reusable AI "patterns" (prompt templates) pipeable in the shell. Each pattern is a markdown file. `cat file.md | fabric --pattern extract_wisdom`.
**Key pattern:** Unix-pipe model for AI — single-purpose prompt files composed at the shell level. Your `agents/` directory is the same idea; Fabric makes it shell-native.
**How to use with agent-os:** Your agent definitions in `agents/` are compatible with the Fabric pattern format. Fabric gives them a shell runtime.
**URL:** https://github.com/danielmiessler/fabric

---

## Category 3: Autonomous Task Execution

### OpenHands (formerly OpenDevin)
**What:** Autonomous agent in a sandboxed Docker environment — browser, terminal, file system. Full task execution, not just generation.
**Key pattern:** `AgentHub` — registered specialized sub-agents by task type. The sandbox/runtime abstraction that keeps agent actions isolated from the host.
**URL:** https://github.com/All-Hands-AI/OpenHands

### SWE-agent (Princeton NLP)
**What:** Solves GitHub issues end-to-end — clones repo, edits code, runs tests, opens PR. Built on an "Agent-Computer Interface" (ACI).
**Key pattern:** ACI — constrained, structured command set between the LLM and the computer. Instead of raw bash, the agent gets `open`, `search_file`, `edit`. Reduces hallucination significantly.
**URL:** https://github.com/princeton-nlp/SWE-agent

### Devon (open-source)
**What:** Terminal UI agent with persistent session state and human-in-the-loop checkpoints.
**Key pattern:** "Interrupt and resume" — agent pauses at decision points, human redirects, then continues. This is our dual-review gate done automatically.
**URL:** https://github.com/entropy-research/devon

### Sweep AI
**What:** GitHub bot that opens PRs from issues automatically. Plan-then-execute loop with self-review.
**Key pattern:** RAG over codebase — vector-indexed repository for retrieval-augmented code generation. Useful reference for when your shared brain context needs search, not just reading.
**URL:** https://github.com/sweepai/sweep

---

## Category 4: Multi-Agent Review & Orchestration

### MetaGPT
**What:** LLM agents assigned to software roles (PM, architect, engineer, QA). Output passes through staged review gates.
**Key pattern:** Role-based "standardized operating procedures" — agents follow defined workflows per role. Formalizes what our planner/code-reviewer/security-reviewer agents do manually.
**URL:** https://github.com/geekan/MetaGPT

### AutoGen (Microsoft)
**What:** Multi-agent conversation framework. Agents can be LLMs, tools, or humans. `GroupChat` + `GroupChatManager` routes messages to the right specialist.
**Key pattern:** "Human proxy" agent — a human steps in at any point in an automated conversation. Maps directly to the user-approval step in the dual-review gate.
**URL:** https://github.com/microsoft/autogen

### CrewAI
**What:** Opinionated framework for agent crews with roles, goals, and backstories. Task → Agent assignment with explicit context passing between steps.
**Key pattern:** The task-context passing model — output of one agent becomes context for the next. Clean formalism for: write → review → security-check → commit.
**URL:** https://github.com/crewAIInc/crewAI

### LangGraph
**What:** Graph-based agent orchestration. Agents are nodes, edges are conditional routing rules. Supports cycles (retry loops), parallel branches, persistent state.
**Key pattern:** State graph for agent handoffs — the cleanest existing formalism for task routing. State is a typed object passed through the graph. Direct architectural reference for a future programmatic routing layer.
**URL:** https://github.com/langchain-ai/langgraph

---

## Category 5: Context & Memory

### Mem0
**What:** Memory layer API for AI apps. Structured memory CRUD (add, search, update, delete). Automatic memory extraction — the model decides what to save. Self-hosted option.
**How to use with agent-os:** Optional upgrade path. Start with flat brain files. When the brain grows beyond ~20 files or you run long-lived agents, add Mem0 as a retrieval layer.
**URL:** https://github.com/mem0ai/mem0

### Letta (formerly MemGPT)
**What:** Tiered memory system — hot (in-context), warm (vector store), cold (archival). Agent self-manages what stays in context.
**Key pattern:** Memory paging abstraction. Maps to: active session = hot, `brain/` files = warm, full vault = cold. Reference this model when your context starts overflowing.
**URL:** https://github.com/letta-ai/letta

---

## Key architectural lessons from the ecosystem

These are the recurring patterns that show up across most of the tools above.
Worth knowing when extending agent-os:

**1. Single source of truth for rules**
Continue.dev, Cline, Cursor, and Claude Code all have separate rule files (`.continuerules`, `.clinerules`, `.cursorrules`, `CLAUDE.md`). Right now you maintain them separately. The next evolution is generating all of them from one canonical source.

**2. Model routing should be declarative**
Aider's architect/editor split and Continue.dev's role-based config both point to the same pattern: define `planning → Claude`, `code application → local`, `review → second model` as config, not convention. This is the next step beyond the routing table in `agents/local-router.md`.

**3. Constrained tool interfaces beat raw shell access**
SWE-agent's ACI pattern — giving agents structured commands instead of raw bash — reduces hallucination and makes agent actions auditable. Relevant when you add any automation to the routing layer.

**4. Tiered context (hot/warm/cold)**
Letta's memory model: active session context is hot (in-window), `brain/` files are warm (read on session start), full vault is cold (searched on demand). Agent-os's brain system is already the warm tier. The cold tier becomes relevant when the vault grows.

**5. Human-in-the-loop is a feature, not a limitation**
Devon, AutoGen, and others all have explicit human checkpoint patterns. The dual-review gate's user approval step is the right call — tools that remove it for "convenience" accumulate more production incidents.

---

## How to add a tool to your environment

1. Add it to `brain/decisions.md` as an ADR — what it does, why you chose it, trade-offs
2. Update `agents/local-router.md` if it changes your routing table
3. Update `brain/active-projects.md` if it becomes infrastructure
4. Rebuild your Ollama model if your workflow changes significantly
