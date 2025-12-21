# Scan Tasks

**Feature**: scan (metadata export)
**Scope**: 実装・テスト・CLI 統合までのタスク分解

## Task Breakdown

1. **Define ports and DTOs (Application)**
   - Create `ScanRow` DTO and `ScanRequest` input model
   - Define ports: `AudioScannerPort`, `MetadataReaderPort`, `DelimitedWriterPort`
   - Traceability: REQ-SCAN-001, REQ-SCAN-005, REQ-SCAN-006

2. **Implement application use case**
   - Implement `ScanDirectoryUseCase`
   - Handle output destination (STDOUT vs file path)
   - Select delimiter based on `.tsv` extension
   - Traceability: REQ-SCAN-002, REQ-SCAN-003, REQ-SCAN-004, REQ-SCAN-009, REQ-SCAN-010

3. **Infrastructure adapters**
   - `AudioScannerAdapter`: recursive scan, extension filter, sorted output
   - `MetadataReaderAdapter`: Mutagen tag extraction, empty field on missing tag
   - `DelimitedWriterAdapter`: CSV/TSV header + row streaming
   - Traceability: REQ-SCAN-001, REQ-SCAN-005, REQ-SCAN-006, REQ-SCAN-007, REQ-SCAN-009

4. **CLI wiring**
   - Add `scan` command options: input directory, output path
   - Map CLI errors to non-zero exit with message
   - Traceability: REQ-SCAN-002, REQ-SCAN-003, REQ-SCAN-008

5. **Tests (Test-first)**
   - Unit tests: extension filtering, delimiter selection, header ordering
   - Integration tests: Mutagen reads real sample files
   - CLI tests: STDOUT vs file output behavior
   - Traceability: REQ-SCAN-001..010

6. **Docs**
   - Update README with scan usage example
   - Traceability: REQ-SCAN-002, REQ-SCAN-003

