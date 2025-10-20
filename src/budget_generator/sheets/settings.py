"""Builder for the Settings worksheet."""

from __future__ import annotations

from typing import Any, Mapping

from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

from ..utils.named_ranges import NamedRangeManager, NamedRangeSpec


def build_settings_sheet(worksheet: Worksheet, spec: Mapping[str, Any]) -> None:
    """Populate the Settings worksheet according to the design baseline."""

    general_settings = spec.get("general", {})
    late_income_settings = spec.get("late_income", {})

    hero_title = general_settings.get(
        "hero_title", general_settings.get("title", "Budget Planning")
    )
    general_label = general_settings.get("section_label", "General")
    starting_year_label = general_settings.get("starting_year_label", "Starting Year:")
    starting_year = general_settings.get("starting_year", 2025)
    starting_year_help = general_settings.get(
        "starting_year_help",
        "Set The starting year (yyyy) once at the beginning and do not change it again.",
    )
    tracking_section_title = general_settings.get(
        "tracking_section_title", "Budget Tracking & Dashboard"
    )

    late_income_section = late_income_settings.get(
        "section_title", "Late Monthly Income"
    )
    late_income_status_label = late_income_settings.get(
        "status_label", "Shift late Income:"
    )
    late_income_enabled = bool(late_income_settings.get("enabled_default", False))
    late_income_status_display = (
        late_income_settings.get("status_active_text", "Active")
        if late_income_enabled
        else late_income_settings.get("status_inactive_text", "Inactive")
    )
    late_income_help = late_income_settings.get(
        "status_help",
        "Set The starting year (yyyy) once at the beginning and do not change it again.",
    )
    late_income_day_label = late_income_settings.get(
        "day_label", "Starting in day x in month:"
    )
    late_income_day = late_income_settings.get("day_default", 25)

    worksheet["C1"].value = hero_title
    worksheet["C1"].font = Font(bold=True, size=16)

    worksheet["C6"].value = general_label
    worksheet["C6"].font = Font(bold=True)

    worksheet["D8"].value = starting_year_label
    worksheet["D8"].font = Font(bold=True)
    worksheet["E8"].value = starting_year
    worksheet["E8"].number_format = "0"
    worksheet["G8"].value = starting_year_help
    worksheet["G8"].alignment = Alignment(wrap_text=True)

    worksheet["C12"].value = tracking_section_title
    worksheet["C12"].font = Font(bold=True)

    worksheet["D14"].value = late_income_section
    worksheet["D14"].font = Font(bold=True)
    worksheet["D16"].value = late_income_status_label
    worksheet["D16"].font = Font(bold=True)
    worksheet["E16"].value = late_income_status_display
    worksheet["G16"].value = late_income_help
    worksheet["G16"].alignment = Alignment(wrap_text=True)
    worksheet["D18"].value = late_income_day_label
    worksheet["D18"].font = Font(bold=True)
    worksheet["E18"].value = late_income_day
    worksheet["E18"].number_format = "0"
    worksheet["E19"].value = " "

    # Hidden boolean cell used for formulas via named range.
    worksheet["J16"].value = late_income_enabled
    worksheet.column_dimensions["J"].hidden = True


def register_settings_named_ranges(manager: NamedRangeManager) -> None:
    """Register named ranges originating from the Settings sheet."""

    specs = (
        NamedRangeSpec("StartingYear", "Settings", "$E$8"),
        NamedRangeSpec("LateIncomeEnabled", "Settings", "$J$16"),
        NamedRangeSpec("LateIncomeDay", "Settings", "$E$18"),
    )
    manager.register_many(specs)
