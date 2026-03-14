# SDD Change Apply Command

Apply an approved change proposal to the codebase.

## Inputs

- `storage/changes/<change-name>/proposal.md`
- any affected feature specs under `storage/specs/`

## Process

1. Read the proposal, then inspect the impacted code and tests.
2. Implement the change with the smallest coherent patch set.
3. Update affected specs and docs if behavior changed.
4. Verify with targeted tests or CLI checks.

## Rules

- Use the existing Python project layout.
- Do not scaffold unrelated APIs, frontend routes, or library layouts.
- Stop and report if the proposal depends on missing prerequisites.
