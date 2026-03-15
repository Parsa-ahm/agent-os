# CLI Tool Structure

## When to use
Command-line tools in Node.js (tsx/ts-node) or Python (uv).

## Node.js CLI

```
my-cli/
├── src/
│   ├── index.ts                  ← entry point, command registration
│   ├── commands/                 ← one file per command
│   │   ├── init.ts
│   │   ├── run.ts
│   │   └── config.ts
│   ├── lib/                      ← shared utilities
│   │   ├── config.ts             ← read/write config file (~/.mytool/config.json)
│   │   ├── logger.ts             ← stdout/stderr formatting
│   │   └── errors.ts
│   └── types/
│       └── index.ts
│
├── tests/
├── .env.example
├── package.json
├── tsconfig.json
└── CLAUDE.md
```

## Python CLI

```
my-cli/
├── src/
│   └── my_cli/
│       ├── __init__.py
│       ├── main.py               ← entry point (typer or click app)
│       ├── commands/             ← one file per command group
│       │   ├── init.py
│       │   └── run.py
│       ├── lib/
│       │   ├── config.py         ← read/write ~/.mytool/config.toml
│       │   ├── output.py         ← rich / click echo helpers
│       │   └── errors.py
│       └── types.py
│
├── tests/
├── .env.example
├── pyproject.toml
└── CLAUDE.md
```

## Key rules

- One file per command — commands are not methods in a class
- `lib/config.ts` handles the user config file (~/.toolname/config.json) — not inline
- Never print directly — use the logger/output helper (makes testing easier)
- Commands validate their own args — use zod (Node) or typer's type hints (Python)

## What to add to brain/coding-standards.md

```
## CLI tool structure
- commands/ = one file per top-level command
- lib/config = handles user config file, not inline
- All output through logger/output helper, never print/console.log directly
- Commands validate their own args before doing anything
```
