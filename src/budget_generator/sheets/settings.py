"""Builder for the Settings worksheet."""

from __future__ import annotations

from typing import Any, Mapping

from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.worksheet.worksheet import Worksheet

from ..formatting.styles import apply_fill, merge_and_format
from ..formatting.validation import add_list_validation, add_number_validation
from ..utils.named_ranges import NamedRangeManager, NamedRangeSpec


HEADER_RANGE = "B2:E2"


def build_settings_sheet(worksheet: Worksheet, spec: Mapping[str, Any]) -> None:
    """Populate the Settings worksheet according to the PRD contract."""

    general_settings = spec.get("general", {})
    late_income_settings = spec.get("late_income", {})

    header_title = general_settings.get("title", "General Settings")
    starting_year = general_settings.get("starting_year", 2025)
    starting_year_help = general_settings.get(
        "starting_year_help", "\u2190 Change this to your budget base year"
    )

    late_income_enabled = late_income_settings.get("enabled_default", False)
    late_income_day = late_income_settings.get("day_default", 25)

    # --- Header block ---
    merge_and_format(
        worksheet,
        HEADER_RANGE,
        value=header_title,
        font=Font(bold=True),
        alignment=Alignment(horizontal="center"),
        fill_color="D9EAD3",
    )
    header_border = Border(bottom=Side(style="thin", color="006600"))
    for cell in worksheet[HEADER_RANGE][0]:
        cell.border = header_border

    # --- Starting year controls ---
    worksheet["B4"].value = "Starting Year"
    worksheet["C4"].value = starting_year
    worksheet["D4"].value = starting_year_help

    # --- Late income toggles ---
    worksheet["B6"].value = "Late Monthly Income Enabled"
    worksheet["C6"].value = "TRUE" if late_income_enabled else "FALSE"
    worksheet["B7"].value = "Late Income Day"
    worksheet["C7"].value = late_income_day
    worksheet["D6"].value = "Toggle support for paycheques that arrive after month end"
    worksheet["D7"].value = "Day of month to post late income"

    add_list_validation(worksheet, "C6", ["TRUE", "FALSE"])
    add_number_validation(worksheet, "C7", 1, 31)

    # Apply subtle fills so the interactive cells stand out without clashing.
    apply_fill(worksheet["B6"], "FFFFFF")
    apply_fill(worksheet["C6"], "FFFFFF")
    apply_fill(worksheet["C7"], "FFFFFF")


def register_settings_named_ranges(manager: NamedRangeManager) -> None:
    """Register named ranges originating from the Settings sheet."""

    specs = (
        NamedRangeSpec("StartingYear", "Settings", "$C$4"),
        NamedRangeSpec("LateIncomeEnabled", "Settings", "$C$6"),
        NamedRangeSpec("LateIncomeDay", "Settings", "$C$7"),
    )
    manager.register_many(specs)
