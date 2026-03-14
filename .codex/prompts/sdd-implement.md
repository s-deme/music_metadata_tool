# SDD Implement Command

Implement a feature from the existing specs.

## Canonical Paths

- `storage/specs/<feature>/requirements.md`
- `storage/specs/<feature>/design.md`
- `storage/specs/<feature>/tasks.md`

## Process

1. Read the three feature spec files if they exist.
2. Inspect the current implementation and tests before editing.
3. Make the smallest coherent change that satisfies the task.
4. Verify with relevant tests or CLI checks.
5. Update specs only if the implementation changed the intended behavior.

## Rules

- Use Codex tools that exist in this environment, not Claude-specific tools.
- Use actual project paths and package names.
- Prefer `apply_patch` for manual edits.
- Report any missing prerequisites instead of inventing files or commands.
