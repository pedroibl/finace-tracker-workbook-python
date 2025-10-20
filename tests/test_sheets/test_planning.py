from __future__ import annotations

from openpyxl import Workbook

from budget_generator.sheets.planning import build_planning_sheet


def test_planning_banner_and_headers() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget Planning"

    build_planning_sheet(ws, {})

    assert ws["B2"].value == '="Budget Plan for Year "&StartingYear'
    assert ws["B2"].fill.start_color.rgb[-6:] == "CFE2F3"
    month_headers = [ws.cell(row=6, column=col).value for col in range(4, 16)]
    assert month_headers == [
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


def test_planning_sections_and_totals() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget Planning"

    build_planning_sheet(ws, {})

    assert ws["B7"].value == "Income"
    assert ws["B7"].fill.start_color.rgb[-6:] == "43D40F"
    assert ws["C8"].value == "Salary"
    assert ws["B13"].value == "Total Income"
    assert ws["D13"].value == "=SUM(D8:D12)"

    assert ws["B15"].value == "Expenses"
    assert ws["B15"].fill.start_color.rgb[-6:] == "F01010"
    assert ws["C16"].value == "Housing"
    assert ws["B26"].value == "Total Expenses"

    assert ws["B28"].value == "Savings"
    assert ws["B28"].fill.start_color.rgb[-6:] == "1564ED"
    assert ws["C29"].value == "Emergency Fund"
    assert ws["B34"].value == "Total Savings"

    # Cells start with zeros and number format configured
    for column in range(4, 16):
        assert ws.cell(row=8, column=column).value == 0
        assert ws.cell(row=8, column=column).number_format.startswith("_($*")


def test_unallocated_row_formulas_and_conditional_formatting() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget Planning"

    build_planning_sheet(ws, {})

    for column in range(4, 16):
        col_letter = ws.cell(row=36, column=column).column_letter
        assert ws.cell(row=36, column=column).value == (
            f"={col_letter}13-{col_letter}26-{col_letter}34"
        )

    cf_rules = []
    for cf in ws.conditional_formatting:
        cf_rules.extend(cf.rules)

    assert any(rule.type == "cellIs" and rule.operator == "equal" for rule in cf_rules)
    assert any(rule.type == "cellIs" and rule.operator == "lessThan" for rule in cf_rules)
    assert any(rule.type == "expression" for rule in cf_rules)


def test_year_two_scaffold_present() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget Planning"

    build_planning_sheet(ws, {})

    assert ws["Q2"].value == '="Budget Plan for Year "&(StartingYear+1)'
    second_year_headers = [ws.cell(row=6, column=col).value for col in range(17, 29)]
    assert second_year_headers == [
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
    assert ws["Q4"].value == "Year 2 scaffold – extend sections as needed"


def test_scaffold_years_config_creates_additional_headers() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget Planning"

    build_planning_sheet(ws, {"scaffold_years": 3})

    # Year 3 banner should reference StartingYear+2 and begin at column AF (index 32)
    assert ws["AF2"].value == '="Budget Plan for Year "&(StartingYear+2)'
    headers_year3 = [ws.cell(row=6, column=col).value for col in range(32, 44)]
    assert headers_year3 == [
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
