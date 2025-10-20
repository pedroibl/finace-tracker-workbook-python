"""Budget Planning worksheet builder and helpers."""

from __future__ import annotations

from typing import Mapping

from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from ..formatting.conditional import add_unallocated_conditional_formatting
from ..formatting.styles import merge_and_format
from ..utils.named_ranges import NamedRangeManager, NamedRangeSpec


MONTHS: tuple[str, ...] = (
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
)


ACCOUNTING_FORMAT = '_($* #,##0_);_($* (#,##0);_($* "-"??_);_(@_)'


class PlanningSheetBuilder:
    """Internal helper that encapsulates worksheet layout and styling."""

    SECTION_DEFINITIONS = (
        {
            "title": "Income",
            "title_cell": "B7",
            "title_fill": "43D40F",
            "categories": ["Salary", "Freelance", "Investments", "Other", ""],
            "start_row": 8,
        },
        {
            "title": "Expenses",
            "title_cell": "B15",
            "title_fill": "F01010",
            "categories": [
                "Housing",
                "Utilities",
                "Groceries",
                "Transportation",
                "Insurance",
                "Healthcare",
                "Debt Repayments",
                "Entertainment",
                "Subscriptions",
                "Miscellaneous",
            ],
            "start_row": 16,
        },
        {
            "title": "Savings",
            "title_cell": "B28",
            "title_fill": "1564ED",
            "categories": [
                "Emergency Fund",
                "Retirement",
                "Investments",
                "Vacation",
                "Other",
            ],
            "start_row": 29,
        },
    )

    def __init__(self, worksheet: Worksheet, spec: Mapping[str, object]):
        self.ws = worksheet
        self.spec = spec

    def build(self) -> None:
        self._build_year_one_banner()
        self._build_year_one_month_headers()
        self._build_sections()
        self._build_unallocated_row()
        self._apply_conditional_formatting()
        self._build_additional_year_scaffolds()
        self.ws.freeze_panes = "C7"

    def _build_year_one_banner(self) -> None:
        merge_and_format(
            self.ws,
            "B2:N2",
            value='="Budget Plan for Year "&StartingYear',
            font=Font(bold=True, size=14),
            alignment=Alignment(horizontal="center"),
            fill_color="CFE2F3",
        )

    def _build_year_one_month_headers(self) -> None:
        header_fill = PatternFill(start_color="DAE3F3", end_color="DAE3F3", fill_type="solid")
        header_font = Font(bold=True)
        header_alignment = Alignment(horizontal="center")
        for index, month in enumerate(MONTHS, start=4):
            cell = self.ws.cell(row=6, column=index, value=month)
            cell.font = header_font
            cell.alignment = header_alignment
            cell.fill = header_fill

    def _build_sections(self) -> None:
        for section in self.SECTION_DEFINITIONS:
            self._render_section(section)

    def _render_section(self, section: Mapping[str, object]) -> None:
        title_cell = self.ws[section["title_cell"]]
        title_cell.value = section["title"]
        title_cell.font = Font(bold=True)
        title_cell.fill = PatternFill(  # type: ignore[arg-type]
            start_color=section["title_fill"],
            end_color=section["title_fill"],
            fill_type="solid",
        )

        start_row = int(section["start_row"])
        categories = list(section["categories"])
        for offset, category in enumerate(categories, start=0):
            row = start_row + offset
            self.ws[f"C{row}"].value = category
            for column in range(4, 16):
                cell = self.ws.cell(row=row, column=column, value=0)
                cell.number_format = ACCOUNTING_FORMAT

        total_row = start_row + len(categories)
        self.ws[f"B{total_row}"] = f"Total {section['title']}"
        total_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
        for column in range(4, 16):
            cell = self.ws.cell(row=total_row, column=column)
            column_letter = cell.column_letter
            start_cell = f"{column_letter}{start_row}"
            end_cell = f"{column_letter}{total_row - 1}"
            cell.value = f"=SUM({start_cell}:{end_cell})"
            cell.fill = total_fill
            cell.font = Font(bold=True)
            cell.number_format = ACCOUNTING_FORMAT

        self._apply_section_borders(start_row, total_row)

    def _apply_section_borders(self, start_row: int, total_row: int) -> None:
        border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )
        for row in range(start_row - 1, total_row + 1):
            for column in range(2, 16):
                self.ws.cell(row=row, column=column).border = border

    def _build_unallocated_row(self) -> None:
        row = 36
        self.ws[f"B{row}"] = "Unallocated (per month)"
        for column in range(4, 16):
            column_letter = self.ws.cell(row=row, column=column).column_letter
            income_ref = f"{column_letter}13"
            expenses_ref = f"{column_letter}26"
            savings_ref = f"{column_letter}34"
            cell = self.ws.cell(row=row, column=column)
            cell.value = f"={income_ref}-{expenses_ref}-{savings_ref}"
            cell.number_format = ACCOUNTING_FORMAT

    def _apply_conditional_formatting(self) -> None:
        add_unallocated_conditional_formatting(self.ws, "D", "O", 36)

    def _build_additional_year_scaffolds(self) -> None:
        scaffold_years = max(1, int(self.spec.get("scaffold_years", 2)))
        for year_index in range(2, scaffold_years + 1):
            self._render_scaffold(year_index)

    def _render_scaffold(self, year_index: int) -> None:
        # Each scaffold occupies 13 columns with a two-column spacer (total stride 15).
        start_col_idx = 17 + (year_index - 2) * 15
        end_col_idx = start_col_idx + 12
        start_letter = get_column_letter(start_col_idx)
        end_letter = get_column_letter(end_col_idx)

        merge_and_format(
            self.ws,
            f"{start_letter}2:{end_letter}2",
            value=f'="Budget Plan for Year "&(StartingYear+{year_index - 1})',
            font=Font(bold=True, size=14),
            alignment=Alignment(horizontal="center"),
            fill_color="CFE2F3",
        )

        header_fill = PatternFill(start_color="DAE3F3", end_color="DAE3F3", fill_type="solid")
        header_font = Font(bold=True)
        header_alignment = Alignment(horizontal="center")
        for offset, month in enumerate(MONTHS):
            column_index = start_col_idx + offset
            cell = self.ws.cell(row=6, column=column_index, value=month)
            cell.font = header_font
            cell.alignment = header_alignment
            cell.fill = header_fill

        note_cell = f"{start_letter}4"
        self.ws[note_cell] = f"Year {year_index} scaffold – extend sections as needed"


