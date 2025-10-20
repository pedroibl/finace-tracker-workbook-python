from __future__ import annotations

from openpyxl import Workbook

from budget_generator.sheets.settings import build_settings_sheet


def default_spec() -> dict:
    return {
        "general": {
            "title": "General Settings",
            "starting_year": 2026,
            "starting_year_help": "← Change this to your budget base year",
        },
        "late_income": {
            "enabled_default": True,
            "day_default": 5,
        },
    }


def test_settings_sheet_values_and_formatting() -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Settings"

    build_settings_sheet(worksheet, default_spec())

    merged_ranges = [rng.coord for rng in worksheet.merged_cells.ranges]
    assert "B2:E2" in merged_ranges
    header_cell = worksheet["B2"]
    assert header_cell.value == "General Settings"
    assert header_cell.font.bold is True
    assert header_cell.alignment.horizontal == "center"
    assert header_cell.fill.start_color.rgb[-6:] == "D9EAD3"
    assert header_cell.border.bottom.style == "thin"

    assert worksheet["B4"].value == "Starting Year"
    assert worksheet["C4"].value == 2026
    assert worksheet["D4"].value.startswith("←")

    assert worksheet["C6"].value == "TRUE"
    assert worksheet["C7"].value == 5

    validations = list(worksheet.data_validations.dataValidation)
    list_validation = next(v for v in validations if v.type == "list")
    assert "TRUE,FALSE" in list_validation.formula1
    number_validation = next(v for v in validations if v.type == "whole")
    assert number_validation.formula1 == "1"
    assert number_validation.formula2 == "31"
