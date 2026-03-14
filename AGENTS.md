# MUSUBI - workspace

機能1：指定フォルダ以下にある音楽ファイルのメタデータを一覧で出力。機能2：メタデータCSVをインポートし指定フォルダ内の音楽ファイルメタデータを更新する。その他：CSVの更新はEXCELなどで行うので機能化は不要

## Initialized with MUSUBI SDD for Codex CLI

This project uses MUSUBI as a documentation workflow, but Codex should follow the repository reality first.

### Prompts

- `/prompts:sdd-steering` - sync steering docs with the current codebase
- `/prompts:sdd-requirements <feature>` - write `storage/specs/<feature>/requirements.md`
- `/prompts:sdd-design <feature>` - write `storage/specs/<feature>/design.md`
- `/prompts:sdd-tasks <feature>` - write `storage/specs/<feature>/tasks.md`
- `/prompts:sdd-implement <feature>` - implement from the existing specs
- `/prompts:sdd-validate <feature>` - validate spec and implementation consistency

### Project Memory

- `steering/structure.md` - architecture patterns
- `steering/tech.md` - technology stack
- `steering/product.md` - product context
- `steering/rules/constitution.md` - governance rules

### Notes For Codex

- Prefer `storage/specs/<feature>/` over legacy flat files in `storage/specs/`.
- `.codex/AGENTS.md` is the Codex-specific instruction source for this workspace.
- `.codex/prompts/` files are maintained for Codex and should remain short and concrete.

---

**Agent**: Codex CLI
**Initialized**: 2025-12-15
**MUSUBI Version**: 0.1.0
