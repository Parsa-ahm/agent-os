# agent-os

A unified AI development environment that makes Claude Code, Cursor/Codex, and a local Ollama model work as a coherent team — sharing context, following the same rules, and routing tasks to the right model.

> **Not a framework. Not a library. A set of files and conventions that transform three separate AI tools into one coordinated system.**

---

## The problem this solves

| Symptom | Root cause |
|---------|-----------|
| Re-explaining your stack every session | No shared context between AI tools |
| AI gives verbose, hedging responses | No behavior rules — default mode is chatbot mode |
| Paying Claude rates for a CSS fix | No task routing — everything goes to the most expensive model |
| AI suggests something you already ruled out | No decision log |
| Architecture bug found after 2 days of coding | Single model reviewed a critical design |

agent-os fixes all five.

---

## What you get

```
┌──────────────────────────────────────────────────────┐
│                       YOU                             │
└────────────────────┬─────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
 ┌────────────┐ ┌──────────┐ ┌──────────────┐
 │ Claude Code│ │  Cursor  │ │    Ollama    │
 │            │ │  Codex   │ │ local model  │
 │ Planning   │ │          │ │              │
 │ Architecture│ │ In-editor│ │ CSS / config │
 │ Complex bugs│ │ completions│ │ Env edits   │
 │ Security   │ │ Refactors│ │ Boilerplate  │
 └────────────┘ └──────────┘ └──────────────┘
        │              │            │
        └──────────────┴────────────┘
                       │
              reads from brain/
     (same context, same rules, same personality)
```

**Three models. One shared brain. One set of rules. Explicit routing.**

---

## Quick start

```bash
# Clone
git clone https://github.com/your-handle/agent-os
cd agent-os

# Run setup (checks dependencies, guides next steps)
bash scripts/setup.sh

# Fill in your context
# Edit brain/about-you.md — who you are, your stack
# Edit brain/active-projects.md — what you're building

# Build your local model
cp ollama/Modelfile.template ollama/Modelfile
# Fill in your details in ollama/Modelfile
bash scripts/create-model.sh my-coder

# Verify everything is in place
bash scripts/verify.sh
```

Setup takes about 15 minutes. Most of it is filling in your brain files.

---

## How it works

### Shared brain

The `brain/` directory is plain markdown files every AI reads:

| File | What to put in it |
|------|-------------------|
| `about-you.md` | Your role, stack, tools, preferences |
| `active-projects.md` | What you're building right now |
| `coding-standards.md` | Hard rules: always/never lists |
| `decisions.md` | Why things are the way they are (ADRs) |
| `ai-behavior.md` | How every AI in this env must behave |

Claude reads via `CLAUDE.md`. Cursor reads via `.cursorrules`. Ollama has it in its system prompt.
One update, all three models know.

### Behavior rules

All three models follow the same communication rules from `brain/ai-behavior.md`:
- Direct and concise — no filler, no hedging
- Say something is wrong immediately, plainly
- Explain what and why when asking for confirmation — not just "run this?"
- No unsolicited refactors or scope creep

### Task routing

Not every task needs a frontier model. The routing table in `agents/local-router.md`:

| Task | Model | Saves |
|------|-------|-------|
| CSS fix, config edit, .env | Local (Ollama) | ~$0.002/task |
| In-editor refactor, completions | Cursor/Codex | Cheaper than Claude |
| Architecture, complex bugs | Claude | Worth it |
| Security review | Claude | Non-negotiable |

Typical result: 60-70% of routine tasks stay local or in Cursor. Claude is reserved for work that actually needs it.

### Dual-review gate

Critical decisions — architecture, security, data models, auth flows — pass through two models before implementation:

1. Claude drafts the design
2. Codex reviews independently
3. Claude reconciles both reviews
4. You approve

Neither model's blind spots are the other's. Two independent reviews before a line of code is written.
Full details: `docs/03-dual-review-gate.md`

---

## Documentation

The `docs/` directory is written to be read end-to-end. Start at `01`, each one builds on the last.

| Doc | What it covers |
|-----|----------------|
| [01-why-this-exists.md](docs/01-why-this-exists.md) | The problems and why this approach solves them |
| [02-architecture.md](docs/02-architecture.md) | How the three models connect, full directory map |
| [03-dual-review-gate.md](docs/03-dual-review-gate.md) | The two-model review workflow for critical decisions |
| [04-task-routing.md](docs/04-task-routing.md) | What goes where and why, token cost analysis |
| [05-brain-system.md](docs/05-brain-system.md) | The shared context files, what to put in them |
| [06-behavior-rules.md](docs/06-behavior-rules.md) | The communication rules and how to apply them |
| [07-customization.md](docs/07-customization.md) | Making it yours — what to change, what to leave |
| [08-ecosystem.md](docs/08-ecosystem.md) | Complementary tools worth knowing |

---

## Requirements

- [Claude Code](https://claude.ai/download) (Claude subscription)
- [Cursor](https://cursor.sh) or VS Code with an AI extension
- [Ollama](https://ollama.ai) + at least 8GB RAM
- git

Optional but recommended:
- [ECC (Everything Claude Code)](https://github.com/affaan-m/everything-claude-code) — extends Claude Code with skills, agents, and rules
- [Continue.dev](https://github.com/continuedev/continue) — multi-model IDE extension, complements Cursor

---

## Directory structure

```
agent-os/
├── README.md
├── CLAUDE.md                 ← Claude Code entry point
├── .gitignore
├── brain/                    ← fill these in first
├── .claude/rules/            ← Claude Code rule files
├── cursor/                   ← paste into .cursorrules
├── ollama/                   ← local model setup
├── agents/                   ← sub-agent definitions
├── scripts/                  ← setup, build, verify
└── docs/                     ← the full guide
```

---

## Contributing

Issues and PRs welcome. Particularly interested in:
- Rule files for additional languages (Go, Rust, Java)
- Additional agent definitions for common workflows
- Routing table improvements based on real usage
- Integration guides for specific tools

---

## License

MIT
