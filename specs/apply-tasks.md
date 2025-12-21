# Apply Tasks

**Feature**: apply (metadata import)
**Scope**: 実装・テスト・CLI 統合までのタスク分解

## Task Breakdown

1. **Define ports and DTOs (Application)**
   - Create `ApplyRowData` DTO and `ApplyRequest`
   - Define ports: `DelimitedReaderPort`, `MetadataWriterPort`
   - Traceability: REQ-APPLY-001, REQ-APPLY-007

2. **Implement application use case**
   - Implement `ApplyMetadataUseCase`
   - Validate input path, resolve relative paths
   - Dry-run vs write behavior
   - Traceability: REQ-APPLY-002, REQ-APPLY-003, REQ-APPLY-004, REQ-APPLY-005, REQ-APPLY-006, REQ-APPLY-007

3. **Infrastructure adapters**
   - `DelimitedReaderAdapter`: CSV/TSV parsing + header validation
   - `MetadataWriterAdapter`: Mutagen 書き込み
   - Traceability: REQ-APPLY-001, REQ-APPLY-004

4. **CLI wiring**
   - Add `apply` command options: input path, `--write`
   - Map errors to non-zero exit
   - Traceability: REQ-APPLY-003, REQ-APPLY-005

5. **Tests (Test-first)**
   - Unit tests: headers, delimiter, path resolution, dry-run
   - CLI tests: non-zero exit on missing file
   - Traceability: REQ-APPLY-001..007

6. **Docs**
   - Update README with apply usage example
   - Traceability: REQ-APPLY-003, REQ-APPLY-004
