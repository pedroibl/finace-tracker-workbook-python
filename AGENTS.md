# Agent Execution Brief

## Mission & Scope
- Deliver the Python Excel Budget Generator v1.0.0 described in `docs/prd-excell-budget-tracker.md` within the eight-week window beginning 2025-10-15.
- Complete every task in the PRD's four phases while respecting the documented priorities (P0–P3) and status states (Not Started, In Progress, Blocked, Complete, Cancelled).
- Keep the PRD as the authoritative plan; this brief distills the execution view for every agent role.

## Source of Truth
- `docs/prd-excell-budget-tracker.md` (latest requirements, task breakdown, verification steps).
- `src/budget_generator/` (implementation packages for sheets, formatting, formulas, utilities, generator, CLI).
- `tests/` (unit and integration coverage, fixtures, regression harness).
- `examples/` (JSON specifications used for end-to-end generation checks).

## Recent Deliverables
- Phase 1 foundation shipped: repo scaffold, dependency management, CLI entry point, JSON loader, workbook generator, and Settings sheet builder with validations.
- Phase 2 delivery complete: Dropdown Data sheet (`src/budget_generator/sheets/dropdown.py`) with formula helpers, named range infrastructure (`utils/named_ranges.py`), and comprehensive tests.
- Budget-Planning sheet (`sheets/planning.py`) now renders full income/expense/savings grids with refreshed color palette, accounting formats, unallocated row, conditional formatting, and configurable multi-year scaffolding per PRD 2.3–2.5.
- Tracking sheet (`sheets/tracking.py`) ships with table layout, validations linked to planning ranges, SUMPRODUCT/late-income formulas, and conditional formatting to highlight NA categories and income rows (PRD 2.6–2.8).
- Planning named ranges are wired via `register_planning_named_ranges`, covering categories, grids, totals, headers, and unallocated row references; tracking sheet consumes these dynamic lists.
- Planning named ranges are wired via `register_planning_named_ranges`, covering categories, grids, totals, headers, and unallocated row references.
- Formatting helpers expanded (`formatting/styles.py`, `formatting/conditional.py`) and 26-test suite green, covering CLI, generator, utilities, and all sheet builders.
- PRD progress tracked live with completed checkboxes; next focus: Phase 3 calculations/dashboard features.
- Calculations sheet (Phase 3, sections 3.1–3.3) implemented with metrics tiles, month mapping, budget-vs-tracked table, new formula helpers, generator orchestration, and expanded test coverage (36 tests total).
- Dashboard sheet structure and selectors (Phase 3, section 3.4) now live with year/period dropdowns, updated generator integration, new named ranges (DashYear/DashPeriod), and dedicated tests.
- Dashboard KPI tiles and doughnut charts (Phase 3, sections 3.5–3.6) implemented with formatting, formulas, reusable chart helpers, and unit tests; generator now orchestrates settings/dropdown named ranges and hides helper sheets, bringing total tests to 39.
- Phase 4 QA underway: tutorial spec fixture, golden workbook, integration suite (`tests/test_integration.py`), output validation checks, README/tutorial mapping, and fallback coverage runner (`scripts/run_coverage.py`); test suite at 46 cases with ~82% line coverage (per fallback script).

## Roles & Responsibilities
### Project Lead
- Maintain the milestone schedule and unblock owners for Phases 1–4.
- Run weekly PRD reviews, keep the Kanban/status icons accurate, and manage stakeholder updates.
- Coordinate release readiness: changelog, checklist, and sign-off sequence.

### Dev Lead
- Drive Phase 1 setup (Sections 1.1–1.6): tooling, dependency management, CLI scaffolding, workbook skeleton, and Settings sheet foundations.
- Define code quality bar (black, ruff, mypy, pytest) and ensure `uv` workflows remain green.
- Partner with Backend Dev to decompose upcoming P0/P1 items into actionable backlog slices.

