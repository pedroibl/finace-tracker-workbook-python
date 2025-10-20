from __future__ import annotations

from openpyxl import Workbook

from openpyxl import Workbook

from budget_generator.sheets.planning import build_planning_sheet


def test_planning_banner_and_headers() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget-Planning"

    build_planning_sheet(ws, {})

    assert ws["C1"].value == "Budget Planning"
    assert ws["C3"].value.startswith("Plan your")
    assert ws["E5"].value == "=StartingYear+0"
    assert ws["E6"].value == '=IF(E7=0,"Jan ✓","Jan")'
    assert ws["Q6"].value == '=IF(Q7=0,"Total ✓","Total")'


def test_planning_sections_and_totals() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget-Planning"

    build_planning_sheet(ws, {})

    assert ws["D10"].value == "Income"
    assert ws["D10"].fill.start_color.rgb[-6:] == "43D40F"
    assert ws["D12"].value == "Salary"
    assert ws["D24"].value == "Total Income"
    assert ws["E24"].value == "=SUM(E12:E23)"

    assert ws["D31"].value == "Expenses"
    assert ws["D31"].fill.start_color.rgb[-6:] == "F01010"
    assert ws["D33"].value == "Housing"
    assert ws["D45"].value == "Total Expenses"

    assert ws["D53"].value == "Savings"
    assert ws["D53"].fill.start_color.rgb[-6:] == "1564ED"
    assert ws["D55"].value == "Emergency Fund"
    assert ws["D67"].value == "Total Savings"

    for column in range(5, 17):  # Columns E through P
        assert ws.cell(row=12, column=column).value == 0
        assert ws.cell(row=12, column=column).number_format.startswith("_($*")

    total_cell = ws.cell(row=12, column=17)
    assert total_cell.value == "=SUM(E12:P12)"
    assert total_cell.number_format.startswith("_($*")


def test_unallocated_row_formulas_and_conditional_formatting() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget-Planning"

    build_planning_sheet(ws, {})

    for column in range(5, 18):
        col_letter = ws.cell(row=7, column=column).column_letter
        assert ws.cell(row=7, column=column).value == (
            f"={col_letter}24-{col_letter}45-{col_letter}67"
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
    ws.title = "Budget-Planning"

    build_planning_sheet(ws, {})

    assert ws["S5"].value == "=StartingYear+1"
    second_year_headers = [ws.cell(row=6, column=col).value for col in range(19, 32)]
    assert second_year_headers[0] == '=IF(S7=0,"Jan ✓","Jan")'
    assert ws["S8"].value == "Year 2 scaffold – extend rows as needed"


def test_scaffold_years_config_creates_additional_headers() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget-Planning"

    build_planning_sheet(ws, {"scaffold_years": 3})

    # Year 3 banner should reference StartingYear+2 and begin at column AG (index 33)
    assert ws["AG5"].value == "=StartingYear+2"
    headers_year3 = [ws.cell(row=6, column=col).value for col in range(33, 46)]
    assert headers_year3[0] == '=IF(AG7=0,"Jan ✓","Jan")'
