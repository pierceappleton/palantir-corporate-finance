"""Standalone FCFF valuation; forecast integration follows reconciled source inputs."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Bridge:
    cash: float
    investments: float
    debt: float
    other_claims: float
    shares: float

    def validate(self):
        if not all(isfinite(x) and x >= 0 for x in (self.cash,self.investments,self.debt,self.other_claims)):
            raise ValueError('Bridge amounts must be finite and nonnegative')
        if not isfinite(self.shares) or self.shares <= 0:
            raise ValueError('Positive finite shares required')

def dcf(fcffs, periods, wacc, growth, terminal_fcff, bridge):
    """All currency/share quantities use consistent millions; end-period discounting.

    Terminal FCFF is explicitly supplied from a mature operating calculation,
    rather than blindly scaling a possibly immature fifth-year cash flow.
    Terminal value is located at the final explicit forecast period.
    """
    bridge.validate()
    if not (isfinite(wacc) and isfinite(growth) and wacc > growth and wacc > 0 and growth > -1):
        raise ValueError('Require finite positive WACC > growth > -100%')
    if len(fcffs) != 5 or len(periods) != 5:
        raise ValueError('Exactly five forecast years required')
    if not all(isfinite(x) for x in fcffs) or not isfinite(terminal_fcff) or terminal_fcff <= 0:
        raise ValueError('Finite forecast and positive mature terminal FCFF required')
    if not all(isfinite(t) and t > 0 for t in periods) or any(b <= a for a,b in zip(periods,periods[1:])):
        raise ValueError('Discount periods must be positive and increasing')
    explicit=sum(f/(1+wacc)**t for f,t in zip(fcffs,periods))
    terminal=terminal_fcff/(wacc-growth)/(1+wacc)**periods[-1]
    ev=explicit+terminal
    equity=ev+bridge.cash+bridge.investments-bridge.debt-bridge.other_claims
    return dict(explicit_pv=explicit,terminal_pv=terminal,enterprise_value=ev,equity_value=equity,
                per_share=equity/bridge.shares,terminal_share=terminal/ev if ev else None)