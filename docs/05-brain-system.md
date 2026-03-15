# The Brain System

## What it is

The `brain/` directory is a set of plain markdown files that every AI in the environment reads.
It's the single source of truth for "who you are, what you're building, and how things work."

Without it:
- Every new conversation starts cold
- You repeat your stack to every model every session
- AI assistants make assumptions that contradict each other

With it:
- Every model starts with the same context
- No re-explaining your stack
- Decisions are documented so AI doesn't re-argue resolved trade-offs

## The files

### `brain/about-you.md`
Who you are. Your role, stack, tools, preferences.
This is what makes AI responses relevant to your specific situation instead of generic.

Fill this in first. It's the most important file.

### `brain/active-projects.md`
What you're building right now. Status, stack, repo, goal.
Keeps AI from suggesting approaches that conflict with your current direction.

Update this whenever you start or finish a project.

### `brain/coding-standards.md`
Hard rules. Always/never lists. These are non-negotiable instructions.
If it's here, AI should follow it without being asked.

### `brain/decisions.md`
Why things are the way they are. Architecture decision records (ADRs).

The most underused file. Every time you make a significant technical choice,
log it here with the reason and trade-offs. This prevents:
- AI re-suggesting something you already ruled out
- You forgetting why you made a decision 3 months ago
- New team members (human or AI) making conflicting decisions

Format:
```
## ADR-001: Title
Reason: why you chose this
Trade-off: what you gave up
```

### `brain/ai-behavior.md`
How every AI in this environment must behave. The communication rules.
Direct, concise, no hedging. How confirmation requests are phrased.
The dual-review gate requirement.

## How each tool reads it

**Claude Code:** Via `CLAUDE.md` at the project root, which lists the brain file paths.

**Cursor/Codex:** Add the brain files to your `.cursorrules`:
```
Read and internalize: brain/about-you.md, brain/active-projects.md,
brain/coding-standards.md, brain/ai-behavior.md
```
Or reference them in a Cursor rule. See `cursor/rules.md`.

**Ollama local model:** The brain content is pasted directly into the Modelfile system prompt.
This is a one-time operation — rebuild the model when the brain changes significantly.

## What NOT to put in the brain

- Temporary task state (use a todo list or session notes)
- Code snippets (link to the file instead)
- Debugging notes (those belong in commit messages)
- Secrets (never)

## Keeping it current

The brain only helps if it's accurate. Stale context is worse than no context.

Maintenance habits:
- Update `active-projects.md` when a project status changes
- Add an ADR to `decisions.md` every time you make a significant technical choice
- Review `about-you.md` every few months — stacks change
- Rebuild the Ollama model after major brain updates
