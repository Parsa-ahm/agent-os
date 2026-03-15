# Ecosystem: Complementary Tools

agent-os is intentionally minimal — it's a workflow and a set of conventions, not a platform.
These tools either extend what agent-os does or take it further in specific directions.

---

## Tools worth knowing

### Continue.dev
**What:** Open-source IDE extension (VS Code + JetBrains) that connects any LLM directly to your editor — Claude, GPT-4, or a local Ollama model.
**Why it matters for agent-os:** Its `config.json` model routing is the closest existing implementation to agent-os's task routing. Defines model providers by role: chat, autocomplete, embeddings.
**How to use with agent-os:** Install Continue.dev, point its `autocomplete` model at your local Ollama model and its `chat` model at Claude. Your brain files can be added as `@file` context providers.
**URL:** https://github.com/continuedev/continue

### Aider
**What:** CLI AI pair programmer that works directly with your git repo. Supports multiple backends including local Ollama. "Architect + editor" split mode — one model plans, a cheaper model applies.
**Why it matters for agent-os:** The architect/editor split maps directly to our Claude/local routing. Every change is a git commit — aligns with our conventional commits requirement.
**How to use with agent-os:** Use Aider's `--model` flag to route tasks. Point `--editor-model` at Ollama for application, keep `--architect-model` on Claude for planning.
**URL:** https://github.com/paul-gauthier/aider

### Mem0
**What:** Memory layer for AI agents. Write structured memories after each session, retrieve relevant ones in future sessions. Self-hosted option available.
**Why it matters for agent-os:** As your brain files grow, a queryable memory API becomes more useful than flat markdown files. Mem0 can back or extend the brain system.
**How to use with agent-os:** Optional upgrade path. Start with flat brain files (simpler). If you're running long-lived agents or the brain grows to 20+ files, add Mem0 as a retrieval layer.
**URL:** https://github.com/mem0ai/mem0

### OpenHands (formerly OpenDevin)
**What:** Autonomous agent with a sandboxed runtime — browser, terminal, file system. Full task execution, not just code generation.
**Why it matters for agent-os:** The `AgentHub` pattern (registering specialized sub-agents by task type) is a more formal version of our `agents/` directory. Useful reference for when you scale up.
**URL:** https://github.com/All-Hands-AI/OpenHands

### SWE-agent
**What:** Solves GitHub issues end-to-end. Built on an "Agent-Computer Interface" (ACI) — a constrained, structured command set between the LLM and the computer.
**Why it matters for agent-os:** The ACI concept reduces hallucination by giving agents structured operations instead of raw shell access. Direct inspiration for tool-use boundaries in routing.
**URL:** https://github.com/princeton-nlp/SWE-agent

### Devon (open-source Devin)
**What:** Terminal UI agent with persistent session state and human-in-the-loop checkpoints.
**Why it matters for agent-os:** The "interrupt and resume" model is exactly what our dual-review gate does manually. Worth studying if you want to automate the gate flow.
**URL:** https://github.com/entropy-research/devon

### MetaGPT
**What:** Assigns LLM agents to software roles (PM, architect, engineer, QA). They communicate via structured documents.
**Why it matters for agent-os:** Formalizes the multi-agent review pattern. Our dual-review gate is a lightweight version of this — MetaGPT is where you go when you need a full pipeline.
**URL:** https://github.com/geekan/MetaGPT

### Letta (formerly MemGPT)
**What:** Tiered memory system for LLMs — hot (in-context), warm (vector store), cold (archival). Agent self-manages what stays in context.
**Why it matters for agent-os:** The memory paging model is a more sophisticated version of the brain file system. Good reference for when context management becomes the bottleneck.
**URL:** https://github.com/letta-ai/letta

---

## How to add a tool to your environment

When you find a tool you want to integrate:

1. Add it to `brain/decisions.md` as an ADR — what it does, why you chose it, trade-offs
2. Update `agents/local-router.md` if it changes your routing table
3. Update `brain/active-projects.md` if it becomes part of your infrastructure
4. Rebuild your Ollama model if the tool changes how you work

This keeps all three AI models informed about your environment changes.

---

## What agent-os deliberately doesn't do

- **No GUI** — the brain is markdown, the rules are markdown, the scripts are bash. Simple tools last.
- **No cloud dependency** — everything works offline if you have Ollama running
- **No lock-in** — switching from Claude to another frontier model means editing a few config files
- **No automation of the dual-review gate** — the human-in-the-loop on critical decisions is intentional, not a limitation to automate away
