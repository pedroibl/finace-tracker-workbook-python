# Excel Budget Generator v1.0.0

Release date: _TBD_

## Highlights
- Full multi-sheet workbook generation (Settings, Dropdown Data, Budget-Planning, Budget Tracking, Calculations, Budget Dashboard) aligned with the PRD design targets.
- Dynamic named range infrastructure powering validations, cross-sheet formulas, and dashboard selectors.
- Dashboard KPI tiles and doughnut charts backed by the Calculations sheet metrics pipeline.
- Integration and golden-regression coverage: 46 automated tests with 95 % line coverage.

## Verification Snapshot
- `pytest --cov=budget_generator --cov-report=term` → 46 passed / 95 % coverage.
- Golden workbook parity (`pytest -k output`) against `tests/fixtures/golden_tutorial.xlsx`.
- CLI smoke test: `budget-generator -v generate examples/tutorial_spec.json -o build/tutorial.xlsx`.
- Updated design references: `OutcomeExpected.xlsx` and `build/outcome_expected_details.json`.

## Known Follow-Ups
- Package build blocked in current sandbox because `setuptools` cannot be downloaded; rerun `python -m build` once internet access is available.
- Manual validation in Microsoft 365 + LibreOffice and screenshot capture still required per `docs/release-checklist.md`.
- Git tagging/push and GitHub release publication must happen from a git-enabled environment.

## Artifacts
- Generated workbook: `build/tutorial.xlsx`
- Golden workbook: `tests/fixtures/golden_tutorial.xlsx`
- Design reference: `OutcomeExpected.xlsx`

## Upgrade Notes
- No breaking CLI changes; install wheel/zip once packaging artifacts are produced.
- New named ranges (`DashYear`, `DashPeriod`, `MonthMap`, etc.) land with this release—review downstream integrations that rely on the workbook schema.
