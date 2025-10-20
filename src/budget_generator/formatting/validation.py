"""Data validation helpers to keep sheet builders succinct."""

from __future__ import annotations

from typing import Iterable

from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.worksheet import Worksheet


def add_list_validation(worksheet: Worksheet, cell_range: str, options: Iterable[str]) -> DataValidation:
    """Attach a dropdown list validation to *cell_range* using *options*."""

    option_text = ",".join(options)
    validation = DataValidation(type="list", formula1=f'"{option_text}"', allow_blank=False)
    worksheet.add_data_validation(validation)
    validation.add(cell_range)
    return validation


def add_number_validation(
    worksheet: Worksheet, cell_range: str, minimum: int, maximum: int
) -> DataValidation:
    """Restrict *cell_range* to a whole number between *minimum* and *maximum*."""

    validation = DataValidation(
        type="whole",
        operator="between",
        formula1=str(minimum),
        formula2=str(maximum),
        allow_blank=False,
    )
    worksheet.add_data_validation(validation)
    validation.add(cell_range)
    return validation
