"""Market-implied expectations in readable terms (reverse DCF).

One price cannot pin down growth, steady-state margin and fade length at once, so each
search moves one of them and holds every other base-case input fixed:
1. the 2026-2030 revenue CAGR (same growth rate for both segments each year, base margins);
2. the steady-state (terminal) operating margin, base growth and immediate maturity;
3. the length of a linear fade before maturity, base growth and margins.
The original commercial-growth multiplier in src/model.py is kept as a diagnostic.
"""
import copy

from src.model import dump_csv, forecast, load, value


def per_share(case, data, config, fade_years=0):
    """Base-engine value for a modified case."""
    return value(forecast(case, data, config), case, data, config, fade_years=fade_years)["per_share"]


def bisect(function, target, lo, hi, steps=100):
    """Solve function(x) = target for an increasing function on [lo, hi]; None if unbracketed."""
    if function(lo) > target or function(hi) < target:
        return None
    for _ in range(steps):
        mid = (lo + hi) / 2
        if function(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def implied_revenue_cagr(data, config):
    """Uniform 2027-2030 growth for both segments that reproduces the price."""
    base = config["cases"]["base"]

    def at(growth):
        case = copy.deepcopy(base)
        case["commercial_growth"] = [0] + [growth] * 4
        case["government_growth"] = [0] + [growth] * 4
        return per_share(case, data, config)

    growth = bisect(at, config["price"], 0.0, 3.0)
    rows = forecast(base, data, config)
    base_cagr = (rows[-1]["revenue"] / rows[0]["revenue"]) ** (1 / 4) - 1
    return dict(implied_cagr_2026_2030=growth, base_cagr_2026_2030=base_cagr, revenue_2026=rows[0]["revenue"])


def implied_terminal_margin(data, config):
    """Terminal operating margin that reproduces the price, base growth and immediate maturity."""
    base = config["cases"]["base"]

    def at(margin):
        case = copy.deepcopy(base)
        case["terminal_margin"] = margin
        return per_share(case, data, config)

    ceiling = 1.0
    margin = bisect(at, config["price"], 0.01, ceiling)
    return dict(implied_terminal_margin=margin, value_at_100pct_margin=at(ceiling), base_terminal_margin=base["terminal_margin"])


def implied_fade_years(data, config, max_years=100):
    """Smallest whole number of linear fade years whose value reaches the price."""
    base = config["cases"]["base"]
    values = []
    for years in range(0, max_years + 1):
        values.append(per_share(base, data, config, fade_years=years))
        if values[-1] >= config["price"]:
            return dict(implied_fade_years=years, value_at_implied=values[-1], value_at_max=None, max_years=max_years)
    return dict(implied_fade_years=None, value_at_implied=None, value_at_max=values[-1], max_years=max_years)


def sentences(price, cagr, margin, fade, multiplier):
    """One plain sentence per expectation."""
    lines = []
    if cagr["implied_cagr_2026_2030"] is None:
        lines.append(f"At ${price:.2f}, no revenue CAGR up to 300% a year for 2026-2030 reaches the price with base margins held fixed.")
    else:
        lines.append(
            f"At ${price:.2f}, with base margins, discount rate and immediate maturity after 2030 held fixed, the market implies "
            f"revenue compounding about {cagr['implied_cagr_2026_2030']:.0%} a year from 2026 to 2030, versus {cagr['base_cagr_2026_2030']:.0%} in the base case."
        )
    if margin["implied_terminal_margin"] is None:
        lines.append(
            f"At ${price:.2f}, with base growth held fixed, no steady-state operating margin up to 100% of revenue is enough "
            f"(even 100% gives ${margin['value_at_100pct_margin']:.0f}); the price cannot be explained by maturity-year profitability alone."
        )
    else:
        lines.append(f"At ${price:.2f}, with base growth held fixed, the market implies a steady-state operating margin of about {margin['implied_terminal_margin']:.0%}.")
    if fade["implied_fade_years"] is None:
        lines.append(
            f"At ${price:.2f}, with base growth and margins held fixed, even a {fade['max_years']}-year linear fade to maturity gives only "
            f"${fade['value_at_max']:.0f}, so a longer runway alone does not reach the price."
        )
    else:
        lines.append(
            f"At ${price:.2f}, with base growth and margins held fixed, the market implies about {fade['implied_fade_years']} years of linear fade before maturity."
        )
    if "commercial_growth_multiplier" in multiplier:
        growths = ", ".join(f"{x:.0%}" for x in multiplier["annual_growths"])
        lines.append(
            f"Diagnostic only: scaling base commercial growth alone requires {multiplier['commercial_growth_multiplier']:.2f}x the base path ({growths} for 2027-2030)."
        )
    return lines


def run(multiplier):
    """Compute all expectations, write outputs/market_implied.csv and return a summary."""
    data, c = load()
    cagr = implied_revenue_cagr(data, c)
    margin = implied_terminal_margin(data, c)
    fade = implied_fade_years(data, c)
    text = sentences(c["price"], cagr, margin, fade, multiplier)
    summary = dict(price=c["price"], revenue_cagr=cagr, terminal_margin=margin, fade_length=fade, sentences=text,
                   note="One price cannot pin down growth, steady-state margin and fade length at once; each line moves one and holds the rest at base.")
    dump_csv("outputs/market_implied.csv", [dict(expectation=i + 1, sentence=s) for i, s in enumerate(text)])
    return summary


if __name__ == "__main__":
    from src.model import reverse_dcf

    data, c = load()
    for line in run(reverse_dcf(data, c))["sentences"]:
        print(line)
