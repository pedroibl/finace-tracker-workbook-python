# Budget Excel Generator

![Tests](https://img.shields.io/badge/tests-46%20passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-95%25-blue)

Generate a fully formatted multi-sheet Excel budget workbook from a structured JSON specification.  
The product requirements and phase checklists live in [`docs/prd-excell-budget-tracker.md`](docs/prd-excell-budget-tracker.md).

---

## Features Overview

- **Settings sheet** with starting year controls, late-income toggles, and named ranges (`StartingYear`, `LateIncomeEnabled`, `LateIncomeDay`).
- **Dropdown Data sheet** housing dynamic years/months lists that back workbook validations (`YearsList`, `MonthsList`).
- **Budget-Planning sheet** containing income/expense/savings grids, totals, conditional formatting, and multi-year scaffolding.
- **Budget Tracking sheet** with an Excel table, validations, running balance formulas, and conditional formatting.
- **Calculations sheet** (hidden) that aggregates metrics, calculates MonthIdx, and exposes budget-vs-tracked comparisons.
- **Dashboard sheet** combining selectors, KPI tiles, and doughnut charts for Income/Expenses/Savings.
- **CLI** command (`budget-generator`) that loads a JSON spec, assembles every sheet, registers named ranges, and saves the workbook.
- **Test suite** (46 tests) covering CLI behavior, sheet builders, chart creation, named ranges, formulas, and generator orchestration.

---

## Prerequisites

- Python **3.11+**
- [uv](https://docs.astral.sh/uv/) for dependency management (already assumed by the PRD)
- macOS / Linux / Windows capable of running openpyxl

To install `uv` (macOS/Linux):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows, follow the [official uv instructions](https://docs.astral.sh/uv/getting-started/installation/).

---

## Installation

Clone the repository and install dependencies:

```bash
git clone <repo-url> budget-excel-tracker
cd budget-excel-tracker

# Install runtime dependencies (+ optional dev extras via the project metadata)
uv sync --all-packages
```

> `uv sync --all-packages` installs both the core requirements (`openpyxl`, `click`) and the dev toolchain declared in `pyproject.toml`.

### Managing Dependencies with `uv add`

The project already pins the required packages, but if you need to add or upgrade:

```bash
# Runtime dependencies
uv add openpyxl click

# Development-only tooling (note the --dev flag)
uv add pytest --dev
uv add pytest-cov --dev
uv add black --dev
uv add ruff --dev
uv add mypy --dev
```

Running `uv sync` afterwards will refresh the lockfile and install anything new.

---

## Quick Start

```bash
# Show CLI usage
uv run budget-generator --help

# Validate a JSON spec without writing a workbook
uv run budget-generator generate examples/tutorial_spec.json --validate-only

# Generate a workbook
uv run budget-generator -v generate examples/tutorial_spec.json -o budget.xlsx
```

> **Tip:** Global options like `-v/--verbose` must appear before the subcommand, e.g. `uv run budget-generator -v generate …`.

Flags:

- `-o / --output` – destination Excel file (defaults to `budget_workbook.xlsx`)
- `-v / --verbose` – enables INFO/DEBUG logging during generation
- `--validate-only` – schema/structure validation without writing a file

---

## Project Structure

```
src/
  budget_generator/
    charts/            # Doughnut chart helpers
    formatting/        # Styling, validation, and conditional formatting utilities
    formulas/          # Excel formula builders
    sheets/            # Sheet builders (settings, planning, tracking, dashboard, calculations, dropdown data)
    utils/             # JSON loader, named range manager, etc.
    __main__.py        # Click CLI entry point

tests/
  test_cli.py
  test_generator.py
  test_named_ranges.py
  test_sheets/
  ...
docs/
  prd-excell-budget-tracker.md
examples/
  tutorial_spec.json (placeholder for sample specs)
```

Key entry points:

- `budget_generator.generator.BudgetGenerator` orchestrates sheet creation, named ranges, dashboard charts, and final visibility.
- `budget_generator.__main__` exposes the `budget-generator` CLI.

---

## Development Workflow

### Run Tests

```bash
uv run pytest
# If macOS sandbox restrictions interfere, fall back to:
.venv/bin/python -m pytest
```

### Coverage & Integration Suites

```bash
# Coverage (target ≥80%)
uv run pytest --cov=budget_generator --cov-report=term
# Fallback (sandbox without pytest-cov)
uv run python scripts/run_coverage.py

# Integration & golden output checks
uv run pytest -k "integration"
uv run pytest -k "output"   # compares against tests/fixtures/golden_tutorial.xlsx
```

### Lint & Format

```bash
uv run black src tests
uv run ruff check src tests
uv run mypy src
```

### Generate Sample Workbook

```bash
uv run budget-generator generate examples/tutorial_spec.json -o build/tutorial.xlsx -v
```

Open the resulting workbook in Excel (or LibreOffice) to review formatting, charts, and named ranges.

---

## JSON Specification Outline

The CLI expects a JSON document with three top-level sections:

- `meta`: optional metadata (name, author, etc.)
- `workbook.sheets`: ordered list of worksheets, their names, and whether they start hidden
- `workbook.named_ranges`: optional override for named ranges (provide an empty object if you rely on the generator defaults)
- `sheets`: per-sheet configuration (starting year defaults, planning scaffold instructions, tracking limits, dashboard options, etc.)

Examples live under `examples/`. Consult the PRD for field-by-field requirements.

---

## Sheet Highlights

### Settings
- Merged header with green styling
- Validated dropdowns for late income toggles/day
- Named ranges `StartingYear`, `LateIncomeEnabled`, `LateIncomeDay`

### Dropdown Data
- Year list formulas built from `StartingYear`
- Month list (Jan–Dec)
- Named ranges `YearsList`, `MonthsList`

### Budget-Planning
- Income/Expense/Savings sections with totals and accounting formats
- Unallocated row with conditional formatting (green/red/grey)
- Multi-year scaffolding with configurable count

### Budget Tracking
- Excel table `tblTracking`
- Validations for Date/Type/Category
- SUMPRODUCT running balance and late income adjustments
- Conditional formatting to surface `#N/A` categories and income rows

### Calculations (hidden)
- Metric tiles (Current Date, Last Record Date, Count, Tracking Balance)
- MonthMap table and MonthIdx calculation
- Budget-vs-tracked table for Income, Expenses, Savings

### Dashboard
- Year/Period selectors linked to named ranges
- KPI tiles (Selected Year/Period, Tracking Balance, Savings Rate)
- Doughnut charts for Income vs Tracked, Expenses vs Tracked, Savings vs Tracked

---

## Running the CLI in CI

Example GitHub Actions workflow fragment:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh
- name: Sync dependencies
  run: uv sync --all-packages
- name: Run tests
  run: uv run pytest
- name: Build sample workbook
  run: uv run budget-generator generate examples/tutorial_spec.json -o build/tutorial.xlsx
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `uv run pytest` fails with `Attempted to create a NULL object` (macOS) | Sandbox restrictions on `SystemConfiguration` | Use `.venv/bin/python -m pytest` instead of `uv run` |
| Charts missing in Excel | Excel version lacks doughnut chart support | Upgrade Excel (Microsoft 365 recommended) or inspect via LibreOffice |
| Dropdowns not populated | Named ranges missing | Ensure `build_sheet_contents()` ran after `create_sheets()` |
| Validation errors in JSON | Invalid spec structure | Run `uv run budget-generator generate spec.json --validate-only` and fix reported fields |

---

## Contributing

1. Fork and clone the repo.
2. Install deps (`uv sync --all-packages`).
3. Create a feature branch.
4. Write code + tests; run `uv run pytest`.
5. Format & lint (`uv run black`, `uv run ruff`).
6. Update documentation (README, PRD checkboxes, AGENTS brief).
7. Open a PR describing changes and verification steps.

---

## License

MIT – see `LICENSE` (or update to your preferred license). Contributions are welcome!
# finace-tracker-workbook-python
