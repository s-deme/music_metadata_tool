# SDD Change Init Command

Create a concise change proposal for a brownfield change.

## Output Path

- `storage/changes/<change-name>/proposal.md`

## Process

1. Read the relevant steering docs, specs, code, and tests.
2. Describe current behavior, intended change, affected files, risks, and verification plan.
3. Keep the proposal specific to this repository and feature set.

## Rules

- Do not require interactive question tools.
- Do not use placeholder tokens.
- If `storage/changes/` does not exist, create it only when you are actually writing a proposal.
