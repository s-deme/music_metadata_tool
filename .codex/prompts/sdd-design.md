# SDD Design Command

Create or update the design document for a feature.

## Canonical Paths

- `storage/specs/<feature>/requirements.md`
- `storage/specs/<feature>/design.md`

## Process

1. Read the feature requirements and the relevant implementation and tests.
2. Describe the current or target design in terms of Python modules, data flow, CLI entry points, and adapters.
3. Reference real files and real commands only.
4. Record important tradeoffs and constraints that matter to implementation.

## Rules

- Do not mention nonexistent directories like `lib/<feature>/` unless they actually exist.
- Do not require templates or external agent roles.
- Keep the design aligned with `src/music_metadata_lib/`, `src/music_metadata_tool/`, and `tests/`.
