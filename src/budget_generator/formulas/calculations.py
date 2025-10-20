"""Formula helpers for the Calculations worksheet."""

from __future__ import annotations

from collections.abc import Sequence


def build_choose_month_formula(cells: Sequence[str], month_name: str = "MonthIdx") -> str:
    """Return a CHOOSE formula selecting the month-specific value."""

    values = ",".join(cells)
    return f"=CHOOSE({month_name},{values})"


def build_monthly_tracking_sumproduct(
    transaction_type: str,
    *,
    month_name: str = "MonthIdx",
) -> str:
    """Return SUMPRODUCT formula computing tracked totals for a transaction type."""

    month_clause = f"(MONTH(tblTracking[Effective Date])={month_name})"
    type_clause = f'(tblTracking[Type]="{transaction_type}")'
    return f"=SUMPRODUCT({month_clause}*{type_clause}*tblTracking[Amount])"
