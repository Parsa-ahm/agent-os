# The Dual-Review Gate

## What it is

Critical decisions — architecture, security design, data models, API contracts, auth flows —
must be reviewed by two independent AI models before you write a single line of implementation code.

One model's blind spots are not the other's. Claude and Codex are trained differently, on different data,
with different tendencies. A design flaw that one misses, the other often catches.

## What triggers the gate

A decision hits the gate if it affects any of these:

- **Architecture** — how components connect, what owns what, module boundaries
- **Security** — auth flows, session management, permission models, data access rules
- **Data models** — schema design, relationships, migrations that can't be undone
- **API contracts** — public endpoints, request/response shapes, versioning
- **Payments / PII** — anything touching money or personal data

When in doubt: put it through the gate. The cost is 10 minutes. The cost of not doing it is hours of untangling.

## The workflow

```
Step 1 — Claude drafts the design
  Claude proposes architecture/design in plain language (not code yet).
  This becomes the "proposal document".

Step 2 — Codex independently reviews
  Paste the proposal into Cursor with this prompt:
  "Review this design proposal as a senior engineer.
   Flag any architectural problems, security gaps, missing edge cases,
   or better alternatives. Be direct — no softening."

Step 3 — Claude reconciles
  Paste Codex's review back into Claude:
  "Codex flagged the following issues with our design proposal: [paste].
   For each point: is it valid? If yes, how do we address it?
   Update the proposal with the resolved version."

Step 4 — You decide
  Claude presents the final reconciled proposal.
  You read both the original and the changes.
  You approve, modify, or reject.
  Only after your approval does implementation begin.
```

## How Claude asks for confirmation

When Claude reaches step 4, it will explain:

- **What** the proposal is (plain language, not code)
- **Why** each key decision was made
- **What Codex flagged** and how it was resolved
- **What you're approving** — what will be built if you say yes
- **What changes if you say no** — alternative paths

It will NOT just show a command or a code block and ask "proceed?".

## Example

**Bad confirmation request:**
> "Shall I implement this with JWT stored in localStorage?"

**Good confirmation request:**
> "The auth design uses JWT tokens stored in httpOnly cookies (not localStorage).
>
> Why: httpOnly cookies prevent XSS from reading the token. localStorage is accessible
> to any JavaScript on the page, which is a known attack vector.
>
> Codex flagged that we need to set SameSite=Strict and handle token refresh.
> I've added both to the proposal.
>
> If you approve: I'll implement the login endpoint, cookie-setting logic,
> and a refresh endpoint. No client-side token storage.
>
> If you decline: we can discuss an alternative flow. What's your concern?
>
> Proceed?"

## Why two models

No AI is right 100% of the time. Each has trained biases and blind spots.
Making critical decisions require two independent reviews raises the bar
from "one model's opinion" to "two models that agree (or surfaced a disagreement for you to resolve)".

Your approval is the third check — the human in the loop.
