# SDD Steering Command

Update `steering/` so it matches the actual repository.

## Scope

- Read `README.md`, `pyproject.toml`, `src/`, `tests/`, and existing `steering/*.md`.
- Treat code and tests as the source of truth when steering is stale.
- Keep English `.md` as the reference version. Update `.ja.md` only after the English file is correct.

## Required Outputs

- `steering/structure.md`
- `steering/tech.md`
- `steering/product.md`
- matching `.ja.md` files when they already exist

## Rules

- Do not invent frameworks, directories, or commands that are not present.
- Use the actual package names: `music_metadata_lib` and `music_metadata_tool`.
- If a referenced file under `steering/rules/` does not exist, remove the reference instead of documenting a nonexistent workflow.
- Summarize the changes you made and list any remaining inconsistencies.
