# Automation Project Structure

## When to use
n8n workflows, AI pipelines, webhook handlers, scheduled jobs, data pipelines.
Anything where the product IS the automation, not a user-facing app.

## Full structure

```
my-automation/
├── workflows/                    ← n8n workflow exports (JSON)
│   ├── lead-qualifier.json
│   └── notification-sender.json
│
├── src/                          ← custom code nodes and scripts
│   ├── agents/                   ← AI agent definitions
│   │   ├── lead-scorer.ts        ← scoring logic called by n8n
│   │   └── message-formatter.ts
│   │
│   ├── integrations/             ← third-party API wrappers
│   │   ├── telegram.ts
│   │   ├── supabase.ts
│   │   └── gemini.ts
│   │
│   ├── lib/                      ← shared utilities
│   │   ├── validation.ts         ← zod schemas for all external data
│   │   ├── logger.ts
│   │   └── errors.ts
│   │
│   └── config/
│       └── env.ts                ← validated env vars
│
├── prompts/                      ← LLM prompt templates
│   ├── lead-score.md             ← scoring prompt
│   └── message-draft.md         ← message generation prompt
│
├── tests/
│   ├── agents/
│   └── integrations/
│
├── scripts/
│   ├── export-workflows.sh       ← export from n8n instance
│   └── import-workflows.sh       ← import to n8n instance
│
├── docs/
│   └── workflow-map.md           ← plain-language description of each workflow
│
├── .env.example
├── .env                          ← gitignored
├── package.json                  ← (or pyproject.toml)
└── CLAUDE.md
```

## Key rules

- Prompts are files, not strings — `prompts/` stores all LLM prompt templates as markdown
- Every external API call is wrapped in `integrations/` — no inline API calls in agents
- All external data (webhook payloads, API responses) is validated with zod/pydantic before use
- Workflows are exported and version-controlled as JSON — never only live in the n8n UI
- `docs/workflow-map.md` describes each workflow in plain language — this is what AI reads to understand the system

## Prompt file format

```markdown
<!-- prompts/lead-score.md -->
# Lead Scorer

## Task
Score the following lead on a scale of 1-10 based on buying intent signals.

## Input
Lead comment: {{comment}}
Platform: {{platform}}

## Output format
Respond with JSON only:
{"score": <1-10>, "reason": "<one sentence>", "follow_up": <true|false>}

## Scoring criteria
- 8-10: Direct question about pricing, availability, or "how to buy"
- 5-7: Strong interest signals ("I need this", "how does it work")
- 1-4: Casual engagement, no intent signals
```

## What to add to brain/coding-standards.md

```
## Automation project structure
- workflows/ = n8n exports, version controlled
- prompts/ = all LLM prompts as markdown files, never inline strings
- integrations/ = all third-party API wrappers
- All external data validated with zod before processing
- docs/workflow-map.md describes every workflow in plain language
```

## AI context hint

Add `docs/workflow-map.md` as a path in your `CLAUDE.md`.
When AI knows your workflow map, it can make changes to agents and integrations
that are consistent with the automation design — without you explaining it every time.