def build_planning_sheet(worksheet: Worksheet, spec: Mapping[str, object] | None = None) -> None:
    builder = PlanningSheetBuilder(worksheet, spec or {})
    builder.build()


def register_planning_named_ranges(manager: NamedRangeManager) -> None:
    """Register named ranges for the Budget Planning sheet."""

    specs = [
        NamedRangeSpec("IncomeCats", "Budget Planning", "$C$8:$C$12"),
        NamedRangeSpec("ExpenseCats", "Budget Planning", "$C$16:$C$25"),
        NamedRangeSpec("SavingsCats", "Budget Planning", "$C$29:$C$33"),
        NamedRangeSpec("IncomeGrid", "Budget Planning", "$D$8:$O$12"),
        NamedRangeSpec("ExpenseGrid", "Budget Planning", "$D$16:$O$25"),
        NamedRangeSpec("SavingsGrid", "Budget Planning", "$D$29:$O$33"),
        NamedRangeSpec("IncomeHeader", "Budget Planning", "$B$7"),
        NamedRangeSpec("ExpenseHeader", "Budget Planning", "$B$15"),
        NamedRangeSpec("SavingsHeader", "Budget Planning", "$B$28"),
        NamedRangeSpec("IncomeTotals", "Budget Planning", "$D$13:$O$13"),
        NamedRangeSpec("ExpenseTotals", "Budget Planning", "$D$26:$O$26"),
        NamedRangeSpec("SavingsTotals", "Budget Planning", "$D$34:$O$34"),
        NamedRangeSpec("UnallocatedRow", "Budget Planning", "$D$36:$O$36"),
    ]

    manager.register_many(specs)
