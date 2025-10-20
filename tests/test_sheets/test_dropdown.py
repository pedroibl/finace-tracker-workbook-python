from __future__ import annotations

from openpyxl import Workbook

from budget_generator.sheets.dropdown import build_dropdown_sheet


def test_dropdown_sheet_builds_years_and_months() -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Dropdown Data"

    build_dropdown_sheet(worksheet)

    header_years = worksheet["B2"]
    header_months = worksheet["C2"]

    assert header_years.value == "Years"
    assert header_years.font.bold is True
    assert header_years.fill.start_color.rgb[-6:] == "D9D2E9"
    assert header_months.value == "Months"
    assert header_months.font.bold is True

    expected_year_formulas = ["=StartingYear+0", "=StartingYear+1", "=StartingYear+2", "=StartingYear+3", "=StartingYear+4"]
    actual_year_formulas = [worksheet[f"B{row}"].value for row in range(3, 8)]
    assert actual_year_formulas == expected_year_formulas

    expected_months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    actual_months = [worksheet[f"C{row}"].value for row in range(3, 15)]
    assert actual_months == expected_months


def test_dropdown_sheet_respects_custom_year_count() -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Dropdown Data"

    build_dropdown_sheet(worksheet, {"years": {"count": 3, "start_row": 5}})

    actual_year_formulas = [worksheet[f"B{row}"].value for row in range(5, 8)]
    assert actual_year_formulas == ["=StartingYear+0", "=StartingYear+1", "=StartingYear+2"]
    # Ensure cells before configured start row remain empty
    assert worksheet["B3"].value is None
