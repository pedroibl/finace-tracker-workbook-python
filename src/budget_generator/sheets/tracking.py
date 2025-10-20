"""Budget Tracking worksheet builder with validations and formulas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.worksheet import Worksheet


HEADERS: tuple[str, ...] = (
    "Date",
    "Type",
    "Category",
    "Amount",
    "Details",
    "Balance",
    "Effective Date",
)

ACCOUNTING_FORMAT = '_($* #,##0_);_($* (#,##0);_($* "-"??_);_(@_)'
DATE_FORMAT = "yyyy-mm-dd"


@dataclass
class TrackingConfig:
    """Configuration for building the tracking sheet."""

    max_rows: int = 200
    table_name: str = "tblTracking"
    header_row: int = 2
    start_column: int = 2  # column B

    @property
    def data_start_row(self) -> int:
        return self.header_row + 1

    @property
    def end_row(self) -> int:
        return self.max_rows

    @property
    def end_column(self) -> int:
        return self.start_column + len(HEADERS) - 1

    @property
    def table_ref(self) -> str:
        start_letter = get_column_letter(self.start_column)
        end_letter = get_column_letter(self.end_column)
        return f"{start_letter}{self.header_row}:{end_letter}{self.end_row}"


def build_tracking_sheet(worksheet: Worksheet, spec: Mapping[str, object] | None = None) -> None:
    """Build the Budget Tracking sheet end-to-end."""

    config = _resolve_config(spec)
    _render_headers(worksheet, config)
    _set_column_widths(worksheet)
    _create_table(worksheet, config)
    _apply_number_formats(worksheet, config)
    add_tracking_validations(worksheet, config)
    add_tracking_formulas(worksheet, config)
    add_tracking_conditional_formatting(worksheet, config)


def add_tracking_validations(worksheet: Worksheet, config: TrackingConfig | None = None) -> None:
    """Attach date/type/category validations required by the PRD."""

    cfg = config or TrackingConfig()

    date_validation = DataValidation(
        type="date",
        operator="between",
        formula1="DATE(2000,1,1)",
        formula2="DATE(2100,12,31)",
        allow_blank=True,
    )
    worksheet.add_data_validation(date_validation)
    date_validation.add(f"B{cfg.data_start_row}:B{cfg.end_row}")

    type_validation = DataValidation(
        type="list",
        formula1='"Income,Expense,Saving"',
        allow_blank=False,
    )
    worksheet.add_data_validation(type_validation)
    type_validation.add(f"C{cfg.data_start_row}:C{cfg.end_row}")

    for row in range(cfg.data_start_row, cfg.end_row + 1):
        formula = (
            f'=IF($C{row}="Income",IncomeCats,'
            f'IF($C{row}="Expense",ExpenseCats,SavingsCats))'
        )
        category_validation = DataValidation(type="list", formula1=formula, allow_blank=True)
        worksheet.add_data_validation(category_validation)
        category_validation.add(f"D{row}")


def add_tracking_formulas(worksheet: Worksheet, config: TrackingConfig | None = None) -> None:
    """Populate balance and effective-date formulas."""

    cfg = config or TrackingConfig()
    for row in range(cfg.data_start_row, cfg.end_row + 1):
        balance_cell = worksheet.cell(row=row, column=cfg.start_column + 5)
        balance_cell.value = (
            "=SUMPRODUCT((tblTracking[Date]<=[@Date])*(tblTracking[Type]=\"Income\")*"
            "tblTracking[Amount])"
            "-SUMPRODUCT((tblTracking[Date]<=[@Date])*((tblTracking[Type]=\"Expense\")+"
            "(tblTracking[Type]=\"Saving\"))*tblTracking[Amount])"
        )
        balance_cell.number_format = ACCOUNTING_FORMAT

        effective_cell = worksheet.cell(row=row, column=cfg.start_column + 6)
        effective_cell.value = (
            "=IF(AND(LateIncomeEnabled,[@Type]=\"Income\",DAY([@Date])>LateIncomeDay),"
            "DATE(YEAR([@Date]),MONTH([@Date])+1,1),[@Date])"
        )
        effective_cell.number_format = DATE_FORMAT


def add_tracking_conditional_formatting(
    worksheet: Worksheet, config: TrackingConfig | None = None
) -> None:
    """Apply conditional formatting rules called out in the PRD."""

    cfg = config or TrackingConfig()
    start_row = cfg.data_start_row
    end_row = cfg.end_row

    from openpyxl.formatting.rule import FormulaRule

    cat_range = f"D{start_row}:D{end_row}"
    worksheet.conditional_formatting.add(
        cat_range,
        FormulaRule(
            formula=[f"ISNA(D{start_row})"],
            fill=PatternFill(start_color="FCE5CD", end_color="FCE5CD", fill_type="solid"),
        ),
    )

    amt_range = f"D{start_row}:D{end_row}"
    worksheet.conditional_formatting.add(
        amt_range,
        FormulaRule(
            formula=[f"$C{start_row}=\"Income\""],
            fill=PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid"),
        ),
    )


def _resolve_config(spec: Mapping[str, object] | None) -> TrackingConfig:
    spec = spec or {}
    max_rows = int(spec.get("max_rows", 200))
    return TrackingConfig(max_rows=max_rows)


def _render_headers(worksheet: Worksheet, config: TrackingConfig) -> None:
    header_fill = PatternFill(start_color="CFE2F3", end_color="CFE2F3", fill_type="solid")
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal="center")

    for offset, header in enumerate(HEADERS):
        column = config.start_column + offset
        cell = worksheet.cell(row=config.header_row, column=column, value=header)
        cell.font = header_font
        cell.alignment = header_alignment
        cell.fill = header_fill


def _set_column_widths(worksheet: Worksheet) -> None:
    widths = {
        "B": 14,
        "C": 12,
        "D": 24,
        "E": 12,
        "F": 30,
        "G": 16,
        "H": 16,
    }
    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width


def _create_table(worksheet: Worksheet, config: TrackingConfig) -> None:
    table = Table(displayName=config.table_name, ref=config.table_ref)
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    worksheet.add_table(table)


def _apply_number_formats(worksheet: Worksheet, config: TrackingConfig) -> None:
    for row in range(config.data_start_row, config.end_row + 1):
        date_cell = worksheet.cell(row=row, column=config.start_column)
        date_cell.number_format = DATE_FORMAT

        amount_cell = worksheet.cell(row=row, column=config.start_column + 2)
        amount_cell.number_format = ACCOUNTING_FORMAT

        details_cell = worksheet.cell(row=row, column=config.start_column + 3)
        details_cell.number_format = "@"
