# Task Routing

## The rule

Use the cheapest model that can do the job correctly.
Frontier model tokens are expensive and slow. Local is free and instant.
Don't use a sledgehammer for a finishing nail.

## Routing table

| Task | Model | Why |
|------|-------|-----|
| CSS/styling fix | Local (Ollama) | Mechanical substitution |
| .env / config edit | Local (Ollama) | Text substitution |
| Boilerplate (CRUD, form, basic component) | Local (Ollama) | Pattern-based |
| README / doc edits | Local (Ollama) | Text only |
| Small rename / refactor (<20 lines, 1 file) | Cursor/Codex | In-editor context |
| Test generation for simple functions | Cursor/Codex | Pattern-based |
| Component wiring in existing patterns | Cursor/Codex | Context-aware completions |
| Bug investigation | Claude | Reasoning required |
| New feature design | Claude | Planning required |
| Multi-file refactor | Claude | Cross-file context |
| Architecture decisions | Claude + dual-review gate | Critical, see doc 03 |
| Security review | Claude | Non-negotiable |
| Anything touching auth / payments / PII | Claude | High risk |

## Decision flowchart

```
Is this a critical path item (architecture/security/data model)?
  YES → Dual-review gate (docs/03-dual-review-gate.md)
  NO  ↓

Does it require reasoning, investigation, or multi-file context?
  YES → Claude
  NO  ↓

Is it in-editor, using existing patterns in the current file?
  YES → Cursor/Codex
  NO  ↓

Is it mechanical (CSS, config, text edits, boilerplate)?
  YES → Local (Ollama)
  NO  → Claude (default up when unsure)
```

## Token cost in practice

A typical dev day before routing discipline:
- 200 Claude messages × ~2000 tokens avg = ~400k tokens
- At Sonnet rates: ~$1.20/day just in routine tasks

With routing:
- 40 Claude messages (complex only) = 80k tokens = ~$0.24
- 80 Codex messages (in-editor) = ~$0.10
- 80 local model runs = $0.00
- Total: ~$0.34/day — ~70% savings on routine work

The goal isn't penny-pinching. It's that when Claude is reserved for hard problems,
its responses are more focused and the conversation context stays relevant.

## When to break the rules

- Security and risk escalate: if in doubt about a routing call, go to Claude
- Local model says it can't handle something: route up immediately
- Codex produces something that doesn't feel right: have Claude review it
