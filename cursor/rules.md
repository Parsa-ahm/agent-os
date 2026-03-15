# Cursor Rules for agent-os

Copy this content into `.cursorrules` at the root of any project using agent-os.
Or set it as a global Cursor rule in Settings → Rules for AI.

---

```
Read and follow: brain/about-you.md, brain/active-projects.md,
brain/coding-standards.md, brain/ai-behavior.md, brain/decisions.md

## Communication rules
- Direct and concise. No preamble, no softening, no filler.
- If something is wrong or a bad idea, say so immediately and plainly.
- No "great question!", no "certainly!", no "I see what you're going for..."
- When asking for confirmation: explain what the action does and why. Not just the command.

## Code rules (from brain/coding-standards.md)
- TypeScript strict mode
- pnpm (Node), uv (Python)
- zod or pydantic for all external data validation
- Conventional commits: feat: fix: chore: docs: refactor: test:
- Explicit error handling — no silent failures
- .env for all secrets, .env.example committed
- No hardcoded secrets or tokens
- No console.log in production code

## Scope
- Do not refactor code you weren't asked to touch
- Do not add features beyond what was requested
- Flag potential issues — don't silently fix them

## Critical paths
Architecture decisions, security design, data models, API contracts, and auth flows
require dual-review (Claude + Codex + human) before implementation.
Do not implement these without surfacing them for review first.
See: docs/03-dual-review-gate.md
```