### Backend Developer
- Implement JSON loader, CLI commands, generator, sheet builders, named range utilities, and advanced dashboard logic (Sections 1.3 through 3.6).
- Keep formulas, conditional formatting, and data validation aligned with the PRD's explicit cell references and color codes.
- Land tests alongside each feature (unit, fixture-backed, and integration) before merging.

### QA Engineer
- Build the Phase 4 verification suite (Section 4.1) targeting at least 80 percent coverage with golden workbook comparisons.
- Automate regression execution via `uv run pytest --cov=budget_generator --cov-report=term` and track flakiness regressions.
- Validate named ranges, formulas, chart rendering, and cross-version Excel compatibility prior to release sign-off.

### Technical Writer
- Produce and maintain README, CLI reference, troubleshooting guide, and onboarding content (Section 4.4).
- Confirm documentation tracks CLI flags, JSON schema changes, release packaging, and known limitations.
- Prepare release notes and post-launch handoff materials in step with the release checklist.

## Phase Roadmap & Exit Criteria
### Phase 1 – Foundation & Setup (Weeks 1–2; PRD Sections 1.1–1.6)
- Install `uv`, scaffold repo layout, configure dependencies, and initialize git metadata.
- Ship JSON loader, CLI group, workbook generator skeleton, and the initial Settings sheet utilities.
- Exit criteria: `uv run budget-generator --help` succeeds; workbook creation writes six sheets with correct visibility; Settings sheet validations operate as described.

### Phase 2 – Core Sheets (Weeks 3–4; PRD Sections 2.1–2.4)
- Implement Dropdown Data sheet, named range manager, and full Budget-Planning sheet structure with formulas, conditional formatting, and unallocated calculations.
- Ensure tests cover sheet builders, formula helpers, and named ranges.
- Exit criteria: Planning sheet totals balance, named ranges resolve inside Excel, and regression tests flag any drift.

### Phase 3 – Advanced Features (Weeks 5–6; PRD Sections 3.1–3.6)
- Deliver Calculations sheet metrics, dashboard selectors, KPI tiles, charts, and tracking integrations.
- Harden formula utilities and performance for cross-sheet references.
- Exit criteria: Dashboard updates respond to DashYear/DashPeriod changes without Excel warnings; charts render cleanly; integration tests pass.

### Phase 4 – Polish & Testing (Weeks 7–8; PRD Sections 4.1–4.4)
- Achieve comprehensive test coverage (≥80 percent), finalize documentation, and execute dry-run release workflow.
- Address accessibility, formatting polish, and packaging validation as outlined.
- Exit criteria: Test suite green with coverage target met; documentation ready for public consumption; release checklist complete.

## Quality Gates
- Continuous testing: `uv run pytest --cov=budget_generator --cov-report=term` for every merge candidate.
- Workbook regression: compare generated files to golden artifacts for values, formulas, formatting, sheet visibility, and named ranges.
- Static analysis: enforce black, ruff, and mypy per PRD dependency list; block merges on lint/type errors.
- Manual validation: open generated workbooks in latest Microsoft 365 and one LibreOffice release prior to final sign-off.

## Operating Cadence
- Daily 15-minute stand-up (status, blockers, next focus) with updates mapped to PRD task IDs.
- Weekly phase review to confirm exit criteria readiness and reprioritize any at-risk P0/P1 items.
- Async updates in project channel for merges, test failures, and stakeholder announcements.

## Risk Watchlist
- Chart rendering support in openpyxl: prototype early; keep fallback visualization plan ready.
- Complex SUMPRODUCT/CHOOSE formulas: cover with focused unit tests and integration fixtures.
- Hidden sheet visibility and named range drift: include assertions in integration tests and workbook comparisons.
- Schedule compression in Phase 3: advance dependency work from earlier phases where possible to protect buffer.

## Definition of Done
- All PRD tasks reach Complete status with documented verification evidence.
- Automated and manual quality gates pass; coverage stays above 80 percent.
- Documentation, release notes, and packaging artifacts are published and reviewed.
- Outstanding issues triaged with clear owners for post-launch follow-up.
