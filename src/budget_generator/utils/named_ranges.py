"""Named range utilities for workbook generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from openpyxl import Workbook
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils.cell import absolute_coordinate


class NamedRangeError(RuntimeError):
    """Base exception for named range management."""


class DuplicateNamedRangeError(NamedRangeError):
    """Raised when attempting to register a duplicate named range."""


def _normalise_formula(sheet_name: str, cell_range: str) -> str:
    sheet_ref = f"'{sheet_name}'" if " " in sheet_name else sheet_name
    return f"{sheet_ref}!{_ensure_absolute(cell_range)}"


def _ensure_absolute(cell_range: str) -> str:
    if ":" in cell_range:
        start, end = cell_range.split(":", 1)
        return f"{absolute_coordinate(start)}:{absolute_coordinate(end)}"
    return absolute_coordinate(cell_range)


@dataclass
class NamedRangeSpec:
    name: str
    sheet: str
    ref: str


class NamedRangeManager:
    """Manage workbook-level named ranges."""

    def __init__(self, workbook: Workbook):
        self.workbook = workbook

    def create_range(
        self,
        name: str,
        sheet_name: str,
        cell_range: str,
        *,
        scope: str = "workbook",
    ) -> None:
        if name in self.workbook.defined_names:
            raise DuplicateNamedRangeError(f"Named range '{name}' already exists")

        formula = _normalise_formula(sheet_name, cell_range)
        defined_name = DefinedName(name, attr_text=formula)
        if scope != "workbook":
            defined_name.localSheetId = self._resolve_sheet_index(scope)
        self.workbook.defined_names.add(defined_name)

    def register_many(self, specs: Iterable[NamedRangeSpec]) -> None:
        for spec in specs:
            self.create_range(spec.name, spec.sheet, spec.ref)

    def _resolve_sheet_index(self, scope: str) -> int:
        if scope.isdigit():
            return int(scope)
        try:
            return list(self.workbook.sheetnames).index(scope)
        except ValueError as exc:  # pragma: no cover - defensive guard
            raise NamedRangeError(f"Unknown sheet '{scope}' for named range scope") from exc
