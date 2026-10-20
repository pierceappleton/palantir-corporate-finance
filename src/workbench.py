"""Bounded driver workbench and one-at-a-time / equal-proportional sensitivities."""
import copy

from src.model import dump_csv, forecast, load, value

BOUNDS = {
    "growth_shift": (-0.15, 0.15),
    "margin_shift": (-0.05, 0.05),
    "wacc": (0.08, 0.13),
    "terminal_growth": (0.02, 0.04),
    "terminal_roic": (0.02, 0.30),
}


def calculate(data, config, growth_shift=0.0, margin_shift=0.0, wacc=None, terminal_growth=None, terminal_roic=None):
    """Recalculate the base case with bounded driver changes; raise outside disclosed bounds."""
    c = copy.deepcopy(config)
    case = copy.deepcopy(c["cases"]["base"])
    values = {
        "growth_shift": growth_shift,
        "margin_shift": margin_shift,
        "wacc": wacc if wacc is not None else case["wacc"],
        "terminal_growth": terminal_growth if terminal_growth is not None else case["growth"],
        "terminal_roic": terminal_roic if terminal_roic is not None else c["terminal_roic"],
    }
    for key, x in values.items():
        lo, hi = BOUNDS[key]
        if not lo <= x <= hi:
            raise ValueError(f"{key} outside disclosed workbench bounds")
    for key in ["commercial_growth", "government_growth"]:
        case[key] = [x if i == 0 else x + growth_shift for i, x in enumerate(case[key])]
    case["margins"] = [x + margin_shift for x in case["margins"]]
    case["wacc"] = values["wacc"]
    case["growth"] = values["terminal_growth"]
    c["terminal_roic"] = values["terminal_roic"]
    rows = forecast(case, data, c)
    v = value(rows, case, data, c)
    return rows, v


def sensitivities():
    """Write one-at-a-time and equal 10% proportional sensitivity tables."""
    data, c = load()
    rows = []
    for driver, changes in [("growth_shift", [-0.10, 0, 0.10]), ("margin_shift", [-0.03, 0, 0.03])]:
        for change in changes:
            f, v = calculate(data, c, **{driver: change})
            rows.append(
                dict(
                    driver=driver,
                    input=change,
                    units="absolute percentage-point shift as decimal",
                    operating_profit_2030=f[-1]["ebit"],
                    fcff_2030=f[-1]["fcff"],
                    per_share=v["per_share"],
                )
            )
    dump_csv("outputs/one_at_a_time.csv", rows)

    # Equal 10% proportional perturbations of the base rate/level, not equal percentage points.
    equal = []
    for driver in ["growth_rates", "operating_margins"]:
        for multiplier in [0.9, 1, 1.1]:
            case = copy.deepcopy(c["cases"]["base"])
            if driver == "growth_rates":
                for key in ["commercial_growth", "government_growth"]:
                    case[key] = [x if i == 0 else x * multiplier for i, x in enumerate(case[key])]
            else:
                case["margins"] = [x * multiplier for x in case["margins"]]
            f = forecast(case, data, c)
            v = value(f, case, data, c)
            equal.append(
                dict(
                    driver=driver,
                    multiplier=multiplier,
                    operating_profit_2030=f[-1]["ebit"],
                    fcff_2030=f[-1]["fcff"],
                    per_share=v["per_share"],
                )
            )
    dump_csv("outputs/equal_proportional_sensitivity.csv", equal)
    return rows, equal


if __name__ == "__main__":
    sensitivities()
