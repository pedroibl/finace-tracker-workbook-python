from __future__ import annotations

from budget_generator.formulas.calculations import (
    build_choose_month_formula,
    build_monthly_tracking_sumproduct,
)


def test_build_choose_month_formula_generates_expected_string() -> None:
    cells = [f"D{13 + idx}" for idx in range(12)]
    formula = build_choose_month_formula(cells)
    assert formula == "=CHOOSE(MonthIdx,D13,D14,D15,D16,D17,D18,D19,D20,D21,D22,D23,D24)"


def test_build_monthly_tracking_sumproduct_inserts_type() -> None:
    formula = build_monthly_tracking_sumproduct("Income")
    assert (
        formula
        == "=SUMPRODUCT((MONTH(tblTracking[Effective Date])=MonthIdx)*(tblTracking[Type]=\"Income\")*tblTracking[Amount])"
    )
