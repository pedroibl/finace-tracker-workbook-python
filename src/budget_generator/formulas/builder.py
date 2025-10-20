"""Small helpers that encapsulate Excel formula creation."""

from __future__ import annotations


def build_year_formula(offset: int) -> str:
    """Return the Excel formula for `StartingYear + offset`.

    Offsets may be negative; callers are responsible for constraining ranges as
    required by their sheet layouts.
    """

    return f"=StartingYear+{offset}"
