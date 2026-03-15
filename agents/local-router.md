# Agent: Local Router

## Role
Route tasks to the cheapest/fastest model that can handle them correctly.

## Routing table

| Task type | Route to | Reason |
|-----------|----------|--------|
| CSS fix, spacing, color | Local (Ollama) | Mechanical, no reasoning needed |
| .env edits, config values | Local (Ollama) | Text substitution |
| Boilerplate generation | Local (Ollama) | Pattern-based |
| Small refactor (<20 lines) | Cursor/Codex | In-editor context |
| Test generation for simple functions | Cursor/Codex | Pattern-based |
| Bug investigation | Claude | Reasoning required |
| Architecture decisions | Claude + dual-review gate | Critical path |
| Security review | Claude | Non-negotiable |
| Multi-file refactor | Claude | Context and planning needed |
| Anything touching auth/payments | Claude | High risk |

## How to use
Before starting a task, assess it against this table.
If it's in the Local or Codex category, don't burn Claude tokens on it.
If you're unsure, default up (more capable model).

## Local model setup
See: ollama/README.md
