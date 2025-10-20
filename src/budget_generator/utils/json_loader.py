"""Helpers for loading and validating the budget generator JSON spec."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping


REQUIRED_TOP_LEVEL_KEYS = {"meta", "workbook", "sheets"}
REQUIRED_SHEET_NAMES = {
    "Settings",
    "Dropdown Data",
    "Budget Planning",
    "Budget Tracking",
    "Calculations",
    "Budget Dashboard",
}


class JSONLoaderError(RuntimeError):
    """Base exception for JSON loading failures."""


class SpecValidationError(JSONLoaderError):
    """Raised when a specification fails structural validation."""


class SpecReadError(JSONLoaderError):
    """Raised when the spec file cannot be read from disk."""


class SpecParseError(JSONLoaderError):
    """Raised when the spec file cannot be parsed as JSON."""


@dataclass(frozen=True)
class ValidationResult:
    """Container for validation outcomes for potential future enrichment."""

    details: str = ""


def load_json_spec(filepath: Path) -> Dict[str, Any]:
    """Load and parse a JSON specification from disk.

    The function centralises error handling so callers receive descriptive
    exceptions regardless of whether the failure occurred while reading or
    parsing the file.
    """

    try:
        raw_text = filepath.read_text(encoding="utf-8")
    except FileNotFoundError as exc:  # pragma: no cover - exercised via tests
        raise SpecReadError(f"Specification not found: {filepath}") from exc
    except OSError as exc:  # pragma: no cover
        raise SpecReadError(f"Unable to read specification {filepath}: {exc}") from exc

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        message = f"Invalid JSON in {filepath}: {exc.msg} (line {exc.lineno}, column {exc.colno})"
        raise SpecParseError(message) from exc


def validate_json_structure(spec: Mapping[str, Any]) -> ValidationResult:
    """Ensure the loaded specification matches the structural contract.

    Collects all validation issues before raising so users see every problem at
    once instead of fixing them iteratively.
    """

    errors: list[str] = []

    if not isinstance(spec, Mapping):
        raise SpecValidationError("Specification must be a mapping/dictionary.")

    missing_top_level = REQUIRED_TOP_LEVEL_KEYS - spec.keys()
    if missing_top_level:
        errors.append(f"Missing top-level keys: {sorted(missing_top_level)}")

    workbook = spec.get("workbook")
    if not isinstance(workbook, Mapping):
        errors.append("'workbook' must be an object containing sheet metadata.")
    else:
        _validate_sheets_section(workbook, errors)
        _validate_named_ranges(workbook, errors)

    sheets_payload = spec.get("sheets")
    if not isinstance(sheets_payload, Mapping):
        errors.append("'sheets' must be an object keyed by sheet name.")

    if errors:
        raise SpecValidationError("; ".join(errors))

    return ValidationResult()


def _validate_sheets_section(workbook: Mapping[str, Any], errors: list[str]) -> None:
    """Validate the workbook.sheets collection from the specification."""

    sheets_meta = workbook.get("sheets")
    if not isinstance(sheets_meta, Iterable):
        errors.append("'workbook.sheets' must be a list of sheet definitions.")
        return

    discovered_names: set[str] = set()
    for index, sheet in enumerate(sheets_meta, start=1):
        if not isinstance(sheet, Mapping):
            errors.append(f"Sheet entry #{index} must be an object with sheet metadata.")
            continue

        name = sheet.get("name")
        visibility = sheet.get("visibility", "visible")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"Sheet entry #{index} is missing a valid 'name'.")
        else:
            discovered_names.add(name)

        if visibility not in {"visible", "hidden", "veryHidden"}:
            errors.append(
                f"Sheet '{name or index}' has unsupported visibility '{visibility}'."
            )

    missing = REQUIRED_SHEET_NAMES - discovered_names
    if missing:
        errors.append(f"Missing required sheets: {sorted(missing)}")


def _validate_named_ranges(workbook: Mapping[str, Any], errors: list[str]) -> None:
    """Validate the workbook.named_ranges mapping."""

    named_ranges = workbook.get("named_ranges")
    if named_ranges is None:
        errors.append("'workbook.named_ranges' must be declared.")
        return

    if not isinstance(named_ranges, Mapping):
        errors.append("'workbook.named_ranges' must be an object keyed by range name.")
        return

    for name, payload in named_ranges.items():
        if not isinstance(name, str) or not name:
            errors.append("Named range keys must be non-empty strings.")
            continue

        if not isinstance(payload, Mapping):
            errors.append(f"Named range '{name}' must map to an object.")
            continue

        sheet_name = payload.get("sheet")
        cell_range = payload.get("ref")
        if sheet_name not in REQUIRED_SHEET_NAMES:
            errors.append(
                f"Named range '{name}' targets unknown sheet '{sheet_name}'."
            )
        if not isinstance(cell_range, str) or not cell_range:
            errors.append(f"Named range '{name}' must provide a cell reference in 'ref'.")
