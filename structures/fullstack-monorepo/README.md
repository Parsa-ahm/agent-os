# Full-Stack Monorepo Structure

## When to use
A single repo containing a frontend, backend, and shared packages.
Use pnpm workspaces (Node) or uv workspaces (Python).

## Full structure

```
my-project/
├── apps/
│   ├── web/                      ← Next.js frontend (see structures/nextjs/)
│   │   ├── app/
│   │   ├── features/
│   │   ├── lib/
│   │   ├── package.json
│   │   └── CLAUDE.md
│   │
│   └── api/                      ← Backend API (see structures/python-api/)
│       ├── src/
│       ├── pyproject.toml
│       └── CLAUDE.md
│
├── packages/                     ← shared code (imported by apps/)
│   ├── types/                    ← shared TypeScript types
│   │   ├── src/
│   │   │   └── index.ts
│   │   └── package.json
│   │
│   ├── ui/                       ← shared component library
│   │   ├── src/
│   │   │   ├── Button.tsx
│   │   │   └── index.ts
│   │   └── package.json
│   │
│   └── config/                   ← shared configs (eslint, tsconfig, etc.)
│       ├── eslint-base.js
│       └── tsconfig.base.json
│
├── scripts/
│   ├── setup.sh                  ← one-command setup
│   └── dev.sh                    ← starts all services
│
├── .env.example                  ← all vars for all apps
├── pnpm-workspace.yaml
├── package.json                  ← root scripts only
├── turbo.json                    ← turborepo pipeline (optional)
└── CLAUDE.md                     ← root context, points to brain/
```

## Key rules

- `apps/` contains runnable applications — each has its own CLAUDE.md
- `packages/` contains code imported by apps — never runnable on its own
- `packages/types/` is the single source of truth for shared data shapes
- Apps never import from each other — only from `packages/`
- Each app has its own `.env` — no shared env files (different secrets per service)
- Root `package.json` has only workspace scripts — no app-level dependencies

## Dependency flow

```
apps/web  ──────┐
                ├── packages/types
apps/api  ──────┘
                └── packages/config

apps/web ─────────── packages/ui
```

`apps` depend on `packages`. `packages` depend on each other with care.
Never: `apps/web` imports from `apps/api`.

## pnpm workspace setup

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

```json
// packages/types/package.json
{
  "name": "@myapp/types",
  "main": "./src/index.ts",
  "exports": { ".": "./src/index.ts" }
}
```

```json
// apps/web/package.json — import shared types
{
  "dependencies": {
    "@myapp/types": "workspace:*"
  }
}
```

## When NOT to use a monorepo

- Solo project with one frontend and one backend that rarely share code
- If you're spending more time configuring the monorepo than building features
- Start with separate repos and monorepo when you feel the friction of code duplication

## What to add to brain/coding-standards.md

```
## Monorepo structure
- apps/ = runnable applications. Each has own CLAUDE.md and .env.
- packages/ = shared code imported by apps. Not runnable standalone.
- Apps never import from each other — only from packages/.
- packages/types/ is the single source of truth for shared types.
- pnpm workspaces for Node, uv workspaces for Python.
```
