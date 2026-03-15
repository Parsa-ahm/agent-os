# Folder Architecture

Good folder structure isn't about aesthetics. It's about:

1. **AI legibility** — your AI tools navigate by path. Predictable structure means faster, more accurate edits.
2. **Cognitive load** — where does a new file go? If you have to think about it, the structure is wrong.
3. **Scalability** — structure that works at 10 files should still work at 200. Most don't.
4. **Boundary enforcement** — folders are architecture made visible. `lib/` should not import from `app/`. That boundary is clearest when the folders make it obvious.

---

## Core Principles

### 1. Feature-first, not type-first

```
# Wrong — type-first (everything in one bucket)
src/
  components/
    UserCard.tsx
    ProductCard.tsx
    CheckoutForm.tsx
  hooks/
    useUser.ts
    useProduct.ts
    useCheckout.ts
  utils/
    userUtils.ts
    productUtils.ts

# Right — feature-first (co-located by domain)
src/
  features/
    user/
      UserCard.tsx
      useUser.ts
      userUtils.ts
    product/
      ProductCard.tsx
      useProduct.ts
      productUtils.ts
    checkout/
      CheckoutForm.tsx
      useCheckout.ts
```

Why: when you touch the user feature, all relevant files are in one place.
Type-first means a single feature change touches 4 different directories.
AI assistants also navigate features far more accurately than type buckets.

### 2. Depth signals importance

```
src/           ← entry points and wiring only
  app/         ← routes / pages
  features/    ← domain logic (the real work)
  lib/         ← shared utilities (no domain knowledge)
  config/      ← environment and app configuration
```

The shallower the import path, the more foundational the code.
`lib/` should have zero knowledge of your domain.
`features/user/` should have zero knowledge of `features/checkout/`.

### 3. The 3-file rule for new features

Every new feature starts with exactly 3 files:
1. The thing itself (`UserCard.tsx`)
2. Its logic (`useUser.ts` or `user.service.ts`)
3. Its tests (`user.test.ts`)

No more until you need more. Premature folder expansion is the same as premature abstraction.

### 4. Colocation over DRY (until it's actually shared)

Don't extract to `lib/` until two different features need the same code.
Duplication is cheaper than wrong abstraction.
When you do extract, the extraction is obvious because you're eliminating real duplication.

### 5. The index file rule

`index.ts` files are public API declarations.
If it's not exported from `index.ts`, it's internal to that feature.
This gives you a clear boundary and makes refactoring cheaper.

```
features/user/
  index.ts        ← exports: UserCard, useUser (public API)
  UserCard.tsx    ← internal implementation
  useUser.ts      ← internal implementation
  user.types.ts   ← internal types
  user.test.ts    ← tests
```

### 6. Name what it does, not what it is

```
# Wrong — names what it is
UserComponent.tsx
DataService.ts
HelperUtils.ts

# Right — names what it does
UserCard.tsx
user.service.ts
formatCurrency.ts
```

---

## Structure Templates

See `structures/` for full templates per project type:

| Template | Use case |
|----------|----------|
| [`structures/nextjs/`](../structures/nextjs/README.md) | Next.js app (App Router) |
| [`structures/python-api/`](../structures/python-api/README.md) | FastAPI / Flask service |
| [`structures/fullstack-monorepo/`](../structures/fullstack-monorepo/README.md) | Full-stack with shared packages |
| [`structures/automation/`](../structures/automation/README.md) | n8n / automation projects |
| [`structures/cli-tool/`](../structures/cli-tool/README.md) | CLI tool (Node or Python) |

---

## How folders and agent-os work together

AI tools navigate your project by path. The more predictable your structure, the better they perform.

**What to add to `brain/coding-standards.md`:**
```markdown
## Folder structure
- Feature-first: all files for a domain live together in features/
- lib/ contains only domain-agnostic utilities
- New feature = 3 files: the thing, its logic, its tests
- Nothing in lib/ imports from features/
- index.ts declares the public API of each feature
```

When Claude or Cursor knows these rules, they'll place new files correctly without being told.

**In your Modelfile:**
Add the same rules to the system prompt. Your local model handles boilerplate generation —
knowing your folder conventions means it generates files in the right place.

---

## Scaling guide

```
Phase 1 — Single feature (1-5 files)
  src/
    feature.ts
    feature.test.ts

Phase 2 — Multiple features (5-30 files)
  src/
    features/
      user/
      product/
    lib/
    config/

Phase 3 — Large app (30-200 files)
  src/
    features/     ← domain logic
    lib/          ← shared utilities
    config/       ← configuration
    types/        ← shared TypeScript types
    middleware/   ← cross-cutting concerns (auth, logging)

Phase 4 — Monorepo (200+ files)
  See structures/fullstack-monorepo/
```

Don't jump to Phase 4 from Phase 1. Add structure only when you feel the friction of not having it.
