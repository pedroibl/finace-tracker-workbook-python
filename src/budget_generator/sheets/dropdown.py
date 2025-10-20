"""Builder for the supporting dropdown data sheet."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

from ..formatting.styles import apply_fill
from ..formulas import build_year_formula
from ..utils.named_ranges import NamedRangeManager, NamedRangeSpec


HEADER_FILL = "D9D2E9"
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


def build_dropdown_sheet(worksheet: Worksheet, spec: Mapping[str, Any] | None = None) -> None:
    """Populate the dropdown data worksheet with years and month names."""

    spec = spec or {}
    years_config = spec.get("years", {}) if isinstance(spec, Mapping) else {}
    year_count = int(years_config.get("count", 5))
    start_row = int(years_config.get("start_row", 3))

    _add_headers(worksheet)
    _populate_years(worksheet, start_row=start_row, count=year_count)
    _populate_months(worksheet, start_row=start_row)


def _add_headers(worksheet: Worksheet) -> None:
    headers = {
        "B2": "Years",
        "C2": "Months",
    }
    for cell_ref, text in headers.items():
        cell = worksheet[cell_ref]
        cell.value = text
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
        apply_fill(cell, HEADER_FILL)


def _populate_years(worksheet: Worksheet, *, start_row: int, count: int) -> None:
    for offset in range(count):
        row = start_row + offset
        worksheet[f"B{row}"].value = build_year_formula(offset)


def _populate_months(worksheet: Worksheet, *, start_row: int) -> None:
    for index, month in enumerate(_month_list(), start=start_row):
        worksheet[f"C{index}"].value = month


def _month_list() -> Iterable[str]:
    return MONTHS


def register_dropdown_named_ranges(manager: NamedRangeManager) -> None:
    """Register named ranges used for dropdown list sources."""

    specs = (
        NamedRangeSpec("YearsList", "Dropdown Data", "$B$3:$B$7"),
        NamedRangeSpec("MonthsList", "Dropdown Data", "$C$3:$C$14"),
    )
    manager.register_many(specs)
