# SDD Validate Command

Validate that a feature's specs and implementation are consistent.

## Canonical Paths

- `storage/specs/<feature>/requirements.md`
- `storage/specs/<feature>/design.md`
- `storage/specs/<feature>/tasks.md`

## Validation Targets

- relevant source files under `src/`
- relevant tests under `tests/`
- README or user-facing docs when behavior changed

## Process

1. Compare requirements, design, tasks, code, and tests.
2. List concrete mismatches first.
3. If no mismatch is found, state that explicitly and note residual risk.
4. Run the smallest useful verification command.

## Rules

- Do not invoke external reviewer personas.
- Do not assume directories or commands that are not present.
- Keep the report tied to real files and observed behavior.
