# Tutorial Spec Mapping

This document connects the example JSON specification (`examples/tutorial_spec.json`) to the generated workbook so new contributors can understand how each section of the spec manifests inside Excel.

---

## JSON Overview

```json
{
  "meta": {...},
  "workbook": {
    "sheets": [
      {"name": "Settings", "visibility": "visible"},
      ...
    ]
  },
  "sheets": {
    "Settings": {...},
    "Dropdown Data": {...},
    "Budget Planning": {...},
    "Budget Tracking": {...},
    "Budget Dashboard": {...}
  }
}
```

- `meta`: Optional metadata recorded for audit/logging.
- `workbook.sheets`: Ordered list of sheet names plus initial visibility (`hidden`, `veryHidden`, or `visible`).
- `workbook.named_ranges`: Optional hints or manual overrides. Provide an empty object when relying on generator defaults; the builder re-registers every range during generation.
- `sheets`: Per-sheet configuration blocks consumed by sheet builders.

---

## Settings Sheet (`sheets.Settings`)

| JSON Field | Example | Excel Output |
|------------|---------|--------------|
| `general.hero_title` | `"Budget Planning"` | Cell `C1` bold hero heading |
| `general.starting_year` | `2025` | Cell `E8` value (`StartingYear` named range) |
| `general.tracking_section_title` | `"Budget Tracking & Dashboard"` | Cell `C12` section heading |
| `late_income.enabled_default` | `false` | Hidden boolean cell `J16` (display text at `E16`) |
| `late_income.day_default` | `25` | Cell `E18` value (`LateIncomeDay` named range) |

Named ranges created: `StartingYear` (`Settings!$E$8`), `LateIncomeEnabled` (`Settings!$J$16`), `LateIncomeDay` (`Settings!$E$18`).

---

## Dropdown Data (`sheets.Dropdown Data`)

| JSON Field | Example | Excel Output |
|------------|---------|--------------|
| `years.count` | `5` | Five formulas `B3:B7` referencing `StartingYear` |
| `years.start_row` | `3` | First formula written to row 3 |

Derived named ranges: `YearsList` (`B3:B7`), `MonthsList` (`C3:C14`).

---

## Budget Planning (`sheets.Budget Planning`)

| JSON Field | Example | Excel Output |
|------------|---------|--------------|
| `scaffold_years` | `2` | Year 1 detailed grid; Year 2 banner/month headers (`Q` columns) |

Sections (Income, Expenses, Savings) are standardised and always rendered. Conditional formatting and totals are generated automatically. Named ranges registered include `IncomeCats`, `IncomeGrid`, `IncomeTotals`, etc.

---

## Budget Tracking (`sheets.Budget Tracking`)

| JSON Field | Example | Excel Output |
|------------|---------|--------------|
| `intro.title` | `"Budget Tracking"` | Cell `B1` sheet title |
| `intro.duration` | `"1h 33min"` | Cell `E5` italic duration |
| `sample_entries` | `[ ... ]` | Prefilled rows starting at `C12` |
| `max_rows` | `200` | Table `tblTracking` spans columns `C:I` down to row 200 |

Validations reference named ranges from Planning (Income/Expense/Savings categories). SUMPRODUCT formulas compute balances; late income logic uses the Settings named ranges.

---

## Calculations Sheet

Hidden sheet—no direct JSON configuration (defaults used). Provides:

- Metric tiles (`Today`, `MAX Date`, `COUNTA`, `LOOKUP`).
- `MonthMap` table for Jan–Dec lookup.
- Budget-vs-Tracked table (Income, Expenses, Savings) that drives dashboard charts.
- Named ranges: `MonthMap`, `MonthIdx`.

---

## Budget Dashboard (`sheets.Budget Dashboard`)

| JSON Field | Example | Excel Output |
|------------|---------|--------------|
| `selectors.default_year_formula` | `"=StartingYear"` | Cell `C3` formula (named `DashYear`) |
| `selectors.default_period` | `"Jan"` | Cell `C4` value (named `DashPeriod`) |

Builder adds:

- Table header row (`B2:H2`) for future transactional insights.
- KPI tiles (rows `6-9`) referencing named ranges and Calculations sheet metrics.
- Doughnut charts pulling from Calculations sheet row data for Income/Expenses/Savings.

---

## Generation Flow Summary

1. **create_workbook / create_sheets** – instantiates sheets in the order defined by `workbook.sheets`.
2. **build_settings_sheet** – applies Settings config; registers named ranges.
3. **build_dropdown_sheet** – formulas for years/months; registers dropdown ranges.
4. **build_planning_sheet** – renders categories, totals, unallocated row; registers planning ranges.
5. **build_tracking_sheet** – constructs table, validations, formulas.
6. **build_calculations_sheet** – metrics, MonthMap, budget-vs-tracked table; registers Calculations ranges.
7. **build_dashboard_sheet** – selectors, KPI tiles; registers dashboard ranges.
8. **add_dashboard_doughnut_charts** – attaches charts referencing Calculations sheet.
9. Helper sheets (`Dropdown Data`, `Calculations`) set to hidden before saving.

---

## Tips for Customisation

- **Multiple Years**: adjust `Budget Planning.scaffold_years`.
- **Tracking Table Size**: set `Budget Tracking.max_rows` to desired length.
- **Dashboard Defaults**: override `Budget Dashboard.selectors` to change initial Year/Period.
- **Late Income Behavior**: toggle `late_income` in the Settings block.

Always regenerate the workbook (`uv run budget-generator generate ...`) after modifying the spec and run the integration test suite to catch regressions.
