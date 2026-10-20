"""Standalone FCFF valuation; forecast integration follows reconciled source inputs."""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Bridge:
    """Enterprise-to-equity bridge amounts in USD millions and shares in millions."""

    cash: float
    investments: float
    debt: float
    other_claims: float
    shares: float

    def validate(self):
        """Reject negative, infinite or missing bridge amounts."""
        amounts = (self.cash, self.investments, self.debt, self.other_claims)
        if not all(isfinite(x) and x >= 0 for x in amounts):
            raise ValueError("Bridge amounts must be finite and nonnegative")
        if not isfinite(self.shares) or self.shares <= 0:
            raise ValueError("Positive finite shares required")


def dcf(fcffs, periods, wacc, growth, terminal_fcff, bridge):
    """All currency/share quantities use consistent millions; end-period discounting.

    Terminal FCFF is explicitly supplied from a mature operating calculation,
    rather than blindly scaling a possibly immature fifth-year cash flow.
    Terminal value is located at the final explicit forecast period.
    """
    bridge.validate()
    rates_finite = isfinite(wacc) and isfinite(growth)
    if not (rates_finite and wacc > growth and wacc > 0 and growth > -1):
        raise ValueError("Require finite positive WACC > growth > -100%")
    if len(fcffs) != 5 or len(periods) != 5:
        raise ValueError("Exactly five forecast years required")
    if not all(isfinite(x) for x in fcffs) or not isfinite(terminal_fcff) or terminal_fcff <= 0:
        raise ValueError("Finite forecast and positive mature terminal FCFF required")
    periods_increase = all(later > earlier for earlier, later in zip(periods, periods[1:]))
    if not all(isfinite(t) and t > 0 for t in periods) or not periods_increase:
        raise ValueError("Discount periods must be positive and increasing")

    explicit = sum(fcff / (1 + wacc) ** t for fcff, t in zip(fcffs, periods))
    terminal = terminal_fcff / (wacc - growth) / (1 + wacc) ** periods[-1]
    enterprise_value = explicit + terminal
    equity = enterprise_value + bridge.cash + bridge.investments - bridge.debt - bridge.other_claims
    return dict(
        explicit_pv=explicit,
        terminal_pv=terminal,
        enterprise_value=enterprise_value,
        equity_value=equity,
        per_share=equity / bridge.shares,
        terminal_share=terminal / enterprise_value if enterprise_value else None,
    )


def staged_dcf(fcffs, periods, wacc, growth, terminal_fcff, bridge, fade_fcffs=()):
    """Three-stage FCFF value: explicit forecast, optional fade years, then a Gordon terminal.

    Fade year k is discounted at periods[-1] + k, and the terminal value sits at the end of
    the last fade year, so every stage uses the same end-of-period timing. With no fade years
    this returns exactly what dcf() returns.
    """
    base = dcf(fcffs, periods, wacc, growth, terminal_fcff, bridge)
    if not all(isfinite(x) for x in fade_fcffs):
        raise ValueError("Finite fade cash flows required")
    last = periods[-1]
    fade_pv = sum(fcff / (1 + wacc) ** (last + k) for k, fcff in enumerate(fade_fcffs, 1))
    terminal_time = last + len(fade_fcffs)
    terminal = terminal_fcff / (wacc - growth) / (1 + wacc) ** terminal_time
    enterprise_value = base["explicit_pv"] + fade_pv + terminal
    equity = enterprise_value + bridge.cash + bridge.investments - bridge.debt - bridge.other_claims
    return dict(
        explicit_pv=base["explicit_pv"],
        fade_pv=fade_pv,
        terminal_pv=terminal,
        terminal_time=terminal_time,
        enterprise_value=enterprise_value,
        equity_value=equity,
        per_share=equity / bridge.shares,
        terminal_share=terminal / enterprise_value if enterprise_value else None,
    )
