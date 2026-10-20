"""Shared three-stage engine: explicit forecast, fade years, Gordon terminal."""
import copy
import unittest

from src.dcf import Bridge, dcf, staged_dcf
from src.model import forecast, load, value


class StagedEngineTests(unittest.TestCase):
    def setUp(self):
        self.bridge = Bridge(10, 20, 5, 2, 10)
        self.periods = [0.25, 1.25, 2.25, 3.25, 4.25]

    def test_zero_length_fade_reproduces_original_engine_exactly(self):
        original = dcf([100] * 5, self.periods, 0.1, 0.03, 103, self.bridge)
        staged = staged_dcf([100] * 5, self.periods, 0.1, 0.03, 103, self.bridge, ())
        for key, amount in original.items():
            self.assertEqual(staged[key], amount)

    def test_discount_timing_is_consistent_across_stages(self):
        # A Gordon perpetuity split into explicit fade years plus a later terminal must not change value.
        wacc, growth, first = 0.1, 0.03, 103.0
        whole = staged_dcf([100] * 5, self.periods, wacc, growth, first, self.bridge, ())
        for years in [1, 5, 10]:
            fade = [first * (1 + growth) ** (k - 1) for k in range(1, years + 1)]
            split = staged_dcf([100] * 5, self.periods, wacc, growth, first * (1 + growth) ** years, self.bridge, fade)
            self.assertAlmostEqual(split["enterprise_value"], whole["enterprise_value"], places=6)
            self.assertEqual(split["terminal_time"], self.periods[-1] + years)

    def test_wacc_must_exceed_terminal_growth(self):
        for wacc in [0.03, 0.02]:
            with self.assertRaises(ValueError):
                staged_dcf([100] * 5, self.periods, wacc, 0.03, 103, self.bridge, (50, 60))


class ModelFadeTests(unittest.TestCase):
    def setUp(self):
        self.data, self.c = load()

    def test_base_years_zero_matches_immediate_maturity(self):
        case = self.c["cases"]["base"]
        rows = forecast(case, self.data, self.c)
        self.assertEqual(self.c["terminal_fade"]["base_years"], 0)
        self.assertEqual(value(rows, case, self.data, self.c)["per_share"], value(rows, case, self.data, self.c, fade_years=0)["per_share"])

    def test_fade_and_terminal_reinvestment_follow_growth_over_roic(self):
        for case in self.c["cases"].values():
            rows = forecast(case, self.data, self.c)
            v = value(rows, case, self.data, self.c, fade_years=5)
            roic = self.c["terminal_fade"]["roic"]
            for year in v["fade"]:
                self.assertAlmostEqual(year["reinvestment"], year["nopat"] * year["growth"] / roic)
                self.assertAlmostEqual(year["fcff"], year["nopat"] - year["reinvestment"])
            self.assertAlmostEqual(v["terminal_fcff"], v["terminal_nopat"] * (1 - case["growth"] / self.c["terminal_roic"]))
            self.assertAlmostEqual(v["fade"][-1]["revenue"] * (1 + case["growth"]), v["terminal_revenue"])

    def test_linear_path_moves_toward_terminal_values(self):
        case = self.c["cases"]["base"]
        rows = forecast(case, self.data, self.c)
        fade = value(rows, case, self.data, self.c, fade_years=5)["fade"]
        growths = [x["growth"] for x in fade]
        margins = [x["margin"] for x in fade]
        self.assertEqual(growths, sorted(growths, reverse=True))
        self.assertGreater(growths[-1], case["growth"])
        self.assertGreater(margins[-1], case["terminal_margin"])

    def test_explicit_path_length_is_checked(self):
        case = self.c["cases"]["base"]
        rows = forecast(case, self.data, self.c)
        with self.assertRaises(ValueError):
            value(rows, case, self.data, self.c, fade_years=4, fade_path=self.c["terminal_fade"]["named_path"])


if __name__ == "__main__":
    unittest.main()
