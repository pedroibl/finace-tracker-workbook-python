from __future__ import annotations

from openpyxl import Workbook

from budget_generator.sheets.settings import build_settings_sheet


def default_spec() -> dict:
    return {
        "general": {
            "hero_title": "Budget Planning",
            "section_label": "General",
            "starting_year": 2026,
            "starting_year_help": "Set The starting year (yyyy) once at the beginning and do not change it again.",
            "tracking_section_title": "Budget Tracking & Dashboard",
        },
        "late_income": {
            "section_title": "Late Monthly Income",
            "status_label": "Shift late Income:",
            "enabled_default": True,
            "status_active_text": "Active",
            "day_label": "Starting in day x in month:",
            "day_default": 5,
        },
    }


def test_settings_sheet_values_and_formatting() -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Settings"

    build_settings_sheet(worksheet, default_spec())

    assert worksheet["C1"].value == "Budget Planning"
    assert worksheet["C1"].font.bold is True
    assert worksheet["C6"].value == "General"
    assert worksheet["D8"].value == "Starting Year:"
    assert worksheet["E8"].value == 2026
    assert "starting" in worksheet["G8"].value.lower()

    assert worksheet["C12"].value == "Budget Tracking & Dashboard"
    assert worksheet["D14"].value == "Late Monthly Income"
    assert worksheet["D16"].value == "Shift late Income:"
    assert worksheet["E16"].value == "Active"
    assert worksheet["D18"].value == "Starting in day x in month:"
    assert worksheet["E18"].value == 5

    # Hidden boolean cell backing LateIncomeEnabled named range.
    assert worksheet.column_dimensions["J"].hidden is True
    assert worksheet["J16"].value is True
