# Next.js App Structure (App Router)

## When to use
Next.js 13+ with App Router. Works for marketing sites, SaaS dashboards, e-commerce.

## Full structure

```
my-app/
├── app/                          ← Next.js App Router (routes only)
│   ├── (auth)/                   ← route group — no URL segment
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── (dashboard)/              ← route group
│   │   ├── layout.tsx
│   │   └── [feature]/
│   │       └── page.tsx
│   ├── api/                      ← API routes
│   │   └── [resource]/
│   │       └── route.ts
│   ├── layout.tsx                ← root layout
│   ├── page.tsx                  ← home page
│   └── globals.css
│
├── features/                     ← all domain logic (the real work)
│   ├── auth/
│   │   ├── index.ts              ← public API
│   │   ├── LoginForm.tsx
│   │   ├── useAuth.ts
│   │   ├── auth.service.ts       ← server-side auth logic
│   │   ├── auth.types.ts
│   │   └── auth.test.ts
│   └── [feature]/
│       ├── index.ts
│       ├── [Feature]Card.tsx
│       ├── use[Feature].ts
│       ├── [feature].service.ts
│       ├── [feature].types.ts
│       └── [feature].test.ts
│
├── lib/                          ← shared, domain-agnostic utilities
│   ├── db/
│   │   └── client.ts             ← Supabase / Prisma client singleton
│   ├── api/
│   │   └── response.ts           ← standard API response helpers
│   ├── validation/
│   │   └── schemas.ts            ← shared zod schemas
│   └── utils/
│       ├── formatCurrency.ts
│       ├── formatDate.ts
│       └── cn.ts                 ← classname utility
│
├── components/                   ← shared UI only (no domain logic)
│   ├── ui/                       ← shadcn/ui or your design system
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Modal.tsx
│   └── layout/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── Footer.tsx
│
├── config/
│   ├── env.ts                    ← validated env vars (zod)
│   └── site.ts                   ← site metadata, constants
│
├── types/
│   └── index.ts                  ← shared TypeScript types
│
├── public/                       ← static assets
├── .env.example
├── .env                          ← gitignored
├── next.config.ts
├── tsconfig.json
├── package.json
└── CLAUDE.md                     ← copy from agent-os, point to brain/
```

## Key rules

- `app/` contains **routes and layouts only** — no business logic
- Business logic lives in `features/` and is imported by `app/`
- `lib/` has zero domain knowledge — it could be moved to any project
- `components/` is shared UI only — feature-specific components live in `features/[feature]/`
- Never import from `features/a/` into `features/b/` — go through a shared `lib/` or `types/` instead
- API routes in `app/api/` call service functions in `features/` — no logic inline

## Naming conventions

| Type | Pattern | Example |
|------|---------|---------|
| Pages | `page.tsx` | `app/login/page.tsx` |
| Layouts | `layout.tsx` | `app/(dashboard)/layout.tsx` |
| API routes | `route.ts` | `app/api/users/route.ts` |
| Components | PascalCase | `UserCard.tsx` |
| Hooks | camelCase with `use` | `useAuth.ts` |
| Services | camelCase with `.service` | `auth.service.ts` |
| Types | camelCase with `.types` | `auth.types.ts` |
| Tests | same name with `.test` | `auth.test.ts` |

## Environment variables

```bash
# config/env.ts — always validate at startup
import { z } from 'zod'

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  NEXT_PUBLIC_APP_URL: z.string().url(),
})

export const env = envSchema.parse(process.env)
```

## What to add to brain/coding-standards.md

```
## Next.js structure
- app/ = routes only. No logic.
- features/ = domain logic. One folder per domain.
- lib/ = shared utilities with zero domain knowledge.
- components/ = shared UI only. Feature UI lives in features/.
- Validate env vars in config/env.ts at startup with zod.
- API routes call feature services — no inline logic in route.ts.
```
