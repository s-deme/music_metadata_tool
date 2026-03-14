# SDD Tasks Command

Break a feature into implementation tasks that are actionable in this repository.

## Canonical Paths

- `storage/specs/<feature>/requirements.md`
- `storage/specs/<feature>/design.md`
- `storage/specs/<feature>/tasks.md`

## Process

1. Read the current requirements and design for the feature.
2. Produce a small ordered task list with dependencies and verification notes.
3. Anchor tasks to real files, tests, and commands in this repo.
4. Prefer tasks that can be completed and verified independently.

## Rules

- Do not generate boilerplate task hierarchies unrelated to the feature.
- Do not reference unsupported tools such as `TodoWrite`.
- Use Python and Docker commands that already exist in `README.md`.
