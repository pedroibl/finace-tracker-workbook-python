from __future__ import annotations

from pathlib import Path

import pytest

from budget_generator.generator import BudgetGenerator, GeneratorError, WorkbookNotInitialisedError


def minimal_spec() -> dict:
    return {
        "meta": {},
        "workbook": {
            "sheets": [
                {"name": "Settings", "visibility": "visible"},
                {"name": "Dropdown Data", "visibility": "hidden"},
                {"name": "Budget-Planning", "visibility": "visible"},
                {"name": "Budget Tracking", "visibility": "visible"},
                {"name": "Calculations", "visibility": "hidden"},
                {"name": "Budget Dashboard", "visibility": "visible"},
            ]
        },
        "sheets": {},
    }


def test_create_workbook_removes_default_sheet() -> None:
    gen = BudgetGenerator(minimal_spec())
    workbook = gen.create_workbook()
    assert workbook.sheetnames == []


def test_create_sheets_follows_visibility() -> None:
    gen = BudgetGenerator(minimal_spec())
    gen.create_workbook()
    gen.create_sheets()
    assert gen.workbook is not None
    assert gen.workbook.sheetnames == [
        "Settings",
        "Dropdown Data",
        "Budget-Planning",
        "Budget Tracking",
        "Calculations",
        "Budget Dashboard",
    ]
    assert gen.workbook["Dropdown Data"].sheet_state == "hidden"
    assert gen.workbook["Calculations"].sheet_state == "hidden"


def test_create_sheets_requires_workbook() -> None:
    gen = BudgetGenerator(minimal_spec())
    with pytest.raises(WorkbookNotInitialisedError):
        gen.create_sheets()


def test_create_sheets_requires_name() -> None:
    broken = minimal_spec()
    broken["workbook"]["sheets"].append({})
    gen = BudgetGenerator(broken)
    gen.create_workbook()
    with pytest.raises(GeneratorError):
        gen.create_sheets()


def test_save_workbook(tmp_path: Path) -> None:
    gen = BudgetGenerator(minimal_spec())
    gen.create_workbook()
    gen.create_sheets()
    output = tmp_path / "workbook.xlsx"
    saved_path = gen.save_workbook(output)
    assert saved_path.exists()


def test_build_sheet_contents_populates_calculations_sheet() -> None:
    gen = BudgetGenerator(minimal_spec())
    gen.create_workbook()
    gen.create_sheets()
    gen.build_sheet_contents()

    assert gen.workbook is not None
    calc_ws = gen.workbook["Calculations"]
    assert calc_ws["B2"].value == "Metric"
    assert calc_ws["F3"].value == "=CHOOSE(MonthIdx,D13,E13,F13,G13,H13,I13,J13,K13,L13,M13,N13,O13)"

    month_idx_ref = gen.workbook.defined_names["MonthIdx"].attr_text
    assert month_idx_ref in {"Calculations!$K$1", "'Calculations'!$K$1"}
    assert gen.workbook.defined_names["StartingYear"].attr_text == "Settings!$E$8"
    assert gen.workbook.defined_names["YearsList"].attr_text == "'Dropdown Data'!$B$3:$B$7"

    dashboard_ws = gen.workbook["Budget Dashboard"]
    assert dashboard_ws["B3"].value == "Year"
    dash_year_ref = gen.workbook.defined_names["DashYear"].attr_text
    dash_period_ref = gen.workbook.defined_names["DashPeriod"].attr_text
    assert dash_year_ref in {"'Budget Dashboard'!$C$3", "Budget Dashboard!$C$3"}
    assert dash_period_ref in {"'Budget Dashboard'!$C$4", "Budget Dashboard!$C$4"}
    charts = dashboard_ws._charts  # type: ignore[attr-defined]
    assert len(charts) == 3

    assert gen.workbook["Dropdown Data"].sheet_state == "hidden"
    assert gen.workbook["Calculations"].sheet_state == "hidden"
