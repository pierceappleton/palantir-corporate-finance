"""Known-answer, boundary and monotonicity checks for the standalone DCF engine."""
import unittest

from src.dcf import Bridge, dcf


class DCFTests(unittest.TestCase):
    def setUp(self):
        self.bridge = Bridge(10, 20, 5, 2, 10)

    def value(self, wacc=0.1, growth=0.02):
        return dcf([100] * 5, [1, 2, 3, 4, 5], wacc, growth, 102, self.bridge)

    def test_known_annuity_and_bridge(self):
        v = self.value()
        expected = 100 * (1 - 1.1**-5) / 0.1 + 102 / 0.08 / 1.1**5
        self.assertAlmostEqual(v["enterprise_value"], expected)
        self.assertAlmostEqual(v["equity_value"], expected + 23)
        self.assertAlmostEqual(v["per_share"], (expected + 23) / 10)

    def test_predicted_wacc_direction(self):
        self.assertLess(self.value(0.11)["per_share"], self.value()["per_share"])

    def test_controlled_growth_direction(self):
        self.assertGreater(self.value(growth=0.03)["per_share"], self.value()["per_share"])

    def test_invalid_inputs(self):
        for wacc, growth in [(0, 0.02), (0.02, 0.02), (0.01, 0.02), (float("nan"), 0.02), (0.1, -1)]:
            with self.assertRaises(ValueError):
                self.value(wacc, growth)
        with self.assertRaises(ValueError):
            dcf([100] * 5, [1, 2, 2, 4, 5], 0.1, 0.02, 102, self.bridge)
        with self.assertRaises(ValueError):
            dcf([100] * 5, [1, 2, 3, 4, 5], 0.1, 0.02, 102, Bridge(0, 0, 0, 0, 0))

    def test_nonuniform_stub_period(self):
        later = dcf([100] * 5, [1.25, 2.25, 3.25, 4.25, 5.25], 0.1, 0.02, 102, self.bridge)
        self.assertAlmostEqual(later["enterprise_value"], self.value()["enterprise_value"] / 1.1**0.25)


if __name__ == "__main__":
    unittest.main()
