"""Helpers for creating doughnut charts on the dashboard."""

from __future__ import annotations

from typing import NamedTuple

from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.worksheet.worksheet import Worksheet


class ChartSpec(NamedTuple):
    title: str
    data_row: int
    anchor: str


CHART_SPECS: tuple[ChartSpec, ...] = (
    ChartSpec("Income (Budget vs Tracked)", data_row=3, anchor="E6"),
    ChartSpec("Expenses (Budget vs Tracked)", data_row=4, anchor="I6"),
    ChartSpec("Savings (Budget vs Tracked)", data_row=5, anchor="M6"),
)


def add_dashboard_doughnut_charts(dashboard_ws: Worksheet) -> None:
    """Attach the trio of doughnut charts to *dashboard_ws*."""

    workbook = dashboard_ws.parent
    calculations_ws = workbook["Calculations"]

    for spec in CHART_SPECS:
        chart = _build_doughnut_chart(
            calculations_ws=calculations_ws,
            title=spec.title,
            data_row=spec.data_row,
        )
        dashboard_ws.add_chart(chart, spec.anchor)


def _build_doughnut_chart(
    *,
    calculations_ws: Worksheet,
    title: str,
    data_row: int,
) -> DoughnutChart:
    chart = DoughnutChart()
    chart.title = title
    chart.style = 10
    chart.holeSize = 50
    chart.width = 8
    chart.height = 8

    # Data: budgeted vs tracked columns (F & G)
    data = Reference(
        calculations_ws,
        min_col=6,
        max_col=7,
        min_row=data_row,
        max_row=data_row,
    )
    chart.add_data(data, titles_from_data=False)

    # Categories: header row (BudgetedMonth, TrackedMonth)
    categories = Reference(
        calculations_ws,
        min_col=6,
        max_col=7,
        min_row=2,
        max_row=2,
    )
    chart.set_categories(categories)

    # Display both value and percentage labels
    for series in chart.series:
        series.dLbls = DataLabelList(showVal=True, showPercent=True)

    return chart
