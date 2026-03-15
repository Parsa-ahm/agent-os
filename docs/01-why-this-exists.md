# Why This Exists

## The problem

Most developers using AI assistants run into the same failure modes:

1. **Token waste** — asking a frontier model to fix a CSS class or update an env variable
2. **No shared context** — Claude doesn't know what Cursor knows. Your local model knows nothing. Every session starts cold.
3. **No rules** — AI assistants default to verbose, hedging, overly-cautious responses. You spend half the conversation steering them back on track.
4. **Single point of review** — one AI reviewing its own output catches far fewer problems than two independent models with different training.
5. **Things fall through the cracks** — the more complex the system, the more often a small miss in step 2 causes an hour of debugging in step 8.

## What agent-os does

agent-os is not a framework or a library. It's an environment — a set of files, conventions, and workflows that make three AI systems work as a coherent team:

- **Claude Code** — architecture, planning, complex bugs, security review
- **Cursor/Codex** — in-editor coding, completions, quick refactors
- **Ollama (local)** — CSS, config, env edits, boilerplate, offline work

They share:
- A **brain** (context files every AI reads)
- **Behavior rules** (direct, concise, no fluff — same personality across all models)
- **Task routing** (explicit rules for what goes where)
- A **dual-review gate** (critical decisions pass through two models before you touch code)

## Who this is for

- Solo developers or small teams shipping fast
- Anyone who has ever been burned by an AI that confidently wrote broken architecture
- Anyone paying $20-$200/month in AI tokens and wondering if half of it is waste

## What you get

After setup (~15 minutes):
- A consistent AI team that reads from the same context
- No more "let me explain my whole stack again"
- Routing that saves 40-60% of token spend on routine tasks
- Critical decisions reviewed by two models + you before a line of code is written
- Rules that make all three AIs direct, fast, and non-hedging

## What this is NOT

- A coding assistant by itself
- A replacement for thinking
- An autonomous agent that runs without you

You're still the architect. This just makes your AI tools stop contradicting each other and start working as a team.
