# Python API Structure (FastAPI / Flask)

## When to use
Any Python backend service — REST API, webhook handler, background worker, AI pipeline.

## Full structure

```
my-api/
├── src/
│   └── app/                      ← application code
│       ├── main.py               ← FastAPI app init, router mounting
│       │
│       ├── features/             ← domain logic (the real work)
│       │   └── [feature]/
│       │       ├── __init__.py
│       │       ├── router.py     ← FastAPI router / Flask blueprint
│       │       ├── service.py    ← business logic
│       │       ├── repository.py ← data access (DB queries)
│       │       ├── schemas.py    ← pydantic request/response models
│       │       ├── models.py     ← SQLAlchemy / ORM models (if used)
│       │       └── test_[feature].py
│       │
│       ├── lib/                  ← shared, domain-agnostic code
│       │   ├── database.py       ← DB connection / session
│       │   ├── auth.py           ← JWT decode, permission checks
│       │   ├── errors.py         ← exception classes
│       │   ├── response.py       ← standard response helpers
│       │   └── logger.py         ← structured logging setup
│       │
│       ├── config/
│       │   └── settings.py       ← pydantic BaseSettings (reads .env)
│       │
│       └── middleware/
│           ├── auth.py           ← auth middleware
│           └── rate_limit.py
│
├── tests/                        ← integration and e2e tests
│   ├── conftest.py               ← pytest fixtures
│   └── test_[feature]/
│
├── scripts/
│   ├── seed.py                   ← DB seeding
│   └── migrate.py
│
├── .env.example
├── .env                          ← gitignored
├── pyproject.toml                ← uv / pip config
├── Dockerfile
└── CLAUDE.md
```

## Key rules

- `features/[feature]/` is self-contained — router, service, repository, schemas together
- `lib/` has zero domain knowledge — used across all features
- `repository.py` is the only file that touches the database
- `service.py` contains all business logic — it calls repository, never the DB directly
- `router.py` does input validation and calls service — no business logic inline
- Never raise HTTP errors in `service.py` — raise domain exceptions, let the router translate them

## The layers

```
Request → router.py → service.py → repository.py → Database
           (validate)  (business)   (data access)
```

Going up the stack: each layer only talks to the layer directly below it.
`router.py` never imports from `repository.py`.
`service.py` never imports from another feature's `service.py`.

## Settings pattern

```python
# config/settings.py — always validate at startup
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    environment: str = "development"

    model_config = {"env_file": ".env"}

settings = Settings()  # raises on startup if required vars missing
```

## Naming conventions

| Type | Pattern | Example |
|------|---------|---------|
| Routers | `router.py` | `features/user/router.py` |
| Services | `service.py` | `features/user/service.py` |
| Repos | `repository.py` | `features/user/repository.py` |
| Schemas | `schemas.py` | `features/user/schemas.py` |
| Tests | `test_[name].py` | `test_user_service.py` |

## What to add to brain/coding-standards.md

```
## Python API structure
- features/ = one folder per domain, self-contained (router, service, repo, schemas)
- lib/ = shared utilities with zero domain knowledge
- router → service → repository — never skip layers
- pydantic BaseSettings for all env vars, validated at startup
- repository.py is the only file that touches the database
```
