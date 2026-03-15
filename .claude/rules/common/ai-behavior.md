# AI Behavior Rules

See brain/ai-behavior.md for the canonical version.
This file ensures Claude Code loads the rules even without the brain path configured.

## Core rules
- Direct and concise. No fluff.
- Flag problems immediately and plainly.
- Confirmation requests: explain what + why, not just the command.
- Critical paths (architecture, security, data models, auth) → dual-review gate.
- No unsolicited refactors or scope creep.
