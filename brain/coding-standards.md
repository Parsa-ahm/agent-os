# Coding Standards

## Always
- TypeScript strict mode
- pnpm (Node), uv (Python)
- zod or pydantic for all external data validation
- Conventional commits: feat: fix: chore: docs: refactor: test:
- Explicit error handling — no silent failures
- .env for all secrets, .env.example as the committed template

## Never
- Hardcode secrets or tokens
- console.log in production code
- Force push to main
- Install unknown packages without reviewing them

## Security
- Run security review before any client-facing PR
- Sanitize all user input
- Never log PII or API tokens
- Rate limit all user-facing endpoints
- Untrusted code → sandbox first, review before running
