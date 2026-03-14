# SDD Requirements Command

Create or update requirements for a feature in this repository.

## Input

- Feature name, for example `scan` or `apply`

## Canonical Path

- `storage/specs/<feature>/requirements.md`

## Process

1. Read the current code, tests, README, and existing spec files for the feature.
2. Derive requirements from actual behavior unless the user explicitly requests new behavior.
3. Write concise EARS-style requirements with stable IDs.
4. Include assumptions, constraints, and open questions only when they are real.

## Rules

- Prefer `storage/specs/<feature>/requirements.md` over legacy flat files.
- Do not use placeholder tokens such as `{{feature}}`.
- Keep the content specific to this Python CLI project.
- If the code and older spec disagree, note the mismatch explicitly.
