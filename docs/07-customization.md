# Customization

## What to personalize vs. what to leave alone

| Component | Personalize | Leave alone |
|-----------|-------------|-------------|
| `brain/about-you.md` | Yes — fill in completely | — |
| `brain/active-projects.md` | Yes — your projects | — |
| `brain/decisions.md` | Yes — your ADRs | — |
| `brain/coding-standards.md` | Yes — your rules | — |
| `brain/ai-behavior.md` | Yes — tone/style | Core directness rules |
| `.claude/rules/common/` | Extend, don't delete | Security rules |
| `agents/*.md` | Extend with project-specific agents | — |
| `ollama/Modelfile` | Yes — fill in your stack | temperature/ctx params |
| `docs/` | Don't modify | — |

## Step-by-step: making it yours

### 1. Fill in the brain (required)

`brain/about-you.md` is the most important file. Fill it in before anything else.
Be specific: list your actual stack, your package managers, your deployment targets.
Vague entries produce vague AI responses.

### 2. Adjust coding standards

`brain/coding-standards.md` has sensible defaults. Change them to match your actual rules:
- Different package manager? Update it.
- Different validation library? Change zod/pydantic.
- Different commit format? Update it.

### 3. Build your local model

```bash
cp ollama/Modelfile.template ollama/Modelfile
# Edit ollama/Modelfile — paste your brain content into the system prompt
bash scripts/create-model.sh my-coder
```

### 4. Cursor integration

Copy `cursor/rules.md` content into `.cursorrules` in each project that uses this environment.
Or set it as a global Cursor rule in Settings.

### 5. Add project-specific agents

If you have recurring workflows that need specific AI behavior, add an agent definition to `agents/`.
Format: purpose, when to invoke, what it produces, behavior rules.

### 6. Add language-specific rules

`.claude/rules/` has `common/`, `typescript/`, and `python/` directories.
Add a folder for any other language you work in.

## Adjusting the routing table

`agents/local-router.md` defines what goes to which model.
The defaults are conservative (route up when unsure).
You can shift the boundaries based on how capable your local model is.

If you're running a 14B or 32B model locally, you can push more to it.
If you're on a slower machine with a 7B, keep the table as-is.

## Multi-person teams

If you're using this with a team:
- Keep `brain/about-you.md` as a template (don't commit personal details)
- Add a `brain/team.md` for shared team context (stack, conventions, repo links)
- Each person fills in their own local `about-you.md` (gitignored)
- `coding-standards.md` and `decisions.md` are shared and committed

## Updating after changes

When you change the brain significantly:
1. Update `brain/` files
2. Rebuild the Ollama model: `bash scripts/create-model.sh`
3. Cursor picks up changes automatically (reads `.cursorrules` on each session)
4. Claude Code picks up changes automatically (reads `brain/` on each session via CLAUDE.md)
