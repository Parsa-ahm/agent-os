# Architecture

## The three-model setup

```
┌─────────────────────────────────────────────────────────────┐
│                         YOU                                  │
│              (final decision on everything)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌─────────────┐ ┌──────────┐ ┌──────────────┐
   │ Claude Code │ │  Cursor  │ │    Ollama    │
   │             │ │  Codex   │ │ (local model)│
   │ Planning    │ │          │ │              │
   │ Architecture│ │ In-editor│ │ CSS / config │
   │ Complex bugs│ │ completions│ │ Env edits   │
   │ Security    │ │ Refactors│ │ Boilerplate  │
   │ Dual-review │ │          │ │ Offline work │
   └─────────────┘ └──────────┘ └──────────────┘
          │
          └──── All three read from ──── brain/
```

## Shared brain

All three models are given the same context files:

| File | Contents |
|------|----------|
| `brain/about-you.md` | Who you are, your stack, your goals |
| `brain/active-projects.md` | What's being built right now |
| `brain/coding-standards.md` | Hard rules: never do X, always do Y |
| `brain/decisions.md` | Why things are the way they are |
| `brain/ai-behavior.md` | How every AI in this environment must behave |

Claude reads these via `CLAUDE.md`.
Cursor reads these via `.cursorrules` or the cursor/rules.md file.
Ollama reads these via the system prompt in the Modelfile.

## Directory map

```
agent-os/
├── README.md                 ← start here
├── CLAUDE.md                 ← Claude Code entry point
├── .gitignore
│
├── brain/                    ← shared AI context (fill these in)
│   ├── about-you.md
│   ├── active-projects.md
│   ├── coding-standards.md
│   ├── decisions.md
│   └── ai-behavior.md
│
├── .claude/                  ← Claude Code config
│   ├── settings.json         ← ECC plugin enabled
│   └── rules/
│       ├── common/           ← universal rules (9 files)
│       ├── typescript/       ← TS-specific rules
│       └── python/           ← Python-specific rules
│
├── cursor/
│   └── rules.md              ← paste into .cursorrules in your project
│
├── ollama/
│   ├── Modelfile.template    ← copy, fill in, build your local model
│   └── README.md
│
├── agents/                   ← sub-agent behavior definitions
│   ├── planner.md
│   ├── code-reviewer.md
│   ├── security-reviewer.md
│   └── local-router.md       ← routing table (what goes where)
│
├── scripts/
│   ├── setup.sh              ← first-time setup
│   ├── create-model.sh       ← build Ollama model
│   └── verify.sh             ← check everything is working
│
└── docs/
    ├── 01-why-this-exists.md
    ├── 02-architecture.md        ← this file
    ├── 03-dual-review-gate.md
    ├── 04-task-routing.md
    ├── 05-brain-system.md
    ├── 06-behavior-rules.md
    ├── 07-customization.md
    └── 08-ecosystem.md           ← complementary tools
```
