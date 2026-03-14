# Codex Workspace Guide

This repository uses Codex CLI as the primary coding agent.

## Purpose

- `scan`: recursively read music file metadata and export CSV/TSV
- `apply`: import CSV/TSV and update metadata in a target directory
- editing of CSV itself is intentionally out of scope

## Codex Rules For This Repo

- Prefer the real implementation and tests over stale steering text when they conflict.
- Treat `storage/specs/<feature>/` as the canonical location for feature specs.
- Legacy flat files such as `storage/specs/scan-design.md` may exist; do not create new ones unless the user explicitly asks.
- Keep instructions concise. Do not emulate multi-agent orchestration, Claude-only tools, or placeholder templates.
- Use the Python/Docker workflow documented in `README.md`.

## Actual Project Shape

- Python project managed by `pyproject.toml`
- Main packages: `src/music_metadata_lib/` and `src/music_metadata_tool/`
- Tests: `tests/`
- Steering docs: `steering/*.md`
- Specs: `storage/specs/<feature>/requirements.md`, `design.md`, `tasks.md`

## Validation Commands

Use the least expensive command that proves the change:

- `docker compose run --rm app python -m pytest -q`
- `docker compose run --rm app python -m music_metadata_tool.interface.cli.main --help`

## Prompt Files

Files under `.codex/prompts/` are lightweight Codex-oriented workflow guides for this repository. They must stay aligned with the real directory layout and must not reference unsupported tools such as `TodoWrite` or `AskUserQuestion`.
