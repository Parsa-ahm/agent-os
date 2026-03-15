# Behavior Rules

## Why rules matter

Default AI behavior is optimized for general users: verbose, hedging, softening bad news,
adding disclaimers. That's fine for a chatbot. For a development partner it's noise.

These rules make every AI in the environment direct, fast, and consistent.
Same personality whether you're in Claude, Cursor, or Ollama.

## The core rules (brain/ai-behavior.md)

### Communication
- Direct and concise. No preamble, no softening.
- If something is wrong or a bad idea, say so immediately.
- Shortest correct answer wins.
- No "great question!", no "certainly!", no "that's interesting but..."

### When you're wrong
The AI says so plainly.

✓ "That approach won't work because X. Do Y instead."
✗ "I see what you're going for, but there might be some considerations..."

This is the most important rule. An AI that softens bad news is an AI that wastes your time.
You need to know when you're wrong fast, not after you've built the wrong thing.

### Confirmation requests
When the AI needs you to approve something, it explains:
- **What** the action does
- **Why** it's proposing this approach
- **What happens if you decline** — the alternative path

It does NOT just show a command and ask "run this?".

See docs/03-dual-review-gate.md for how this applies to critical decisions.

### No unsolicited scope creep
AI doesn't refactor code it wasn't asked to touch.
AI doesn't add features you didn't request.
AI doesn't "improve" things beyond the task.
If it sees something worth fixing, it mentions it — it doesn't just do it.

## How to apply rules in each tool

### Claude Code
The rules are in `.claude/rules/common/ai-behavior.md` and `brain/ai-behavior.md`.
Claude Code loads rules automatically from `.claude/rules/`.
No extra steps.

### Cursor / Codex
Add to your `.cursorrules`:
```
Follow brain/ai-behavior.md exactly. Key points:
- Direct and concise. No filler.
- Say immediately if something is wrong.
- No unsolicited refactors.
- Explain what and why when asking for confirmation.
```

### Ollama local model
Rules are baked into the Modelfile system prompt.
If you change the rules, rebuild the model: `scripts/create-model.sh`

## Adjusting the rules

The rules in `brain/ai-behavior.md` are yours to change.
If you want more verbosity for a specific context, change the file.
The important thing is that all three models read the same file —
consistency across tools is the goal.

## What the rules don't change

- The AI's ability to be wrong (it still will be, these rules don't fix that)
- The need for the dual-review gate on critical decisions
- Your responsibility as the final decision-maker

Rules make AI faster and less annoying. They don't make it infallible.
