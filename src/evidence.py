"""Sourced history tables built directly from the saved filings in data/raw.

Margin history: GAAP operating margin and stock-based compensation (SBC) as a percent of
revenue by quarter and year. Palantir's own "adjusted operating margin" is defined in its
earnings releases (it excludes SBC and employer payroll taxes on SBC); no release is saved in
data/raw, so that column shows GAAP + SBC only, which omits the payroll-tax piece and is
labelled as such rather than presented as the company's measure.
"""
from src.model import dump_csv
from src.source_check import rows

TENQ = "data/raw/pltr_2026q2_10q_issuer.html"
TENK = "data/raw/pltr_2025_10k_issuer.html"
INCOME_MARKER = (
    "Weighted-average shares of common stock outstanding used in computing earnings per share "
    "attributable to common stockholders, basic"
)
CASH_MARKER = "Cash, cash equivalents, and restricted cash - beginning of period"
SBC_MARKER = "Total stock-based compensation expense"


def period_row(period, kind, revenue, operating_income, sbc, source):
    """One margin-history row with computed percentages."""
    return dict(
        period=period,
        period_type=kind,
        revenue=revenue,
        gaap_operating_income=operating_income,
        gaap_operating_margin=operating_income / revenue,
        sbc=sbc,
        sbc_pct_revenue=sbc / revenue,
        gaap_plus_sbc_margin=(operating_income + sbc) / revenue,
        company_adjusted_operating_margin="pending: earnings release not saved in data/raw",
        source=source,
    )


def margin_history():
    """Return quarterly and annual GAAP margin rows from the 10-Q and 10-K."""
    q_income = rows(TENQ, INCOME_MARKER)
    q_sbc = rows(TENQ, SBC_MARKER)["Total stock-based compensation expense"]
    k_income = rows(TENK, INCOME_MARKER)
    k_sbc = rows(TENK, CASH_MARKER)["Stock-based compensation"]
    revenue = q_income["Revenue"]
    operating = q_income["Income from operations"]
    # 10-Q columns: Q2 2026, Q2 2025, six months 2026, six months 2025. Q1 = six months - Q2.
    q_source = "2026Q2 10-Q income statement and SBC expense table (data/raw/pltr_2026q2_10q_issuer.html)"
    k_source = "2025 10-K income statement and cash-flow SBC (data/raw/pltr_2025_10k_issuer.html)"
    table = [
        period_row("2023", "fiscal year", k_income["Revenue"][2], k_income["Income from operations"][2], k_sbc[2], k_source),
        period_row("2024", "fiscal year", k_income["Revenue"][1], k_income["Income from operations"][1], k_sbc[1], k_source),
        period_row("2025", "fiscal year", k_income["Revenue"][0], k_income["Income from operations"][0], k_sbc[0], k_source),
        period_row("2025 Q1", "quarter (derived: six months less Q2)", revenue[3] - revenue[1], operating[3] - operating[1], q_sbc[3] - q_sbc[1], q_source),
        period_row("2025 Q2", "quarter", revenue[1], operating[1], q_sbc[1], q_source),
        period_row("2026 Q1", "quarter (derived: six months less Q2)", revenue[2] - revenue[0], operating[2] - operating[0], q_sbc[2] - q_sbc[0], q_source),
        period_row("2026 Q2", "quarter", revenue[0], operating[0], q_sbc[0], q_source),
        period_row("2026 H1", "six months", revenue[2], operating[2], q_sbc[2], q_source),
    ]
    return table


def run():
    """Write outputs/margin_history.csv and return the rows."""
    table = margin_history()
    dump_csv("outputs/margin_history.csv", table)
    return table


if __name__ == "__main__":
    for line in run():
        print(line["period"], f"{line['gaap_operating_margin']:.1%}", f"SBC {line['sbc_pct_revenue']:.1%}")
